from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import (
    AuctionRequest, AuctionPhoto, AuctionDocument, Bid,
    AuctionDepositPayment, AuctionReport, AuctionNotification
)
from .serializers import (
    AuctionRequestSerializer, AuctionRequestCreateSerializer,
    BidSerializer, BidCreateSerializer,
    AuctionDepositPaymentSerializer,
    AuctionReportSerializer,
    AuctionNotificationSerializer,
    AuctionPhotoSerializer,
    AuctionDocumentSerializer
)
from products.models import Subcategory
from payments.zibal_service import ZibalService
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AuctionRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for auction requests
    Buyers can create and view their own auctions
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionRequestSerializer
    
    def get_queryset(self):
        """Return auctions for the current user"""
        user = self.request.user
        
        # Buyers see their own auctions
        if hasattr(user, 'profile') and user.profile.is_buyer():
            return AuctionRequest.objects.filter(buyer=user).select_related(
                'buyer', 'product', 'subcategory', 'deposit_payment', 'winner'
            ).prefetch_related('photos', 'documents', 'bids__seller')
        
        # Admins see all auctions
        if user.is_staff:
            return AuctionRequest.objects.all().select_related(
                'buyer', 'product', 'subcategory', 'deposit_payment', 'winner'
            ).prefetch_related('photos', 'documents', 'bids__seller')
        
        return AuctionRequest.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AuctionRequestCreateSerializer
        return AuctionRequestSerializer
    
    def perform_create(self, serializer):
        """Create auction request"""
        serializer.save(buyer=self.request.user, status='pending_review')
    
    @action(detail=True, methods=['post'])
    def accept_bid(self, request, pk=None):
        """Buyer accepts a bid and closes the auction early"""
        auction = self.get_object()
        
        # Check if user is the buyer
        if auction.buyer != request.user:
            return Response(
                {'error': 'Only the buyer can accept bids'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if auction is active
        if auction.status != 'active':
            return Response(
                {'error': 'Can only accept bids on active auctions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get bid ID from request
        bid_id = request.data.get('bid_id')
        if not bid_id:
            return Response(
                {'error': 'bid_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            bid = Bid.objects.get(id=bid_id, auction=auction)
        except Bid.DoesNotExist:
            return Response(
                {'error': 'Bid not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check early close restrictions
        if not auction.can_close_early():
            return Response(
                {'error': 'Cannot close auction early. For live auctions, you must wait until 1 hour before end time.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Accept bid and close auction
        auction.winner = bid
        auction.status = 'closed'
        auction.closed_at = timezone.now()
        bid.is_winner = True
        bid.save()
        auction.save()
        
        # Create notifications
        AuctionNotification.objects.create(
            auction=auction,
            user=bid.seller,
            notification_type='auction_closed',
            message=f'Your bid has been accepted for auction #{auction.id}'
        )
        
        # Notify other bidders
        other_bids = Bid.objects.filter(auction=auction).exclude(id=bid.id)
        for other_bid in other_bids:
            AuctionNotification.objects.create(
                auction=auction,
                user=other_bid.seller,
                notification_type='auction_closed',
                message=f'Auction #{auction.id} has been closed. Another bid was accepted.'
            )
        
        serializer = self.get_serializer(auction)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def close_early(self, request, pk=None):
        """Buyer closes auction early (without accepting a bid)"""
        auction = self.get_object()
        
        # Check if user is the buyer
        if auction.buyer != request.user:
            return Response(
                {'error': 'Only the buyer can close auctions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if auction is active
        if auction.status != 'active':
            return Response(
                {'error': 'Can only close active auctions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check early close restrictions
        if not auction.can_close_early():
            return Response(
                {'error': 'Cannot close auction early. For live auctions, you must wait until 1 hour before end time.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Close auction
        auction.status = 'closed'
        auction.closed_at = timezone.now()
        auction.save()
        
        # Notify all bidders
        for bid in auction.bids.all():
            AuctionNotification.objects.create(
                auction=auction,
                user=bid.seller,
                notification_type='auction_closed',
                message=f'Auction #{auction.id} has been closed by the buyer.'
            )
        
        serializer = self.get_serializer(auction)
        return Response(serializer.data)


class AuctionListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for sellers to view active auctions
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionRequestSerializer
    
    def get_queryset(self):
        """Return active auctions visible to sellers"""
        user = self.request.user
        
        # Only sellers can see active auctions
        if not hasattr(user, 'profile') or not user.profile.is_seller():
            return AuctionRequest.objects.none()
        
        # Get subcategory filter
        subcategory_id = self.request.query_params.get('subcategory', None)
        
        queryset = AuctionRequest.objects.filter(status='active').select_related(
            'buyer', 'product', 'subcategory', 'deposit_payment'
        ).prefetch_related('photos', 'documents', 'bids')
        
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        
        return queryset


class BidViewSet(viewsets.ModelViewSet):
    """
    ViewSet for bids
    Sellers can create bids, buyers can view all bids
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BidSerializer
    
    def get_queryset(self):
        """Return bids based on user role"""
        user = self.request.user
        auction_id = self.request.query_params.get('auction', None)
        
        if auction_id:
            queryset = Bid.objects.filter(auction_id=auction_id)
        else:
            queryset = Bid.objects.all()
        
        # Buyers see all bids for their auctions
        if hasattr(user, 'profile') and user.profile.is_buyer():
            queryset = queryset.filter(auction__buyer=user)
        
        # Sellers see their own bids and other bids (with masking)
        elif hasattr(user, 'profile') and user.profile.is_seller():
            # Include all bids, masking will be handled in serializer
            pass
        
        # Admins see all bids
        elif user.is_staff:
            pass
        
        else:
            queryset = Bid.objects.none()
        
        return queryset.select_related('auction', 'seller')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BidCreateSerializer
        return BidSerializer
    
    def perform_create(self, serializer):
        """Create bid with seller from request user"""
        serializer.save(seller=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_deposit_payment(request):
    """
    Request deposit payment via Zibal
    """
    auction_id = request.data.get('auction_id')
    if not auction_id:
        return Response(
            {'error': 'auction_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        auction = AuctionRequest.objects.get(id=auction_id, buyer=request.user)
    except AuctionRequest.DoesNotExist:
        return Response(
            {'error': 'Auction not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if deposit already paid
    if auction.deposit_status in ['paid', 'held_in_escrow']:
        return Response(
            {'error': 'Deposit already paid'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if payment already exists (OneToOneField constraint)
    if hasattr(auction, 'deposit_payment_detail'):
        # Payment exists but not verified - reuse it
        payment = auction.deposit_payment_detail
        if payment.status == 'verified':
            return Response(
                {'error': 'Deposit already paid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # If payment failed, we can create a new one by deleting the old one
        if payment.status == 'failed':
            payment.delete()
    
    # Get deposit amount from settings (in Toman)
    amount_toman = getattr(settings, 'AUCTION_DEPOSIT_AMOUNT', 5000000)
    # Convert to Rials for Zibal (1 Toman = 10 Rials)
    amount_rials = amount_toman * 10
    
    # Create payment record (store in Toman)
    payment = AuctionDepositPayment.objects.create(
        auction=auction,
        user=request.user,
        amount=amount_toman,
        status='pending'
    )
    
    # Request payment from Zibal (amount in Rials)
    zibal = ZibalService()
    success, data = zibal.request_payment(
        amount=amount_rials,
        callback_url=f"{settings.SITE_URL}/api/auctions/deposit/callback/",
        description=f"Deposit for Auction #{auction.id}",
        order_id=str(payment.order_id)
    )
    
    if success:
        payment.track_id = str(data.get('trackId'))
        payment.save()
        
        payment_url = zibal.get_payment_url(payment.track_id)
        
        return Response({
            'track_id': payment.track_id,
            'payment_url': payment_url,
            'payment_id': payment.id
        }, status=status.HTTP_200_OK)
    else:
        payment.status = 'failed'
        payment.save()
        return Response(
            {'error': 'Failed to create payment request', 'detail': data},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def deposit_callback(request):
    """
    Zibal callback for deposit payment
    """
    success_flag = request.GET.get('success', '0')
    track_id = request.GET.get('trackId')
    status_code = request.GET.get('status')
    
    if not track_id:
        return Response({'error': 'trackId is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment = AuctionDepositPayment.objects.get(track_id=str(track_id))
    except AuctionDepositPayment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if success_flag == '1' and status_code in ['1', '2']:
        # Payment was successful, verify it
        zibal = ZibalService()
        verify_success, verify_data = zibal.verify_payment(str(track_id))
        
        if verify_success:
            payment.mark_as_paid(
                ref_number=verify_data.get('refNumber'),
                card_number=verify_data.get('cardNumber')
            )
            payment.mark_as_verified()
            payment.zibal_response = verify_data
            payment.save()
            
            # Update auction
            payment.auction.request_type = 'verified'
            payment.auction.deposit_status = 'held_in_escrow'
            payment.auction.save()
            
            logger.info(f"Deposit payment verified: track_id={track_id}, auction={payment.auction.id}")
            
            # Redirect to success page
            frontend_url = _get_frontend_url(request)
            from django.shortcuts import redirect
            return redirect(f"{frontend_url}/buyer/auctions/{payment.auction.id}?payment=success")
        else:
            payment.mark_as_failed()
            payment.zibal_response = verify_data
            payment.save()
            
            logger.error(f"Deposit payment verification failed: track_id={track_id}")
            
            frontend_url = _get_frontend_url(request)
            from django.shortcuts import redirect
            return redirect(f"{frontend_url}/buyer/auctions/{payment.auction.id}?payment=failed")
    else:
        payment.mark_as_failed()
        payment.save()
        
        frontend_url = _get_frontend_url(request)
        from django.shortcuts import redirect
        return redirect(f"{frontend_url}/buyer/auctions/{payment.auction.id}?payment=failed")


def _get_frontend_url(request):
    """Helper to get frontend URL for redirects"""
    import os
    
    # Try FRONTEND_URL from settings or environment
    frontend_url = getattr(settings, 'FRONTEND_URL', None)
    if not frontend_url:
        frontend_url = os.environ.get('FRONTEND_URL', '').strip()
    
    # Fallback to SITE_URL
    if not frontend_url:
        frontend_url = getattr(settings, 'SITE_URL', '').strip()
        if not frontend_url:
            frontend_url = os.environ.get('SITE_URL', '').strip()
    
    # In development, replace port 8000 with 3000 if needed
    if settings.DEBUG and frontend_url and ':8000' in frontend_url:
        frontend_url = frontend_url.replace(':8000', ':3000')
    
    return frontend_url.rstrip('/') if frontend_url else 'http://localhost:3000'


class AuctionReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for auction reports (admin only)
    """
    permission_classes = [IsAdminUser]
    serializer_class = AuctionReportSerializer
    
    def get_queryset(self):
        return AuctionReport.objects.all().select_related('auction', 'admin')
    
    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class AuctionNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for auction notifications
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionNotificationSerializer
    
    def get_queryset(self):
        """Return notifications for current user"""
        return AuctionNotification.objects.filter(
            user=self.request.user
        ).select_related('auction').order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})


# Photo and Document upload endpoints
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_auction_photo(request):
    """Upload photo for auction request"""
    if 'image' not in request.FILES:
        return Response(
            {'error': 'image file is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    photo = AuctionPhoto.objects.create(
        auction=None,  # Will be associated when auction is created
        image=request.FILES['image']
    )
    
    serializer = AuctionPhotoSerializer(photo, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_auction_document(request):
    """Upload document for verified auction request"""
    # Check if user has paid deposit or is verified
    user = request.user
    has_deposit = AuctionDepositPayment.objects.filter(
        user=user,
        status='verified'
    ).exists()
    
    # Check if user is verified (premium user)
    is_verified = hasattr(user, 'profile') and user.profile.is_verified
    
    if not (has_deposit or is_verified):
        return Response(
            {'error': 'Documents can only be uploaded for verified requests with paid deposit'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if 'file' not in request.FILES:
        return Response(
            {'error': 'file is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file_name = request.data.get('file_name', request.FILES['file'].name)
    
    document = AuctionDocument.objects.create(
        auction=None,  # Will be associated when auction is created
        file=request.FILES['file'],
        file_name=file_name
    )
    
    serializer = AuctionDocumentSerializer(document, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

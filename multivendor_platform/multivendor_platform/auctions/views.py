from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q

from .models import ReverseAuction, AuctionInvitation, Bid
from .serializers import (
    ReverseAuctionListSerializer,
    ReverseAuctionDetailSerializer,
    ReverseAuctionCreateSerializer,
    BidSerializer,
    BidCreateSerializer,
    AuctionAwardSerializer
)
from .permissions import IsBuyerOrReadOnly, IsInvitedSupplier, IsAuctionOwner, IsAuctionOwnerOrInvitedSupplier
from .services import AuctionService


class AuctionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReverseAuctionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for reverse auctions.
    """
    queryset = ReverseAuction.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = AuctionPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'starting_price']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return ReverseAuctionCreateSerializer
        elif self.action == 'list':
            return ReverseAuctionListSerializer
        return ReverseAuctionDetailSerializer
    
    def get_queryset(self):
        """
        Filter auctions based on user role:
        - Buyers see their own auctions
        - Suppliers see auctions they're invited to
        - Unauthenticated users see active auctions only
        """
        queryset = ReverseAuction.objects.all()
        user = self.request.user
        
        if not user.is_authenticated:
            # Public: only active auctions
            return queryset.filter(status='active')
        
        # Check user role
        try:
            profile = user.profile
            if profile.is_buyer():
                # Buyers see their own auctions
                return queryset.filter(buyer=user)
            elif profile.is_seller():
                # Suppliers see auctions they're invited to
                invited_auction_ids = AuctionInvitation.objects.filter(
                    supplier=user
                ).values_list('auction_id', flat=True)
                return queryset.filter(id__in=invited_auction_ids)
        except:
            pass
        
        # Default: return empty queryset for authenticated users without role
        return queryset.none()
    
    def get_permissions(self):
        """
        Assign permissions based on action.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsBuyerOrReadOnly]
        elif self.action in ['award', 'cancel']:
            permission_classes = [IsAuthenticated, IsAuctionOwner]
        elif self.action == 'place_bid':
            permission_classes = [IsAuthenticated, IsInvitedSupplier]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_object(self):
        """Override to check object-level permissions"""
        obj = super().get_object()
        
        # Check if user has permission to view this auction
        if self.request.user.is_authenticated:
            permission = IsAuctionOwnerOrInvitedSupplier()
            if not permission.has_object_permission(self.request, self, obj):
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You don't have permission to view this auction")
        
        return obj
    
    def create(self, request, *args, **kwargs):
        """
        Create a new auction.
        Auto-publishes and invites suppliers based on category.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set buyer
        auction = serializer.save(buyer=request.user, status='active')
        
        # Auto-invite suppliers based on category
        invited_suppliers = AuctionService.auto_invite_suppliers(auction)
        
        # Return response with invitation count
        response_serializer = ReverseAuctionDetailSerializer(auction, context={'request': request})
        return Response({
            **response_serializer.data,
            'invited_suppliers_count': len(invited_suppliers)
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='place-bid')
    def place_bid(self, request, pk=None):
        """
        Place a bid on an auction.
        Only invited suppliers can bid.
        """
        auction = self.get_object()
        
        # Validate permission
        permission = IsInvitedSupplier()
        if not permission.has_object_permission(request, self, auction):
            return Response(
                {'error': 'You are not invited to this auction'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validate bid data
        serializer = BidCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        
        # Validate bid using service
        is_valid, error_message = AuctionService.validate_bid(auction, request.user, amount)
        if not is_valid:
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create or update bid (unique constraint ensures one bid per supplier)
        bid, created = Bid.objects.update_or_create(
            auction=auction,
            supplier=request.user,
            defaults={'amount': amount}
        )
        
        # Recalculate all ranks
        AuctionService.calculate_all_ranks(auction)
        
        # Check for soft close extension
        extended = AuctionService.check_soft_close(auction)
        
        # Refresh bid to get updated rank
        bid.refresh_from_db()
        
        # Mark invitation as viewed
        try:
            invitation = AuctionInvitation.objects.get(auction=auction, supplier=request.user)
            invitation.mark_viewed()
        except AuctionInvitation.DoesNotExist:
            pass
        
        return Response({
            'bid': BidSerializer(bid, context={'request': request}).data,
            'rank': bid.rank,
            'is_winning': bid.is_winning,
            'deadline_extended': extended,
            'message': 'Bid placed successfully'
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='my-status')
    def my_status(self, request, pk=None):
        """
        Get current user's bid status and rank.
        Only for invited suppliers.
        """
        auction = self.get_object()
        
        try:
            bid = auction.bids.get(supplier=request.user)
            return Response({
                'has_bid': True,
                'bid': BidSerializer(bid, context={'request': request}).data,
                'rank': bid.rank,
                'is_winning': bid.is_winning
            })
        except Bid.DoesNotExist:
            # Check if invited
            is_invited = AuctionInvitation.objects.filter(
                auction=auction,
                supplier=request.user
            ).exists()
            
            return Response({
                'has_bid': False,
                'is_invited': is_invited,
                'message': 'You have not placed a bid yet' if is_invited else 'You are not invited to this auction'
            })
    
    @action(detail=True, methods=['get'], url_path='bids')
    def bids(self, request, pk=None):
        """
        Get all bids for an auction.
        Only buyer can see this, and only after deadline.
        """
        auction = self.get_object()
        
        # Check if user is the buyer
        if request.user != auction.buyer:
            return Response(
                {'error': 'Only the auction creator can view all bids'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if deadline has passed or auction is closed
        if auction.status == 'active' and timezone.now() < auction.deadline:
            return Response({
                'bids': [],
                'message': 'Bids will be visible after the deadline'
            })
        
        # Get all bids sorted by amount (lowest first)
        bids = auction.bids.all().order_by('amount', 'created_at')
        serializer = BidSerializer(bids, many=True, context={'request': request})
        
        return Response({
            'bids': serializer.data,
            'total_count': bids.count()
        })
    
    @action(detail=True, methods=['post'], url_path='award')
    def award(self, request, pk=None):
        """
        Award the auction to a winning bid.
        Only buyer can do this, and only after deadline.
        """
        auction = self.get_object()
        
        # Validate permission
        permission = IsAuctionOwner()
        if not permission.has_object_permission(request, self, auction):
            return Response(
                {'error': 'Only the auction creator can award the auction'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check auction is closed
        if auction.status != 'closed':
            return Response(
                {'error': 'Auction must be closed before awarding'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate award data
        serializer = AuctionAwardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bid_id = serializer.validated_data['bid_id']
        
        try:
            winning_bid = Bid.objects.get(id=bid_id, auction=auction)
        except Bid.DoesNotExist:
            return Response(
                {'error': 'Bid not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Award auction
        success, error_message = AuctionService.award_auction(auction, winning_bid)
        if not success:
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Return updated auction
        serializer = ReverseAuctionDetailSerializer(auction, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """
        Cancel an auction.
        Only buyer can do this.
        """
        auction = self.get_object()
        
        # Validate permission
        permission = IsAuctionOwner()
        if not permission.has_object_permission(request, self, auction):
            return Response(
                {'error': 'Only the auction creator can cancel the auction'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check auction can be cancelled
        if auction.status in ['awarded', 'cancelled']:
            return Response(
                {'error': f'Cannot cancel auction with status: {auction.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        auction.status = 'cancelled'
        auction.save(update_fields=['status'])
        
        serializer = ReverseAuctionDetailSerializer(auction, context={'request': request})
        return Response(serializer.data)




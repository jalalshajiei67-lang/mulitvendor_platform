"""
Payment API Views
"""
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from decimal import Decimal
import logging

from .models import PremiumSubscriptionPayment, PaymentInvoice
from .serializers import (
    PremiumSubscriptionPaymentSerializer,
    PaymentInvoiceSerializer,
    PaymentRequestSerializer,
    PaymentCallbackSerializer,
)
from .zibal_service import ZibalService
from .invoice_generator import create_invoice_for_payment
from users.models import VendorSubscription, PricingTier

logger = logging.getLogger(__name__)


# Pricing configuration (in Toman, will be converted to Rial for Zibal)
PRICING_CONFIG = {
    'monthly': 1_500_000,  # 1.5 million Toman
    'quarterly': 4_500_000,  # 4.5 million Toman
    'semiannual': 9_000_000,  # 9 million Toman
    'yearly': 14_400_000,  # 14.4 million Toman (20% discount)
}


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_premium_payment(request):
    """
    Step 1: Request payment from Zibal
    
    POST /api/payments/premium/request/
    Body: {"billing_period": "monthly"}
    """
    serializer = PaymentRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    billing_period = serializer.validated_data['billing_period']
    
    # Get amount in Toman
    amount_toman = PRICING_CONFIG.get(billing_period, PRICING_CONFIG['monthly'])
    amount_rial = amount_toman * 10  # Convert to Rial
    
    # Create payment record
    try:
        payment = PremiumSubscriptionPayment.objects.create(
            user=request.user,
            billing_period=billing_period,
            amount=amount_rial,
            description=f"Premium Subscription - {billing_period}",
        )
        
        # Request payment from Zibal
        zibal = ZibalService()
        callback_url = f"{settings.SITE_URL}/api/payments/premium/callback/"
        
        success, response_data = zibal.request_payment(
            amount=int(amount_rial),
            callback_url=callback_url,
            description=payment.description,
            order_id=str(payment.order_id),
            mobile=getattr(request.user.vendor_profile, 'contact_phone', '') if hasattr(request.user, 'vendor_profile') else ''
        )
        
        if success:
            # Update payment with track_id
            track_id = response_data.get('trackId')
            payment.track_id = str(track_id)
            payment.zibal_response = response_data
            payment.save()
            
            # Generate payment URL
            payment_url = zibal.get_payment_url(track_id)
            
            logger.info(f"Payment requested successfully for user {request.user.id}, track_id: {track_id}")
            
            return Response({
                'success': True,
                'track_id': track_id,
                'payment_url': payment_url,
                'amount': amount_rial,
                'amount_toman': amount_toman,
                'order_id': str(payment.order_id),
            }, status=status.HTTP_200_OK)
        else:
            # Payment request failed
            payment.status = 'failed'
            payment.zibal_response = response_data
            payment.save()
            
            error_msg = response_data.get('error', 'خطا در درخواست پرداخت')
            logger.error(f"Payment request failed for user {request.user.id}: {error_msg}")
            
            return Response({
                'success': False,
                'error': error_msg,
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Exception in payment request for user {request.user.id}: {str(e)}")
        return Response({
            'success': False,
            'error': 'خطای سیستمی در ایجاد درخواست پرداخت'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def payment_callback(request):
    """
    Step 2: Callback from Zibal after payment
    
    GET /api/payments/premium/callback/?trackId=...&success=1&status=2&orderId=...
    """
    serializer = PaymentCallbackSerializer(data=request.GET)
    if not serializer.is_valid():
        # Redirect to failure page
        frontend_url = settings.SITE_URL.replace(':8000', ':3000')  # Assuming Nuxt runs on 3000
        return redirect(f"{frontend_url}/seller/payment-result?status=failed&error=invalid_callback")
    
    track_id = serializer.validated_data['trackId']
    success_flag = serializer.validated_data['success']
    payment_status = serializer.validated_data['status']
    
    try:
        # Find payment by track_id
        payment = PremiumSubscriptionPayment.objects.get(track_id=str(track_id))
        
        if success_flag == 1 and payment_status in [1, 2]:
            # Payment was successful, now verify it
            zibal = ZibalService()
            verify_success, verify_data = zibal.verify_payment(str(track_id))
            
            if verify_success:
                # Update payment record
                payment.mark_as_paid(
                    ref_number=verify_data.get('refNumber'),
                    card_number=verify_data.get('cardNumber')
                )
                payment.mark_as_verified()
                payment.zibal_response = verify_data
                payment.save()
                
                # Activate premium subscription
                activate_premium_subscription(payment.user, payment)
                
                # Generate invoice
                invoice = create_invoice_for_payment(payment)
                
                logger.info(f"Payment verified successfully: track_id={track_id}, user={payment.user.id}")
                
                # Redirect to success page
                frontend_url = settings.SITE_URL.replace(':8000', ':3000')
                return redirect(f"{frontend_url}/seller/payment-result?status=success&track_id={track_id}")
            else:
                # Verification failed
                payment.mark_as_failed()
                payment.zibal_response = verify_data
                payment.save()
                
                logger.error(f"Payment verification failed: track_id={track_id}")
                
                # Redirect to failure page
                frontend_url = settings.SITE_URL.replace(':8000', ':3000')
                error_msg = verify_data.get('error', 'verification_failed')
                return redirect(f"{frontend_url}/seller/payment-result?status=failed&error={error_msg}")
        else:
            # Payment was not successful
            payment.mark_as_failed()
            payment.save()
            
            logger.warning(f"Payment callback with failure: track_id={track_id}, status={payment_status}")
            
            # Redirect to failure page
            frontend_url = settings.SITE_URL.replace(':8000', ':3000')
            return redirect(f"{frontend_url}/seller/payment-result?status=cancelled")
    
    except PremiumSubscriptionPayment.DoesNotExist:
        logger.error(f"Payment not found for track_id: {track_id}")
        frontend_url = settings.SITE_URL.replace(':8000', ':3000')
        return redirect(f"{frontend_url}/seller/payment-result?status=failed&error=payment_not_found")
    
    except Exception as e:
        logger.error(f"Exception in payment callback: {str(e)}")
        frontend_url = settings.SITE_URL.replace(':8000', ':3000')
        return redirect(f"{frontend_url}/seller/payment-result?status=failed&error=system_error")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment_manual(request, track_id):
    """
    Step 3: Manually verify payment (if needed)
    
    POST /api/payments/premium/verify/<track_id>/
    """
    try:
        payment = PremiumSubscriptionPayment.objects.get(track_id=str(track_id), user=request.user)
        
        if payment.status == 'verified':
            return Response({
                'success': True,
                'message': 'پرداخت قبلاً تایید شده است',
                'payment': PremiumSubscriptionPaymentSerializer(payment).data
            })
        
        # Verify with Zibal
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
            
            # Activate premium subscription
            activate_premium_subscription(payment.user, payment)
            
            # Generate invoice
            invoice = create_invoice_for_payment(payment)
            
            return Response({
                'success': True,
                'message': 'پرداخت با موفقیت تایید شد',
                'payment': PremiumSubscriptionPaymentSerializer(payment).data,
                'invoice': PaymentInvoiceSerializer(invoice, context={'request': request}).data if invoice else None
            })
        else:
            return Response({
                'success': False,
                'error': verify_data.get('error', 'تایید پرداخت ناموفق بود')
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except PremiumSubscriptionPayment.DoesNotExist:
        return Response({
            'success': False,
            'error': 'پرداخت یافت نشد'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Exception in verify payment: {str(e)}")
        return Response({
            'success': False,
            'error': 'خطای سیستمی'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentHistoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """
    Get payment history for current user
    
    GET /api/payments/history/?status=&page=1
    """
    queryset = PremiumSubscriptionPayment.objects.filter(user=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    # Pagination
    paginator = PaymentHistoryPagination()
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        serializer = PremiumSubscriptionPaymentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = PremiumSubscriptionPaymentSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_invoice(request, invoice_id):
    """
    Download invoice PDF
    
    GET /api/payments/invoice/<invoice_id>/download/
    """
    try:
        invoice = PaymentInvoice.objects.get(
            id=invoice_id,
            payment__user=request.user
        )
        
        if not invoice.invoice_pdf:
            return Response({
                'error': 'فاکتور PDF یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return FileResponse(
            invoice.invoice_pdf.open('rb'),
            as_attachment=True,
            filename=f'invoice_{invoice.invoice_number}.pdf'
        )
    
    except PaymentInvoice.DoesNotExist:
        return Response({
            'error': 'فاکتور یافت نشد'
        }, status=status.HTTP_404_NOT_FOUND)


def activate_premium_subscription(user, payment):
    """
    Activate premium subscription for user
    
    Args:
        user: User instance
        payment: PremiumSubscriptionPayment instance
    """
    try:
        # Get or create subscription
        subscription = VendorSubscription.for_user(user)
        
        # Get premium tier
        premium_tier = PricingTier.objects.filter(
            slug='premium'
        ).first()
        
        if not premium_tier:
            logger.error("Premium tier not found in database")
            return
        
        # Calculate expiry date
        duration_days = payment.get_subscription_duration_days()
        expires_at = timezone.now() + timedelta(days=duration_days)
        
        # Update subscription
        subscription.tier = premium_tier
        subscription.expires_at = expires_at
        subscription.is_active = True
        subscription.save()
        
        logger.info(f"Premium subscription activated for user {user.id} until {expires_at}")
    
    except Exception as e:
        logger.error(f"Error activating premium subscription for user {user.id}: {str(e)}")


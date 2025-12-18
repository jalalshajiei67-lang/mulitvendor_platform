from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuctionRequestViewSet,
    AuctionListViewSet,
    BidViewSet,
    AuctionReportViewSet,
    AuctionNotificationViewSet,
    request_deposit_payment,
    deposit_callback,
    upload_auction_photo,
    upload_auction_document,
)

router = DefaultRouter()
router.register(r'auctions', AuctionRequestViewSet, basename='auction-request')
router.register(r'auction-list', AuctionListViewSet, basename='auction-list')
router.register(r'bids', BidViewSet, basename='bid')
router.register(r'reports', AuctionReportViewSet, basename='auction-report')
router.register(r'notifications', AuctionNotificationViewSet, basename='auction-notification')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Deposit payment
    path('deposit/request/', request_deposit_payment, name='auction-deposit-request'),
    path('deposit/callback/', deposit_callback, name='auction-deposit-callback'),
    
    # File uploads
    path('photos/upload/', upload_auction_photo, name='upload-auction-photo'),
    path('documents/upload/', upload_auction_document, name='upload-auction-document'),
]

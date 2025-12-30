from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReverseAuctionViewSet

router = DefaultRouter()
router.register(r'auctions', ReverseAuctionViewSet, basename='auction')

urlpatterns = [
    path('', include(router.urls)),
]


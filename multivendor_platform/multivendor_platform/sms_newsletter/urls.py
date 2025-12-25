from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SellerViewSet, send_sms_view

router = DefaultRouter()
router.register(r'sellers', SellerViewSet, basename='seller')

urlpatterns = [
    path('', include(router.urls)),
    path('send/', send_sms_view, name='send-sms'),
]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    login_view, logout_view, register_view, current_user_view, update_profile_view,
    buyer_dashboard_view, buyer_orders_view, buyer_reviews_view,
    seller_dashboard_view, seller_orders_view, seller_reviews_view,
    SellerAdViewSet,
    admin_dashboard_view, admin_users_view, admin_block_user_view, 
    admin_verify_user_view, admin_change_password_view, admin_activities_view,
    admin_update_order_status_view,
    SupplierViewSet, SupplierCommentViewSet
)

router = DefaultRouter()
router.register(r'ads', SellerAdViewSet, basename='sellerad')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'supplier-comments', SupplierCommentViewSet, basename='suppliercomment')

urlpatterns = [
    # Authentication
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('me/', current_user_view, name='current-user'),
    path('profile/update/', update_profile_view, name='update-profile'),
    
    # Buyer Dashboard
    path('buyer/dashboard/', buyer_dashboard_view, name='buyer-dashboard'),
    path('buyer/orders/', buyer_orders_view, name='buyer-orders'),
    path('buyer/reviews/', buyer_reviews_view, name='buyer-reviews'),
    
    # Seller Dashboard
    path('seller/dashboard/', seller_dashboard_view, name='seller-dashboard'),
    path('seller/orders/', seller_orders_view, name='seller-orders'),
    path('seller/reviews/', seller_reviews_view, name='seller-reviews'),
    
    # Admin Dashboard
    path('admin/dashboard/', admin_dashboard_view, name='admin-dashboard'),
    path('admin/users/', admin_users_view, name='admin-users'),
    path('admin/users/<int:user_id>/block/', admin_block_user_view, name='admin-block-user'),
    path('admin/users/<int:user_id>/verify/', admin_verify_user_view, name='admin-verify-user'),
    path('admin/change-password/', admin_change_password_view, name='admin-change-password'),
    path('admin/activities/', admin_activities_view, name='admin-activities'),
    path('admin/orders/<int:order_id>/status/', admin_update_order_status_view, name='admin-update-order-status'),
    
    # Seller Ads (ViewSet routes)
    path('', include(router.urls)),
]


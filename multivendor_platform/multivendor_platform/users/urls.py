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
    admin_products_view, admin_product_detail_view, admin_product_bulk_action_view,
    admin_delete_product_view,
    admin_departments_view, admin_department_detail_view, admin_create_department_view,
    admin_update_department_view, admin_delete_department_view,
    admin_categories_view, admin_category_detail_view, admin_create_category_view,
    admin_update_category_view, admin_delete_category_view,
    admin_subcategories_view, admin_subcategory_detail_view, admin_create_subcategory_view,
    admin_update_subcategory_view, admin_delete_subcategory_view,
    admin_blog_posts_view, admin_blog_categories_view,
    SupplierViewSet, SupplierCommentViewSet,
    SupplierPortfolioItemViewSet, SupplierTeamMemberViewSet, SupplierContactMessageViewSet,
    otp_request_view, otp_verify_view, password_reset_view
)

router = DefaultRouter()
router.register(r'ads', SellerAdViewSet, basename='sellerad')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'supplier-comments', SupplierCommentViewSet, basename='suppliercomment')
router.register(r'supplier-portfolio', SupplierPortfolioItemViewSet, basename='supplierportfolio')
router.register(r'supplier-team', SupplierTeamMemberViewSet, basename='supplierteam')
router.register(r'supplier-contact', SupplierContactMessageViewSet, basename='suppliercontact')

urlpatterns = [
    # Authentication
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('me/', current_user_view, name='current-user'),
    path('profile/update/', update_profile_view, name='update-profile'),
    
    # OTP Authentication
    path('otp/request/', otp_request_view, name='otp-request'),
    path('otp/verify/', otp_verify_view, name='otp-verify'),
    path('password-reset/', password_reset_view, name='password-reset'),
    
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
    
    # Admin Product Management
    path('admin/products/', admin_products_view, name='admin-products'),
    path('admin/products/<int:product_id>/', admin_product_detail_view, name='admin-product-detail'),
    path('admin/products/bulk-action/', admin_product_bulk_action_view, name='admin-product-bulk-action'),
    path('admin/products/<int:product_id>/delete/', admin_delete_product_view, name='admin-delete-product'),
    
    # Admin Department Management
    path('admin/departments/', admin_departments_view, name='admin-departments'),
    path('admin/departments/<int:department_id>/', admin_department_detail_view, name='admin-department-detail'),
    path('admin/departments/create/', admin_create_department_view, name='admin-create-department'),
    path('admin/departments/<int:department_id>/update/', admin_update_department_view, name='admin-update-department'),
    path('admin/departments/<int:department_id>/delete/', admin_delete_department_view, name='admin-delete-department'),
    
    # Admin Category Management
    path('admin/categories/', admin_categories_view, name='admin-categories'),
    path('admin/categories/<int:category_id>/', admin_category_detail_view, name='admin-category-detail'),
    path('admin/categories/create/', admin_create_category_view, name='admin-create-category'),
    path('admin/categories/<int:category_id>/update/', admin_update_category_view, name='admin-update-category'),
    path('admin/categories/<int:category_id>/delete/', admin_delete_category_view, name='admin-delete-category'),
    
    # Admin Subcategory Management
    path('admin/subcategories/', admin_subcategories_view, name='admin-subcategories'),
    path('admin/subcategories/<int:subcategory_id>/', admin_subcategory_detail_view, name='admin-subcategory-detail'),
    path('admin/subcategories/create/', admin_create_subcategory_view, name='admin-create-subcategory'),
    path('admin/subcategories/<int:subcategory_id>/update/', admin_update_subcategory_view, name='admin-update-subcategory'),
    path('admin/subcategories/<int:subcategory_id>/delete/', admin_delete_subcategory_view, name='admin-delete-subcategory'),
    
    # Admin Blog Management
    path('admin/blog/posts/', admin_blog_posts_view, name='admin-blog-posts'),
    path('admin/blog/categories/', admin_blog_categories_view, name='admin-blog-categories'),
    
    # Seller Ads (ViewSet routes)
    path('', include(router.urls)),
]


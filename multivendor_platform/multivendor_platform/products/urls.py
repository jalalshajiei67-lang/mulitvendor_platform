# multivendor_platform/multivendor_platform/products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, SubcategoryViewSet, DepartmentViewSet, 
    MyProductsView, ProductCommentViewSet, global_search
)
from .test_scraper_api import test_scraper_connection, test_network_access

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-comments', ProductCommentViewSet, basename='product-comment')

urlpatterns = [
    # Put specific routes FIRST before router
    path('products/my_products/', MyProductsView.as_view({'get': 'list'}), name='my-products'),
    path('search/', global_search, name='global-search'),
    
    # Scraper test endpoints (admin only)
    path('test-scraper/', test_scraper_connection, name='test-scraper'),
    path('test-network/', test_network_access, name='test-network'),
    
    # Then include router URLs (this will handle all ViewSet routes automatically)
    path('', include(router.urls)),
]
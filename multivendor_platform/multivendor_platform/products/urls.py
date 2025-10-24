# multivendor_platform/multivendor_platform/products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, SubcategoryViewSet, DepartmentViewSet, 
    MyProductsView, ProductCommentViewSet, global_search
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'product-comments', ProductCommentViewSet)

urlpatterns = [
    # Put specific routes FIRST
    path('products/my_products/', MyProductsView.as_view({'get': 'list'}), name='my-products'),
    path('search/', global_search, name='global-search'),
    
    # Then include router URLs
    path('', include(router.urls)),
    
    # Register products separately to avoid conflicts
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product-detail'),
]
# multivendor_platform/multivendor_platform/products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, SubcategoryViewSet, DepartmentViewSet,
    MyProductsView, ProductCommentViewSet, global_search,
    LabelGroupViewSet, LabelViewSet, LabelComboSeoPageViewSet,
    CategoryRequestViewSet, ProductUploadRequestViewSet,
    admin_product_upload_requests_view
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Label
from .serializers import LabelSerializer
from django.shortcuts import get_object_or_404

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-comments', ProductCommentViewSet, basename='product-comment')
router.register(r'label-groups', LabelGroupViewSet, basename='label-group')
router.register(r'labels', LabelViewSet, basename='label')
router.register(r'label-combos', LabelComboSeoPageViewSet, basename='label-combo')
router.register(r'category-requests', CategoryRequestViewSet, basename='category-request')
router.register(r'product-upload-requests', ProductUploadRequestViewSet, basename='product-upload-request')

# Custom view function for label SEO content by slug
@api_view(['GET'])
@permission_classes([AllowAny])
def label_seo_content_view(request, slug):
    """Retrieve label SEO content by slug"""
    label = get_object_or_404(Label.objects.all(), slug=slug)
    serializer = LabelSerializer(label, context={'request': request})
    return Response(serializer.data)

urlpatterns = [
    # Put specific routes FIRST before router
    path('products/my_products/', MyProductsView.as_view({'get': 'list'}), name='my-products'),
    path('search/', global_search, name='global-search'),
    
    # Admin endpoints
    path('admin/product-upload-requests/', admin_product_upload_requests_view, name='admin-product-upload-requests'),
    
    # Label SEO content by slug (custom route before router)
    # Using a more specific path to avoid router conflicts
    path('labels/seo-content/<slug>/', label_seo_content_view, name='label-seo-content'),
    
    # Then include router URLs (this will handle all ViewSet routes automatically)
    path('', include(router.urls)),
]

# Debug: Print registered URLs for category-requests
# Uncomment to debug URL registration
# print("Category Request URLs:")
# for url_pattern in router.urls:
#     if 'category-request' in str(url_pattern.pattern):
#         print(f"  {url_pattern.pattern} -> {url_pattern.callback}")
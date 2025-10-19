from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, SubcategoryViewSet, DepartmentViewSet, 
    MyProductsView, ProductCommentViewSet, global_search
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'product-comments', ProductCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/my_products/', MyProductsView.as_view({'get': 'list'}), name='my-products'),
    path('search/', global_search, name='global-search'),
]
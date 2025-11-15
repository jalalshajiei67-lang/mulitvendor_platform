# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.db import models

# REST Framework imports
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

# Local imports
from .models import Product, Category, Subcategory, Department, ProductImage, ProductComment
from .forms import ProductForm
from .serializers import (
    ProductSerializer, CategorySerializer, SubcategorySerializer, 
    DepartmentSerializer, ProductImageSerializer, ProductCommentSerializer,
    ProductCommentCreateSerializer, ProductDetailSerializer
)

# --- DJANGO DASHBOARD VIEWS ---

class HomeView(TemplateView):
    """
    Simple home page view that redirects to Vue.js frontend.
    """
    template_name = 'products/home.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect to Vue.js frontend
        return redirect('http://localhost:5173/')

class VendorDashboardView(LoginRequiredMixin, TemplateView):
    """
    Redirects to Vue.js frontend dashboard.
    """
    template_name = 'products/home.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect to Vue.js frontend my-products page
        return redirect('http://localhost:5173/my-products')

class ProductCreateView(LoginRequiredMixin, TemplateView):
    """
    Redirects to Vue.js frontend product creation form.
    """
    template_name = 'products/home.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect to Vue.js frontend product creation page
        return redirect('http://localhost:5173/products/new')

# --- DRF API VIEWSETS ---

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing products.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['vendor', 'is_active', 'primary_category']
    ordering_fields = ['created_at', 'price', 'name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Optionally restricts the returned products to a given category or subcategory,
        by filtering against query parameters in the URL.
        """
        queryset = Product.objects.all().order_by('-created_at')
        
        # Filter by category
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(primary_category=category_id)
        
        # Filter by subcategory (using M2M relationship)
        # Support both 'subcategory' (singular) and 'subcategories' (plural) parameter names
        subcategory_id = self.request.query_params.get('subcategories') or self.request.query_params.get('subcategory')
        if subcategory_id is not None:
            queryset = queryset.filter(subcategories__id=subcategory_id)
        
        return queryset.distinct()  # Use distinct to avoid duplicates from M2M
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
    
    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)', permission_classes=[AllowAny])
    def retrieve_by_slug(self, request, slug=None):
        """
        Retrieve product detail using slug instead of numeric ID.
        """
        queryset = self.get_queryset()
        product = get_object_or_404(queryset, slug=slug)
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        product = serializer.save()
        self._ensure_primary_category(product)
        self._handle_image_uploads(product)
    
    def perform_update(self, serializer):
        product = serializer.save()
        self._ensure_primary_category(product)
        self._handle_image_uploads(product)
    
    def _handle_image_uploads(self, product):
        """Handle multiple image uploads from FormData"""
        if hasattr(self.request, 'FILES'):
            images = self.request.FILES.getlist('images', [])
            if images:
                # Check if adding these images would exceed the limit
                existing_count = product.images.count()
                if existing_count + len(images) > 20:
                    raise serializers.ValidationError("Maximum 20 images allowed per product.")
                
                # Create ProductImage objects
                for i, image_file in enumerate(images):
                    is_primary = (i == 0 and existing_count == 0)  # First image is primary if no existing images
                    ProductImage.objects.create(
                        product=product,
                        image=image_file,
                        is_primary=is_primary,
                        sort_order=existing_count + i
                    )
    
    def _ensure_primary_category(self, product):
        """
        Ensure a product always has a primary category when subcategories exist.
        If the request explicitly provided a primary_category the serializer already set it.
        """
        if product.primary_category or not product.subcategories.exists():
            return
        
        fallback_category = product.subcategories.first().categories.first()
        if not fallback_category:
            return
        
        product.primary_category = fallback_category
        
        requested_is_active = self.request.data.get('is_active')
        if requested_is_active is not None:
            product.is_active = str(requested_is_active).lower() in ['true', '1', 'yes', 'on']
        elif not product.is_active:
            # Reactivate by default when we can determine a primary category
            product.is_active = True
        
        product.save(update_fields=['primary_category', 'is_active'])
    
    @action(detail=True, methods=['delete'], url_path='images/(?P<image_id>[^/.]+)')
    def delete_image(self, request, pk=None, image_id=None):
        """Delete a specific product image"""
        try:
            product = self.get_object()
            image = product.images.get(id=image_id)
            
            # Don't allow deleting the last image
            if product.images.count() <= 1:
                return Response(
                    {'error': 'Cannot delete the last image'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # If deleting primary image, make the next one primary
            if image.is_primary:
                next_image = product.images.exclude(id=image_id).first()
                if next_image:
                    next_image.is_primary = True
                    next_image.save()
            
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductImage.DoesNotExist:
            return Response(
                {'error': 'Image not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        """
        Add a comment to a product
        """
        product = self.get_object()
        serializer = ProductCommentCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(product=product, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all approved comments for a product
        """
        product = self.get_object()
        comments = product.comments.filter(is_approved=True, parent=None).order_by('-created_at')
        serializer = ProductCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing categories.
    Supports filtering by department and slug.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        """
        Optionally filter categories by department
        """
        queryset = Category.objects.all().order_by('sort_order', 'name')
        
        # Filter by department
        department_id = self.request.query_params.get('department', None)
        if department_id:
            queryset = queryset.filter(departments__id=department_id)
        
        # Filter by slug (for detail view)
        slug = self.request.query_params.get('slug', None)
        if slug:
            queryset = queryset.filter(slug=slug)
        
        return queryset.distinct()  # Use distinct to avoid duplicates from M2M
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class SubcategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing subcategories.
    Supports filtering by category and slug.
    """
    queryset = Subcategory.objects.all().order_by('name')
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        """
        Optionally filter subcategories by category
        """
        queryset = Subcategory.objects.all().order_by('sort_order', 'name')
        
        # Filter by category
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        
        # Filter by slug (for detail view)
        slug = self.request.query_params.get('slug', None)
        if slug:
            queryset = queryset.filter(slug=slug)
        
        return queryset.distinct()  # Use distinct to avoid duplicates from M2M
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing departments.
    Supports filtering by slug.
    """
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        """
        Optionally filter departments by slug
        """
        queryset = Department.objects.all().order_by('sort_order', 'name')
        
        # Filter by slug (for detail view)
        slug = self.request.query_params.get('slug', None)
        if slug:
            queryset = queryset.filter(slug=slug)
        
        return queryset
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class MyProductsView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user's own products.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user).order_by('-created_at')

class ProductCommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for product comments
    """
    queryset = ProductComment.objects.all().order_by('-created_at')
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Filter comments based on approval status
        """
        queryset = super().get_queryset()
        
        # Only show approved comments to non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Set author to current user
        """
        serializer.save(author=self.request.user)

# --- GLOBAL SEARCH API ---

@api_view(['GET'])
@permission_classes([AllowAny])
def global_search(request):
    """
    Global search endpoint that searches across products and blog posts
    Returns combined results with type indicators
    """
    from blog.models import BlogPost
    from blog.serializers import BlogPostListSerializer
    
    query = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 10))
    
    if not query or len(query) < 2:
        return Response({
            'products': [],
            'blogs': [],
            'total': 0
        })
    
    # Search products (only active ones)
    products = Product.objects.filter(
        models.Q(name__icontains=query) | models.Q(description__icontains=query),
        is_active=True
    ).select_related('subcategory', 'vendor')[:limit]
    
    # Search blog posts (only published ones)
    blogs = BlogPost.objects.filter(
        models.Q(title__icontains=query) | models.Q(content__icontains=query) | models.Q(excerpt__icontains=query),
        status='published'
    ).select_related('author', 'category')[:limit]
    
    # Serialize results
    product_serializer = ProductSerializer(products, many=True, context={'request': request})
    blog_serializer = BlogPostListSerializer(blogs, many=True, context={'request': request})
    
    return Response({
        'products': product_serializer.data,
        'blogs': blog_serializer.data,
        'total': len(products) + len(blogs)
    })
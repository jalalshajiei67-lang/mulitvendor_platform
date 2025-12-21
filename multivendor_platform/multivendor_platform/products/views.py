# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Case, When, Value, IntegerField, FloatField, BooleanField, F
from django.db.models.functions import Coalesce
from django.conf import settings
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

# REST Framework imports
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# Local imports
from .models import (
    Product,
    Category,
    Subcategory,
    Department,
    ProductImage,
    ProductComment,
    ProductFeature,
    SubcategoryFeatureTemplate,
    Label,
    LabelGroup,
    LabelComboSeoPage,
    CategoryRequest,
)
from .forms import ProductForm
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    SubcategorySerializer,
    DepartmentSerializer,
    ProductImageSerializer,
    ProductCommentSerializer,
    ProductCommentCreateSerializer,
    ProductDetailSerializer,
    SubcategoryFeatureTemplateSerializer,
    LabelSerializer,
    LabelGroupSerializer,
    LabelComboSeoPageSerializer,
    CategoryRequestSerializer,
    CategoryRequestCreateSerializer,
)

# --- DJANGO DASHBOARD VIEWS ---

class HomeView(TemplateView):
    """
    Simple home page view that redirects to Nuxt frontend.
    """
    template_name = 'products/home.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect to frontend using SITE_URL from settings, fallback to localhost for dev
        frontend_url = getattr(settings, 'SITE_URL', 'http://localhost:5173')
        return redirect(frontend_url.rstrip('/') + '/')

class VendorDashboardView(LoginRequiredMixin, TemplateView):
    """
    Redirects to Nuxt frontend dashboard.
    """
    template_name = 'products/home.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect to frontend using SITE_URL from settings, fallback to localhost for dev
        frontend_url = getattr(settings, 'SITE_URL', 'http://localhost:5173')
        return redirect(f'{frontend_url.rstrip("/")}/my-products')

class ProductCreateView(LoginRequiredMixin, TemplateView):
    """
    Redirects to Nuxt frontend product creation form.
    """
    template_name = 'products/home.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect to frontend using SITE_URL from settings, fallback to localhost for dev
        frontend_url = getattr(settings, 'SITE_URL', 'http://localhost:5173')
        return redirect(f'{frontend_url.rstrip("/")}/products/new')

# --- DRF API VIEWSETS ---

class ProductPagination(PageNumberPagination):
    """
    Custom pagination class for products that allows client to specify page size
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing products.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['vendor', 'is_active', 'primary_category', 'approval_status', 'is_marketplace_hidden']
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
        queryset = (
            Product.objects.all()
            .select_related('vendor__profile', 'vendor__vendor_profile__engagement', 'primary_category', 'supplier')
            .prefetch_related('images', 'subcategories', 'labels', 'features')
            .annotate(
                vendor_total_points=Coalesce(
                    F('vendor__vendor_profile__engagement__total_points'),
                    Value(0),
                ),
                vendor_reputation_score=Coalesce(
                    F('vendor__vendor_profile__engagement__reputation_score'),
                    Value(0.0),
                    output_field=FloatField(),
                ),
                vendor_is_premium=Coalesce(
                    F('vendor__profile__is_verified'),
                    Value(False),
                    output_field=BooleanField(),
                ),
            )
        )

        user = self.request.user
        if not getattr(user, 'is_staff', False):
            visibility_filter = models.Q(
                approval_status=Product.APPROVAL_STATUS_APPROVED,
                is_active=True,
                is_marketplace_hidden=False,
            )
            if getattr(user, 'is_authenticated', False):
                visibility_filter = visibility_filter | models.Q(vendor=user)
            queryset = queryset.filter(visibility_filter)

        # Annotate tier values for ordering/display (mirrors GamificationService.calculate_tier)
        queryset = queryset.annotate(
            vendor_tier=Case(
                When(
                    models.Q(vendor_total_points__gte=1000) & models.Q(vendor_reputation_score__gte=80),
                    then=Value('diamond'),
                ),
                When(
                    models.Q(vendor_total_points__gte=500) & models.Q(vendor_reputation_score__gte=60),
                    then=Value('gold'),
                ),
                When(models.Q(vendor_total_points__gte=200), then=Value('silver')),
                When(models.Q(vendor_total_points__gte=50), then=Value('bronze')),
                default=Value('inactive'),
                output_field=models.CharField(),
            ),
            tier_rank=Case(
                When(
                    models.Q(vendor_total_points__gte=1000) & models.Q(vendor_reputation_score__gte=80),
                    then=Value(0),
                ),
                When(
                    models.Q(vendor_total_points__gte=500) & models.Q(vendor_reputation_score__gte=60),
                    then=Value(1),
                ),
                When(models.Q(vendor_total_points__gte=200), then=Value(2)),
                When(models.Q(vendor_total_points__gte=50), then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            premium_order=Case(
                When(vendor_is_premium=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            ),
        )
        
        # Filter by category
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(primary_category=category_id)
        
        # Filter by subcategory (using M2M relationship)
        # Support both 'subcategory' (singular) and 'subcategories' (plural) parameter names
        subcategory_id = self.request.query_params.get('subcategories') or self.request.query_params.get('subcategory')
        if subcategory_id is not None:
            queryset = queryset.filter(subcategories__id=subcategory_id)

        # Filter by labels (AND logic, accepts comma-separated slugs)
        label_slugs = self.request.query_params.get('labels')
        if label_slugs:
            slugs = [slug.strip() for slug in label_slugs.split(',') if slug.strip()]
            for slug in slugs:
                queryset = queryset.filter(labels__slug=slug)

        # Default ordering: premium first, then tier, then reputation/points, then recency
        queryset = queryset.order_by(
            'premium_order',
            'tier_rank',
            '-vendor_reputation_score',
            '-vendor_total_points',
            '-created_at',
        )

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
        try:
            # Handle subcategories before saving
            subcategory_ids = self._get_subcategory_ids()
            if subcategory_ids:
                # Remove subcategories from validated_data if present, we'll handle it manually
                if 'subcategories' in serializer.validated_data:
                    serializer.validated_data.pop('subcategories')
            
            product = serializer.save()
            
            # Set subcategories manually
            if subcategory_ids:
                product.subcategories.set(subcategory_ids)
            
            # Link to category request if provided
            category_request_id = self.request.data.get('category_request_id')
            if category_request_id:
                try:
                    category_request = CategoryRequest.objects.get(
                        id=category_request_id,
                        supplier__vendor=self.request.user
                    )
                    category_request.product = product
                    category_request.save()
                except CategoryRequest.DoesNotExist:
                    pass  # Category request not found or doesn't belong to user
            
            self._ensure_primary_category(product)
            self._handle_image_uploads(product)
            self._handle_features(product)
        except serializers.ValidationError:
            raise
        except Exception as e:
            raise serializers.ValidationError({
                'detail': f'خطا در ایجاد محصول: {str(e)}'
            })
    
    def perform_update(self, serializer):
        try:
            # Handle subcategories before saving
            subcategory_ids = self._get_subcategory_ids()
            if subcategory_ids:
                # Remove subcategories from validated_data if present, we'll handle it manually
                if 'subcategories' in serializer.validated_data:
                    serializer.validated_data.pop('subcategories')
            
            product = serializer.save()
            
            # Set subcategories manually
            if subcategory_ids:
                product.subcategories.set(subcategory_ids)
            
            self._ensure_primary_category(product)
            self._handle_image_uploads(product)
            self._handle_features(product)
        except serializers.ValidationError:
            raise
        except Exception as e:
            raise serializers.ValidationError({
                'detail': f'خطا در بروزرسانی محصول: {str(e)}'
            })
    
    def _get_subcategory_ids(self):
        """Extract subcategory IDs from request data"""
        subcategory_ids = []
        
        # Handle FormData - can be single value or list
        subcategories_data = self.request.data.getlist('subcategories', [])
        if not subcategories_data:
            # Try single value
            subcategory_value = self.request.data.get('subcategories')
            if subcategory_value:
                subcategories_data = [subcategory_value]
        
        for subcategory_value in subcategories_data:
            try:
                subcategory_id = int(subcategory_value)
                subcategory_ids.append(subcategory_id)
            except (ValueError, TypeError):
                # Skip invalid values
                continue
        
        return subcategory_ids if subcategory_ids else None
    
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
    
    def _handle_features(self, product):
        """Handle product features from request data"""
        # Get features from request data (can be JSON string or list)
        features_data = self.request.data.get('features', [])
        
        # If features is a string, try to parse it as JSON
        if isinstance(features_data, str):
            import json
            try:
                features_data = json.loads(features_data)
            except (json.JSONDecodeError, ValueError):
                features_data = []
        
        # Check if product has subcategories with feature templates
        subcategories = product.subcategories.all()
        templates = None
        if subcategories.exists():
            # Check if any subcategory has templates (use first subcategory for now)
            # In the future, we might support multiple subcategories with templates
            primary_subcategory = subcategories.first()
            templates = SubcategoryFeatureTemplate.objects.filter(
                subcategory=primary_subcategory
            ).order_by('sort_order', 'created_at')
            
            if templates.exists():
                # Validate against templates
                template_names = {t.feature_name: t for t in templates}
                provided_features = {}
                
                # Parse provided features
                for feature_data in features_data:
                    if isinstance(feature_data, dict):
                        name = feature_data.get('name', '').strip()
                        value = feature_data.get('value', '').strip()
                        if name:
                            provided_features[name] = value
                
                # Check for invalid feature names (not in templates)
                invalid_features = set(provided_features.keys()) - set(template_names.keys())
                if invalid_features:
                    raise serializers.ValidationError({
                        'features': f'ویژگی‌های زیر در قالب این دسته‌بندی تعریف نشده‌اند: {", ".join(invalid_features)}'
                    })
                
                # Check for missing required features
                missing_required = []
                for template in templates:
                    if template.is_required and template.feature_name not in provided_features:
                        missing_required.append(template.feature_name)
                    elif template.is_required and not provided_features.get(template.feature_name, '').strip():
                        missing_required.append(template.feature_name)
                
                if missing_required:
                    raise serializers.ValidationError({
                        'features': f'ویژگی‌های الزامی زیر باید پر شوند: {", ".join(missing_required)}'
                    })
                
                # Use template order and ensure all templates are included
                features_to_create = []
                for template in templates:
                    feature_name = template.feature_name
                    feature_value = provided_features.get(feature_name, '').strip()
                    if feature_value:  # Only create if value is provided
                        features_to_create.append({
                            'name': feature_name,
                            'value': feature_value,
                            'sort_order': template.sort_order
                        })
                
                # Delete existing features if updating
                if self.request.method in ['PUT', 'PATCH']:
                    ProductFeature.objects.filter(product=product).delete()
                
                # Create features in template order
                for feature_data in features_to_create:
                    ProductFeature.objects.create(
                        product=product,
                        name=feature_data['name'],
                        value=feature_data['value'],
                        sort_order=feature_data['sort_order']
                    )
                return  # Exit early if templates were used
        
        # No templates - use free-form feature system (backward compatibility)
        # Validate max 10 features
        if len(features_data) > 10:
            raise serializers.ValidationError({
                'features': 'حداکثر ۱۰ ویژگی برای هر محصول مجاز است'
            })
        
        # Delete existing features if updating
        if self.request.method in ['PUT', 'PATCH']:
            ProductFeature.objects.filter(product=product).delete()
        
        # Create new features
        for i, feature_data in enumerate(features_data):
            if isinstance(feature_data, dict):
                name = feature_data.get('name', '').strip()
                value = feature_data.get('value', '').strip()
                
                if name and value:  # Only create if both name and value are provided
                    ProductFeature.objects.create(
                        product=product,
                        name=name,
                        value=value,
                        sort_order=i
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
        if requested_is_active is not None and getattr(self.request.user, 'is_staff', False):
            product.is_active = str(requested_is_active).lower() in ['true', '1', 'yes', 'on']
        elif (
            product.approval_status == Product.APPROVAL_STATUS_APPROVED
            and not product.is_active
        ):
            # Reactivate by default when we can determine a primary category and product is approved
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
        comments = product.comments.filter(is_approved=True, parent=None).select_related('author', 'author__profile').prefetch_related('replies').order_by('-created_at')
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
    
    @cache_page(60 * 15)  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @cache_page(60 * 30)  # Cache for 30 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Optionally filter categories by department
        """
        queryset = Category.objects.all().select_related('linked_product_category').prefetch_related('departments', 'subcategories').order_by('sort_order', 'name')
        
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
    pagination_class = None  # Disable pagination to return all subcategories
    
    @cache_page(60 * 15)  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @cache_page(60 * 30)  # Cache for 30 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Optionally filter subcategories by category
        """
        queryset = Subcategory.objects.all().prefetch_related('categories', 'products').order_by('sort_order', 'name')
        
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
    
    @action(detail=True, methods=['get'], url_path='feature-templates')
    def feature_templates(self, request, pk=None):
        """
        Get all feature templates for this subcategory
        """
        subcategory = self.get_object()
        templates = SubcategoryFeatureTemplate.objects.filter(subcategory=subcategory).order_by('sort_order', 'created_at')
        serializer = SubcategoryFeatureTemplateSerializer(templates, many=True, context={'request': request})
        return Response(serializer.data)

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing departments.
    Supports filtering by slug.
    """
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    
    @cache_page(60 * 15)  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @cache_page(60 * 30)  # Cache for 30 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
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
        return Product.objects.filter(vendor=self.request.user).select_related('primary_category', 'supplier').prefetch_related('images', 'subcategories').order_by('-created_at')

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
        queryset = super().get_queryset().select_related('product', 'author', 'author__profile').prefetch_related('replies')
        
        # Only show approved comments to non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Set author to current user
        """
        serializer.save(author=self.request.user)

class LabelGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides read-only access to label groups for filter UI.
    """
    serializer_class = LabelGroupSerializer
    permission_classes = [AllowAny]
    
    @cache_page(60 * 15)  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @cache_page(60 * 30)  # Cache for 30 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        subcategory_id = self.request.query_params.get('subcategory')
        queryset = LabelGroup.objects.filter(is_active=True).prefetch_related('subcategories', 'labels').order_by('display_order', 'name')
        if subcategory_id:
            queryset = queryset.filter(
                models.Q(subcategories__id=subcategory_id) | models.Q(subcategories__isnull=True)
            )
        return queryset.distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['subcategory_id'] = self.request.query_params.get('subcategory')
        return context

class LabelViewSet(viewsets.ModelViewSet):
    """
    CRUD for labels + convenience endpoints for promotional/SEO labels.
    """
    queryset = Label.objects.all().order_by('display_order', 'name')
    serializer_class = LabelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['label_group__slug', 'is_promotional', 'is_seo_page', 'is_filterable', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['display_order', 'name', 'product_count']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        subcategory_id = self.request.query_params.get('subcategory')
        queryset = super().get_queryset().select_related('label_group').prefetch_related('subcategories', 'products')
        if subcategory_id:
            queryset = queryset.filter(
                models.Q(subcategories__id=subcategory_id) | models.Q(subcategories__isnull=True)
            )
        return queryset.distinct()

    @action(detail=False, methods=['get'], url_path='promotional', permission_classes=[AllowAny])
    def promotional_labels(self, request):
        queryset = self.get_queryset().filter(is_promotional=True, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='seo', permission_classes=[AllowAny])
    def seo_labels(self, request):
        queryset = self.get_queryset().filter(is_seo_page=True, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def seo_content(self, request, slug=None):
        """
        Retrieve label SEO content by slug instead of primary key.
        This method is called via custom URL route in urls.py: labels/seo-content/<slug>/
        """
        queryset = self.get_queryset()
        label = get_object_or_404(queryset, slug=slug)
        serializer = self.get_serializer(label, context={'request': request})
        return Response(serializer.data)

class LabelComboSeoPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoints for SEO landing pages defined by label combinations.
    """
    queryset = LabelComboSeoPage.objects.all().order_by('display_order', 'name')
    serializer_class = LabelComboSeoPageSerializer
    permission_classes = [AllowAny]

# --- GLOBAL SEARCH API ---

@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 5)  # Cache search results for 5 minutes
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
    ).select_related('vendor__profile', 'vendor__vendor_profile__engagement', 'primary_category').prefetch_related('subcategories')

    # Annotate gamification fields for ranking
    products = products.annotate(
        vendor_total_points=Coalesce(
            F('vendor__vendor_profile__engagement__total_points'),
            Value(0),
        ),
        vendor_reputation_score=Coalesce(
            F('vendor__vendor_profile__engagement__reputation_score'),
            Value(0.0),
            output_field=FloatField(),
        ),
        vendor_is_premium=Coalesce(
            F('vendor__profile__is_verified'),
            Value(False),
            output_field=BooleanField(),
        ),
    ).annotate(
        vendor_tier=Case(
            When(
                models.Q(vendor_total_points__gte=1000) & models.Q(vendor_reputation_score__gte=80),
                then=Value('diamond'),
            ),
            When(
                models.Q(vendor_total_points__gte=500) & models.Q(vendor_reputation_score__gte=60),
                then=Value('gold'),
            ),
            When(models.Q(vendor_total_points__gte=200), then=Value('silver')),
            When(models.Q(vendor_total_points__gte=50), then=Value('bronze')),
            default=Value('inactive'),
            output_field=models.CharField(),
        ),
        tier_rank=Case(
            When(
                models.Q(vendor_total_points__gte=1000) & models.Q(vendor_reputation_score__gte=80),
                then=Value(0),
            ),
            When(
                models.Q(vendor_total_points__gte=500) & models.Q(vendor_reputation_score__gte=60),
                then=Value(1),
            ),
            When(models.Q(vendor_total_points__gte=200), then=Value(2)),
            When(models.Q(vendor_total_points__gte=50), then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        ),
        premium_order=Case(
            When(vendor_is_premium=True, then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        ),
    ).order_by(
        'premium_order',
        'tier_rank',
        '-vendor_reputation_score',
        '-vendor_total_points',
        '-created_at',
    )[:limit]
    
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

class CategoryRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing category requests.
    Suppliers can create requests, admins can approve/reject them.
    """
    queryset = CategoryRequest.objects.all()
    serializer_class = CategoryRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'supplier']
    search_fields = ['requested_name', 'supplier__name']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if hasattr(self, 'action') and self.action in ['create', 'update', 'partial_update']:
            return CategoryRequestCreateSerializer
        return CategoryRequestSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = CategoryRequest.objects.all().select_related('supplier', 'supplier__vendor', 'product', 'reviewed_by').order_by('-created_at')
        
        # Only filter if request and user are available (not during URL registration)
        if hasattr(self, 'request') and hasattr(self.request, 'user') and self.request.user.is_authenticated:
            # Non-admin users can only see their own requests
            if not self.request.user.is_staff:
                try:
                    supplier = self.request.user.suppliers.first()
                    if supplier:
                        queryset = queryset.filter(supplier=supplier)
                    else:
                        # If no supplier, return empty queryset
                        queryset = queryset.none()
                except:
                    queryset = queryset.none()
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Override create to use the correct serializer"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        """Create category request and link to product if provided"""
        category_request = serializer.save()
        
        # Link to product if product_id is provided
        product_id = self.request.data.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id, vendor=self.request.user)
                product.category_request = category_request
                product.save()
            except Product.DoesNotExist:
                pass  # Product not found or doesn't belong to user
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Approve a category request (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can approve requests'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        category_request = self.get_object()
        category_request.status = 'approved'
        category_request.reviewed_by = request.user
        category_request.reviewed_at = timezone.now()
        category_request.save()
        
        # Create notification for supplier
        # TODO: Implement notification system
        
        serializer = self.get_serializer(category_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """Reject a category request (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can reject requests'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        category_request = self.get_object()
        admin_notes = request.data.get('admin_notes', '')
        
        category_request.status = 'rejected'
        category_request.admin_notes = admin_notes
        category_request.reviewed_by = request.user
        category_request.reviewed_at = timezone.now()
        category_request.save()
        
        # Create notification for supplier
        # TODO: Implement notification system
        
        serializer = self.get_serializer(category_request)
        return Response(serializer.data)
class SubcategoryFeatureTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing subcategory feature templates.
    Admin can create/update/delete templates.
    Sellers can view templates for their selected subcategory.
    """
    queryset = SubcategoryFeatureTemplate.objects.all().order_by('subcategory', 'sort_order', 'created_at')
    serializer_class = SubcategoryFeatureTemplateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subcategory']
    
    def get_queryset(self):
        """Filter by subcategory if provided"""
        queryset = SubcategoryFeatureTemplate.objects.all().select_related('subcategory').order_by('subcategory', 'sort_order', 'created_at')
        subcategory_id = self.request.query_params.get('subcategory', None)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        return queryset
    
    def get_permissions(self):
        """
        Admin can create/update/delete, everyone can view
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Only staff can create templates"""
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only administrators can create feature templates")
        serializer.save()
    
    def perform_update(self, serializer):
        """Only staff can update templates"""
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only administrators can update feature templates")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Only staff can delete templates"""
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only administrators can delete feature templates")
        instance.delete()

# products/serializers.py
from rest_framework import serializers
from django.db import connection
from .models import (
    Product,
    Category,
    Subcategory,
    Department,
    ProductImage,
    ProductComment,
    ProductFeature,
    Label,
    LabelGroup,
    LabelComboSeoPage,
    CategoryRequest,
)
from gamification.models import EarnedBadge
from gamification.services import GamificationService
from .utils import build_absolute_uri, log_debug
import json
import time

class SubcategoryField(serializers.Field):
    """
    Custom field for subcategories that accepts any type.
    Validation is skipped - the view will handle conversion to integers.
    """
    def __init__(self, **kwargs):
        kwargs['write_only'] = True
        kwargs['required'] = False
        kwargs['allow_null'] = True
        super().__init__(**kwargs)
    
    def get_value(self, dictionary):
        """
        Return empty to skip validation - view will handle actual values from request.data.
        This prevents DRF from trying to validate the field.
        """
        # Check if this is FormData (has getlist method)
        if hasattr(dictionary, 'getlist'):
            # For FormData, return empty to skip validation
            return serializers.empty
        # For regular dict, also return empty
        return serializers.empty
    
    def to_internal_value(self, data):
        """
        Should never be called since get_value returns empty, but if it is, return empty list
        """
        # This should never be called, but if it is, return empty list
        return []
    
    def to_representation(self, value):
        """
        Return as list of IDs for read operations (though this shouldn't be called since write_only=True)
        """
        if hasattr(value, 'all'):
            return [obj.id for obj in value.all()]
        if isinstance(value, list):
            return [obj.id if hasattr(obj, 'id') else obj for obj in value]
        return value
    
    def run_validation(self, data=serializers.empty):
        """
        Override to skip validation completely - view will handle it
        """
        if data is serializers.empty:
            return serializers.empty
        # If somehow data is provided, return empty list
        return []

class DepartmentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    og_image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'slug', 'description', 'image', 'image_url', 'image_alt_text', 
                  'og_image', 'og_image_url', 'meta_title', 'meta_description', 'canonical_url', 
                  'schema_markup', 'is_active', 'sort_order', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """Return the full URL of the image"""
        image_field = getattr(obj, 'image', None)
        if not image_field:
            return None
        
        storage = image_field.storage
        if not storage.exists(image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, image_field.url)
    
    def get_og_image_url(self, obj):
        """Return the full URL of the Open Graph image"""
        og_image_field = getattr(obj, 'og_image', None)
        if not og_image_field:
            return None
        
        storage = og_image_field.storage
        if not storage.exists(og_image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, og_image_field.url)

class CategorySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    og_image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'image_url', 'image_alt_text',
                  'og_image', 'og_image_url', 'meta_title', 'meta_description', 'canonical_url',
                  'schema_markup', 'departments', 'is_active', 'sort_order', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """Return the full URL of the image"""
        image_field = getattr(obj, 'image', None)
        if not image_field:
            return None
        
        storage = image_field.storage
        if not storage.exists(image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, image_field.url)
    
    def get_og_image_url(self, obj):
        """Return the full URL of the Open Graph image"""
        og_image_field = getattr(obj, 'og_image', None)
        if not og_image_field:
            return None
        
        storage = og_image_field.storage
        if not storage.exists(og_image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, og_image_field.url)

class SubcategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    departments = serializers.SerializerMethodField(read_only=True)  # Computed from categories
    image_url = serializers.SerializerMethodField(read_only=True)
    og_image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'description', 'image', 'image_url', 'image_alt_text',
                  'og_image', 'og_image_url', 'meta_title', 'meta_description', 'canonical_url',
                  'schema_markup', 'departments', 'categories', 'is_active', 'sort_order', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """Return the full URL of the image"""
        image_field = getattr(obj, 'image', None)
        if not image_field:
            return None
        
        storage = image_field.storage
        if not storage.exists(image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, image_field.url)
    
    def get_og_image_url(self, obj):
        """Return the full URL of the Open Graph image"""
        og_image_field = getattr(obj, 'og_image', None)
        if not og_image_field:
            return None
        
        storage = og_image_field.storage
        if not storage.exists(og_image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, og_image_field.url)
    
    def get_departments(self, obj):
        """Get departments through categories"""
        departments = obj.get_departments()
        return DepartmentSerializer(departments, many=True, context=self.context).data

class LabelSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug']

class ProductFeatureSerializer(serializers.ModelSerializer):
    """Serializer for product key features"""
    
    class Meta:
        model = ProductFeature
        fields = ['id', 'name', 'value', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'is_primary', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """Return the full URL of the image"""
        image_field = getattr(obj, 'image', None)
        if not image_field:
            return None
        
        storage = image_field.storage
        if not storage.exists(image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, image_field.url)

class LabelMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'slug', 'color', 'is_promotional', 'is_filterable', 'is_seo_page', 'is_active']

class LabelSerializer(serializers.ModelSerializer):
    label_group = serializers.StringRelatedField()
    departments = DepartmentSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    subcategories = LabelSubcategorySerializer(many=True, read_only=True)
    og_image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Label
        fields = [
            'id', 'name', 'slug', 'description', 'label_group', 'color',
            'is_promotional', 'is_filterable', 'is_seo_page',
            'departments', 'categories',
            'subcategories',
            'seo_title', 'seo_description', 'seo_h1', 'seo_intro_text',
            'seo_faq', 'og_image', 'og_image_url', 'canonical_url', 'image_alt_text',
            'schema_markup', 'product_count',
            'display_order', 'is_active', 'created_at', 'updated_at'
        ]
    
    def get_og_image_url(self, obj):
        """Return the full URL of the Open Graph image"""
        og_image_field = getattr(obj, 'og_image', None)
        if not og_image_field:
            return None
        
        storage = og_image_field.storage
        if not storage.exists(og_image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, og_image_field.url)

class LabelGroupSerializer(serializers.ModelSerializer):
    label_count = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()
    subcategories = LabelSubcategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = LabelGroup
        fields = [
            'id', 'name', 'slug', 'description', 'display_order', 'is_active',
            'label_count', 'labels', 'subcategories'
        ]

    def _filter_labels(self, obj):
        subcategory_id = self.context.get('subcategory_id')
        return obj.get_labels_for_subcategory(subcategory_id)

    def get_label_count(self, obj):
        return self._filter_labels(obj).count()

    def get_labels(self, obj):
        return LabelMinimalSerializer(
            self._filter_labels(obj),
            many=True,
            context=self.context
        ).data

class LabelComboSeoPageSerializer(serializers.ModelSerializer):
    labels = LabelMinimalSerializer(many=True, read_only=True)
    
    class Meta:
        model = LabelComboSeoPage
        fields = [
            'id', 'name', 'slug', 'labels',
            'seo_title', 'seo_description', 'seo_h1', 'seo_intro_text',
            'seo_faq', 'og_image', 'schema_markup', 'is_indexable',
            'display_order', 'created_at', 'updated_at'
        ]

class CategoryRequestSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    reviewed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CategoryRequest
        fields = [
            'id', 'supplier', 'supplier_name', 'product', 'product_name',
            'requested_name', 'status', 'admin_notes', 'reviewed_by', 'reviewed_by_name',
            'reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'admin_notes', 'reviewed_by', 'reviewed_at', 'created_at', 'updated_at']
    
    def get_reviewed_by_name(self, obj):
        """Get reviewer display name: first_name last_name"""
        if not obj.reviewed_by:
            return None
        name_parts = [obj.reviewed_by.first_name, obj.reviewed_by.last_name]
        return ' '.join(filter(None, name_parts)) or obj.reviewed_by.username
    
    def validate_requested_name(self, value):
        """Validate requested category name"""
        if not value or not value.strip():
            raise serializers.ValidationError("نام دسته‌بندی نمی‌تواند خالی باشد")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("نام دسته‌بندی باید حداقل ۲ کاراکتر باشد")
        
        return value.strip()

class CategoryRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating category requests (supplier side)"""
    
    class Meta:
        model = CategoryRequest
        fields = ['id', 'requested_name', 'product', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
        extra_kwargs = {
            'requested_name': {
                'required': True,
                'error_messages': {
                    'required': 'نام دسته‌بندی الزامی است',
                    'blank': 'نام دسته‌بندی نمی‌تواند خالی باشد'
                }
            },
            'product': {'required': False}
        }
    
    def validate_requested_name(self, value):
        """Validate requested category name"""
        if not value or not value.strip():
            raise serializers.ValidationError("نام دسته‌بندی نمی‌تواند خالی باشد")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("نام دسته‌بندی باید حداقل ۲ کاراکتر باشد")
        
        return value.strip()
    
    def create(self, validated_data):
        """Create category request and link to supplier"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        
        # Get supplier from user
        try:
            supplier = request.user.suppliers.first()
            if not supplier:
                # Try to get from vendor profile
                if hasattr(request.user, 'vendor_profile'):
                    # Create supplier from vendor profile if needed
                    from users.models import Supplier
                    supplier, _ = Supplier.objects.get_or_create(
                        vendor=request.user,
                        defaults={'name': request.user.vendor_profile.store_name}
                    )
                else:
                    raise serializers.ValidationError("شما به عنوان تأمین‌کننده ثبت نشده‌اید")
        except Exception as e:
            raise serializers.ValidationError(f"خطا در دریافت اطلاعات تأمین‌کننده: {str(e)}")
        
        validated_data['supplier'] = supplier
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    vendor_badges = serializers.SerializerMethodField()
    vendor_tier = serializers.SerializerMethodField()
    vendor_reputation_score = serializers.SerializerMethodField()
    vendor_total_points = serializers.SerializerMethodField()
    vendor_is_premium = serializers.SerializerMethodField()
    subcategory_name = serializers.SerializerMethodField()
    subcategory_details = SubcategorySerializer(source='primary_subcategory', read_only=True)
    category_name = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()
    category_path = serializers.CharField(source='get_full_category_path', read_only=True)
    breadcrumb_hierarchy = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField(read_only=True)
    og_image_url = serializers.SerializerMethodField(read_only=True)
    labels = LabelMinimalSerializer(many=True, read_only=True)
    promotional_labels = serializers.SerializerMethodField()
    category_request = serializers.SerializerMethodField(read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)
    # Override subcategories field - view will handle conversion, so we skip validation
    subcategories = SubcategoryField(write_only=True, required=False)
    
    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'subcategories', 'subcategory_name', 'subcategory_details',
            'primary_category', 'category_name', 'category_slug',
            'name', 'slug', 'description', 'price', 'stock', 'image', 'images', 'primary_image',
            'image_alt_text', 'og_image', 'og_image_url', 'meta_title', 'meta_description',
            'canonical_url', 'schema_markup', 'is_active', 'approval_status', 'is_marketplace_hidden', 'marketplace_hide_reason', 'category_path', 'breadcrumb_hierarchy',
            'labels', 'promotional_labels', 'category_request', 'availability_status', 'condition',
            'origin', 'lead_time_days', 'features',
            'vendor_badges', 'vendor_tier', 'vendor_reputation_score', 'vendor_total_points', 'vendor_is_premium',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'name': {
                'required': True,
                'error_messages': {
                    'required': 'نام محصول الزامی است',
                    'blank': 'نام محصول نمی‌تواند خالی باشد',
                    'max_length': 'نام محصول نمی‌تواند بیشتر از ۲۰۰ کاراکتر باشد'
                }
            },
            'description': {
                'required': True,
                'error_messages': {
                    'required': 'توضیحات محصول الزامی است',
                    'blank': 'توضیحات محصول نمی‌تواند خالی باشد'
                }
            },
            'price': {
                'required': True,
                'error_messages': {
                    'required': 'قیمت محصول الزامی است',
                    'invalid': 'قیمت وارد شده معتبر نیست'
                }
            },
            'stock': {
                'error_messages': {
                    'invalid': 'موجودی وارد شده معتبر نیست',
                    'min_value': 'موجودی نمی‌تواند منفی باشد'
                }
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        
        if request and request.user.is_staff:
            # Admin users can modify vendor field, but it's optional (will default to current user if not provided)
            self.Meta.read_only_fields = ['created_at', 'updated_at']
            # Make vendor field optional for admins (not required)
            if 'vendor' in self.fields:
                self.fields['vendor'].required = False
                self.fields['vendor'].allow_null = True
        else:
            # Regular users cannot modify vendor field
            self.Meta.read_only_fields = ['vendor', 'created_at', 'updated_at']
    
    def get_breadcrumb_hierarchy(self, obj):
        """Return the breadcrumb hierarchy for the product"""
        return obj.get_breadcrumb_hierarchy

    def get_vendor_name(self, obj):
        """Return supplier name or vendor fallback for safe serialization."""
        if getattr(obj, 'supplier', None) and obj.supplier.name:
            return obj.supplier.name
        full_name = obj.vendor.get_full_name()
        return full_name or obj.vendor.username

    def get_vendor_badges(self, obj):
        # #region agent log
        initial_queries = len(connection.queries)
        start_time = time.time()
        # #endregion agent log
        
        vendor = getattr(obj, 'vendor', None)
        if not vendor:
            return []

        vendor_profile = getattr(vendor, 'vendor_profile', None)
        if not vendor_profile:
            return []

        # Use prefetched badges if available, otherwise fallback to query
        if hasattr(vendor_profile, 'earned_badges'):
            badges = vendor_profile.earned_badges.all()
        else:
            badges = (
                EarnedBadge.objects.select_related('badge')
                .filter(vendor_profile=vendor_profile)
                .order_by('-achieved_at')
            )
        
        result = [
            {
                'slug': eb.badge.slug,
                'icon': eb.badge.icon,
                'title': eb.badge.title,
                'tier': eb.badge.tier,
            }
            for eb in badges
        ]
        
        # #region agent log
        queries_used = len(connection.queries) - initial_queries
        elapsed = time.time() - start_time
        log_debug(
            'debug-session',
            'post-fix',
            'C',
            'products/serializers.py:get_vendor_badges',
            'Vendor badges queried',
            {
                'product_id': obj.id,
                'queries_count': queries_used,
                'time_ms': round(elapsed * 1000, 2),
                'used_prefetch': hasattr(vendor_profile, 'earned_badges')
            }
        )
        # #endregion agent log
        
        return result

    def get_vendor_name(self, obj):
        """Return supplier name or vendor fallback for safe serialization."""
        if getattr(obj, 'supplier', None) and obj.supplier.name:
            return obj.supplier.name
        full_name = obj.vendor.get_full_name()
        return full_name or obj.vendor.username

    def _get_engagement_payload(self, obj):
        vendor = getattr(obj, 'vendor', None)
        vendor_profile = getattr(vendor, 'vendor_profile', None)
        engagement = getattr(vendor_profile, 'engagement', None) if vendor_profile else None
        return {
            'points': getattr(obj, 'vendor_total_points', None)
            if hasattr(obj, 'vendor_total_points')
            else getattr(engagement, 'total_points', 0),
            'reputation': getattr(obj, 'vendor_reputation_score', None)
            if hasattr(obj, 'vendor_reputation_score')
            else getattr(engagement, 'reputation_score', 0.0),
            'tier': getattr(obj, 'vendor_tier', None)
            if hasattr(obj, 'vendor_tier')
            else None,
            'is_premium': getattr(obj, 'vendor_is_premium', None)
            if hasattr(obj, 'vendor_is_premium')
            else getattr(getattr(vendor, 'profile', None), 'is_verified', False),
            'vendor_profile': vendor_profile,
        }

    def get_vendor_tier(self, obj):
        payload = self._get_engagement_payload(obj)
        if payload['tier']:
            return payload['tier']
        vendor_profile = payload['vendor_profile']
        if not vendor_profile:
            return 'inactive'
        service = GamificationService(vendor_profile)
        return service.calculate_tier(payload['points'] or 0, payload['reputation'] or 0)

    def get_vendor_reputation_score(self, obj):
        payload = self._get_engagement_payload(obj)
        return float(payload['reputation'] or 0.0)

    def get_vendor_total_points(self, obj):
        payload = self._get_engagement_payload(obj)
        return int(payload['points'] or 0)

    def get_vendor_is_premium(self, obj):
        payload = self._get_engagement_payload(obj)
        return bool(payload['is_premium'])

    def get_subcategory_name(self, obj):
        subcat = getattr(obj, 'primary_subcategory', None)
        return subcat.name if subcat else None

    def get_category_name(self, obj):
        category = getattr(obj, 'primary_category', None)
        return category.name if category else None

    def get_category_slug(self, obj):
        category = getattr(obj, 'primary_category', None)
        return category.slug if category else None
    
    def get_primary_image(self, obj):
        """Return the URL of the primary image"""
        import json
        import time
        log_path = '/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log'
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'products/serializers.py:591', 'message': 'ProductSerializer.get_primary_image entry', 'data': {'productId': obj.id, 'productName': obj.name}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'A'}) + '\n')
        except: pass
        # #endregion
        
        primary_img = obj.primary_image
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'products/serializers.py:595', 'message': 'ProductSerializer.get_primary_image property accessed', 'data': {'hasPrimaryImg': bool(primary_img), 'primaryImgType': type(primary_img).__name__ if primary_img else None, 'hasUrl': hasattr(primary_img, 'url') if primary_img else False}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'C'}) + '\n')
        except: pass
        # #endregion
        
        if primary_img:
            try:
                relative_url = primary_img.url if hasattr(primary_img, 'url') else None
                # #region agent log
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({'location': 'products/serializers.py:600', 'message': 'ProductSerializer.get_primary_image relative_url', 'data': {'relativeUrl': relative_url, 'hasRequest': 'request' in self.context}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'B'}) + '\n')
                except: pass
                # #endregion
                
                request = self.context.get('request')
                absolute_url = build_absolute_uri(request, relative_url)
                
                # #region agent log
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({'location': 'products/serializers.py:607', 'message': 'ProductSerializer.get_primary_image absolute_url', 'data': {'absoluteUrl': absolute_url, 'urlLength': len(absolute_url) if absolute_url else 0}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'B'}) + '\n')
                except: pass
                # #endregion
                
                return absolute_url
            except Exception as e:
                # #region agent log
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({'location': 'products/serializers.py:612', 'message': 'ProductSerializer.get_primary_image error', 'data': {'error': str(e), 'errorType': type(e).__name__}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'D'}) + '\n')
                except: pass
                # #endregion
                return None
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'products/serializers.py:618', 'message': 'ProductSerializer.get_primary_image returning None', 'data': {}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'A'}) + '\n')
        except: pass
        # #endregion
        
        return None
    
    def get_og_image_url(self, obj):
        """Return the full URL of the Open Graph image"""
        og_image_field = getattr(obj, 'og_image', None)
        if not og_image_field:
            return None
        
        storage = og_image_field.storage
        if not storage.exists(og_image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, og_image_field.url)

    def get_promotional_labels(self, obj):
        # #region agent log
        initial_queries = len(connection.queries)
        start_time = time.time()
        # #endregion agent log
        
        result = LabelMinimalSerializer(
            obj.get_promotional_labels(),
            many=True,
            context=self.context
        ).data
        
        # #region agent log
        queries_used = len(connection.queries) - initial_queries
        elapsed = time.time() - start_time
        log_debug(
            'debug-session',
            'post-fix',
            'D',
            'products/serializers.py:get_promotional_labels',
            'Promotional labels queried',
            {
                'product_id': obj.id,
                'queries_count': queries_used,
                'time_ms': round(elapsed * 1000, 2)
            }
        )
        # #endregion agent log
        
        return result
    
    def get_category_request(self, obj):
        """Return category request information if exists"""
        if hasattr(obj, 'category_request') and obj.category_request:
            return {
                'id': obj.category_request.id,
                'requested_name': obj.category_request.requested_name,
                'status': obj.category_request.status,
                'created_at': obj.category_request.created_at
            }
        return None
    
    def create(self, validated_data):
        # Remove subcategories from validated_data - it will be handled in the view
        validated_data.pop('subcategories', None)
        
        # Set the vendor to the current authenticated user, unless it's an admin specifying a different vendor
        request = self.context.get('request')
        is_staff = bool(request and request.user and request.user.is_staff)

        # Prevent sellers from forcing activation/approval values
        validated_data.pop('is_active', None)
        if not is_staff:
            validated_data.pop('approval_status', None)
            validated_data['approval_status'] = Product.APPROVAL_STATUS_PENDING
            validated_data.pop('is_marketplace_hidden', None)
            validated_data.pop('marketplace_hide_reason', None)
        else:
            validated_data.setdefault('approval_status', Product.APPROVAL_STATUS_APPROVED)

        if request and request.user and request.user.is_staff and 'vendor' in validated_data and validated_data['vendor']:
            # Admin can specify a specific vendor
            pass
        else:
            # Set vendor to current user (for both regular users and admins who didn't specify vendor)
            if request:
                validated_data['vendor'] = request.user

        # New products start inactive until approved
        validated_data['is_active'] = validated_data.get('approval_status') == Product.APPROVAL_STATUS_APPROVED
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Remove subcategories from validated_data - it will be handled in the view
        validated_data.pop('subcategories', None)
        request = self.context.get('request')
        is_staff = bool(request and request.user and request.user.is_staff)
        if not is_staff:
            validated_data.pop('is_active', None)
            validated_data.pop('approval_status', None)
            validated_data.pop('is_marketplace_hidden', None)
            validated_data.pop('marketplace_hide_reason', None)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        """
        Only show دلیل عدم نمایش to ادمین یا مالک محصول.
        """
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request else None
        is_owner = bool(user and user.is_authenticated and getattr(instance, 'vendor_id', None) == user.id)
        is_staff = bool(user and getattr(user, 'is_staff', False))
        if not (is_owner or is_staff):
            data.pop('marketplace_hide_reason', None)
        return data
    
    def validate(self, data):
        # Remove subcategories from data before validation - view will handle it
        data.pop('subcategories', None)
        
        # Check if images are being uploaded via FormData
        request = self.context.get('request')
        if request and hasattr(request, 'FILES'):
            # Count existing images + new images
            product_id = self.instance.id if self.instance else None
            if product_id:
                existing_count = ProductImage.objects.filter(product_id=product_id).count()
            else:
                existing_count = 0
            
            new_images_count = len([f for f in request.FILES.getlist('images', [])])
            total_count = existing_count + new_images_count
            
            if total_count > 20:
                raise serializers.ValidationError({
                    "images": "حداکثر ۲۰ تصویر برای هر محصول مجاز است"
                })
        
        # Validate price is positive
        if 'price' in data and data['price'] is not None:
            if data['price'] < 0:
                raise serializers.ValidationError({
                    "price": "قیمت نمی‌تواند منفی باشد"
                })
        
        # Validate stock is non-negative
        if 'stock' in data and data['stock'] is not None:
            if data['stock'] < 0:
                raise serializers.ValidationError({
                    "stock": "موجودی نمی‌تواند منفی باشد"
                })
        
        # Validate description is not empty HTML
        if 'description' in data:
            # Remove HTML tags and check if there's actual content
            import re
            clean_text = re.sub(r'<[^>]+>', '', data['description']).strip()
            if not clean_text:
                raise serializers.ValidationError({
                    "description": "توضیحات نمی‌تواند خالی باشد"
                })
        
        # Validate availability status and related fields
        availability_status = data.get('availability_status')
        if availability_status == 'in_stock':
            # Condition is required when in stock
            if 'condition' not in data or not data.get('condition'):
                raise serializers.ValidationError({
                    "condition": "وضعیت محصول (نو یا دست دوم) برای محصولات موجود در انبار الزامی است"
                })
        elif availability_status == 'made_to_order':
            # Lead time is required when made to order
            if 'lead_time_days' not in data or not data.get('lead_time_days'):
                raise serializers.ValidationError({
                    "lead_time_days": "زمان تحویل برای محصولات سفارشی الزامی است"
                })
            # Validate lead_time_days is positive
            if 'lead_time_days' in data and data['lead_time_days'] is not None:
                if data['lead_time_days'] <= 0:
                    raise serializers.ValidationError({
                        "lead_time_days": "زمان تحویل باید بیشتر از صفر باشد"
                    })
        
        return data
    
    def validate_name(self, value):
        """Validate product name"""
        if not value or not value.strip():
            raise serializers.ValidationError("نام محصول نمی‌تواند خالی باشد")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("نام محصول باید حداقل ۳ کاراکتر باشد")
        
        return value.strip()
    
    def validate_description(self, value):
        """Validate product description"""
        if not value or not value.strip():
            raise serializers.ValidationError("توضیحات محصول نمی‌تواند خالی باشد")
        
        # Remove HTML tags and check actual content
        import re
        clean_text = re.sub(r'<[^>]+>', '', value).strip()
        if not clean_text:
            raise serializers.ValidationError("توضیحات نمی‌تواند خالی باشد")
        
        if len(clean_text) < 10:
            raise serializers.ValidationError("توضیحات باید حداقل ۱۰ کاراکتر باشد")
        
        return value
    
    def validate_price(self, value):
        """Validate product price"""
        if value is None:
            raise serializers.ValidationError("قیمت محصول الزامی است")
        
        if value < 0:
            raise serializers.ValidationError("قیمت نمی‌تواند منفی باشد")
        
        if value == 0:
            raise serializers.ValidationError("قیمت نمی‌تواند صفر باشد")
        
        return value
    
    def validate_stock(self, value):
        """Validate product stock"""
        if value is not None and value < 0:
            raise serializers.ValidationError("موجودی نمی‌تواند منفی باشد")
        
        return value

class ProductCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for product comments
    """
    author_name = serializers.SerializerMethodField()
    author_email = serializers.EmailField(source='author.email', read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductComment
        fields = [
            'id', 'product', 'author', 'author_name', 'author_email',
            'content', 'rating', 'is_approved', 'parent', 'replies',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        """Get author display name: first_name last_name"""
        name_parts = [obj.author.first_name, obj.author.last_name]
        return ' '.join(filter(None, name_parts)) or obj.author.username
    
    def get_replies(self, obj):
        """Get nested replies for this comment"""
        replies = obj.replies.filter(is_approved=True).order_by('created_at')
        return ProductCommentSerializer(replies, many=True, context=self.context).data

class ProductCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating product comments
    """
    class Meta:
        model = ProductComment
        fields = ['content', 'rating', 'parent']
    
    def validate_rating(self, value):
        """Validate that rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def create(self, validated_data):
        """Set author to current user"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for individual products including comments
    """
    vendor_name = serializers.SerializerMethodField()
    vendor_badges = serializers.SerializerMethodField()
    vendor_tier = serializers.SerializerMethodField()
    vendor_reputation_score = serializers.SerializerMethodField()
    vendor_total_points = serializers.SerializerMethodField()
    vendor_is_premium = serializers.SerializerMethodField()
    subcategory_name = serializers.CharField(source='primary_subcategory.name', read_only=True)
    subcategory_details = SubcategorySerializer(source='primary_subcategory', read_only=True)
    category_name = serializers.CharField(source='primary_category.name', read_only=True)
    category_slug = serializers.CharField(source='primary_category.slug', read_only=True)
    category_path = serializers.CharField(source='get_full_category_path', read_only=True)
    breadcrumb_hierarchy = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField(read_only=True)
    og_image_url = serializers.SerializerMethodField(read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    labels = LabelMinimalSerializer(many=True, read_only=True)
    promotional_labels = serializers.SerializerMethodField()
    features = ProductFeatureSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'subcategories', 'subcategory_name', 'subcategory_details',
            'primary_category', 'category_name', 'category_slug',
            'name', 'slug', 'description', 'price', 'stock', 'image', 'images', 'primary_image',
            'image_alt_text', 'og_image', 'og_image_url', 'meta_title', 'meta_description',
            'canonical_url', 'schema_markup', 'is_active', 'approval_status', 'is_marketplace_hidden', 'marketplace_hide_reason', 'category_path', 'breadcrumb_hierarchy',
            'comments', 'comment_count', 'average_rating',
            'labels', 'promotional_labels', 'availability_status', 'condition',
            'origin', 'lead_time_days', 'features', 'vendor_badges',
            'vendor_tier', 'vendor_reputation_score', 'vendor_total_points', 'vendor_is_premium',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['vendor', 'created_at', 'updated_at']
    
    def get_breadcrumb_hierarchy(self, obj):
        """Return the breadcrumb hierarchy for the product"""
        return obj.get_breadcrumb_hierarchy
    
    def get_vendor_name(self, obj):
        """Return supplier name or vendor fallback for safe serialization."""
        if getattr(obj, 'supplier', None) and obj.supplier.name:
            return obj.supplier.name
        full_name = obj.vendor.get_full_name()
        return full_name or obj.vendor.username

    def get_vendor_badges(self, obj):
        # #region agent log
        initial_queries = len(connection.queries)
        start_time = time.time()
        # #endregion agent log
        
        vendor = getattr(obj, 'vendor', None)
        if not vendor:
            return []

        vendor_profile = getattr(vendor, 'vendor_profile', None)
        if not vendor_profile:
            return []

        # Use prefetched badges if available, otherwise fallback to query
        if hasattr(vendor_profile, 'earned_badges'):
            badges = vendor_profile.earned_badges.all()
        else:
            badges = (
                EarnedBadge.objects.select_related('badge')
                .filter(vendor_profile=vendor_profile)
                .order_by('-achieved_at')
            )
        
        result = [
            {
                'slug': eb.badge.slug,
                'icon': eb.badge.icon,
                'title': eb.badge.title,
                'tier': eb.badge.tier,
            }
            for eb in badges
        ]
        
        # #region agent log
        queries_used = len(connection.queries) - initial_queries
        elapsed = time.time() - start_time
        log_debug(
            'debug-session',
            'post-fix',
            'C',
            'products/serializers.py:ProductDetailSerializer:get_vendor_badges',
            'Vendor badges queried',
            {
                'product_id': obj.id,
                'queries_count': queries_used,
                'time_ms': round(elapsed * 1000, 2),
                'used_prefetch': hasattr(vendor_profile, 'earned_badges')
            }
        )
        # #endregion agent log
        
        return result

    def _get_engagement_payload(self, obj):
        vendor = getattr(obj, 'vendor', None)
        vendor_profile = getattr(vendor, 'vendor_profile', None)
        engagement = getattr(vendor_profile, 'engagement', None) if vendor_profile else None
        return {
            'points': getattr(obj, 'vendor_total_points', None)
            if hasattr(obj, 'vendor_total_points')
            else getattr(engagement, 'total_points', 0),
            'reputation': getattr(obj, 'vendor_reputation_score', None)
            if hasattr(obj, 'vendor_reputation_score')
            else getattr(engagement, 'reputation_score', 0.0),
            'tier': getattr(obj, 'vendor_tier', None)
            if hasattr(obj, 'vendor_tier')
            else None,
            'is_premium': getattr(obj, 'vendor_is_premium', None)
            if hasattr(obj, 'vendor_is_premium')
            else getattr(getattr(vendor, 'profile', None), 'is_verified', False),
            'vendor_profile': vendor_profile,
        }

    def get_vendor_tier(self, obj):
        payload = self._get_engagement_payload(obj)
        if payload['tier']:
            return payload['tier']
        vendor_profile = payload['vendor_profile']
        if not vendor_profile:
            return 'inactive'
        service = GamificationService(vendor_profile)
        return service.calculate_tier(payload['points'] or 0, payload['reputation'] or 0)

    def get_vendor_reputation_score(self, obj):
        payload = self._get_engagement_payload(obj)
        return float(payload['reputation'] or 0.0)

    def get_vendor_total_points(self, obj):
        payload = self._get_engagement_payload(obj)
        return int(payload['points'] or 0)

    def get_vendor_is_premium(self, obj):
        payload = self._get_engagement_payload(obj)
        return bool(payload['is_premium'])

    def get_primary_image(self, obj):
        """Return the URL of the primary image"""
        import json
        import time
        log_path = '/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log'
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'products/serializers.py:1019', 'message': 'ProductDetailSerializer.get_primary_image entry', 'data': {'productId': obj.id, 'productName': obj.name}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'A'}) + '\n')
        except: pass
        # #endregion
        
        primary_img = obj.primary_image
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'products/serializers.py:1023', 'message': 'ProductDetailSerializer.get_primary_image property accessed', 'data': {'hasPrimaryImg': bool(primary_img), 'primaryImgType': type(primary_img).__name__ if primary_img else None, 'hasUrl': hasattr(primary_img, 'url') if primary_img else False}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'C'}) + '\n')
        except: pass
        # #endregion
        
        if primary_img:
            try:
                relative_url = primary_img.url if hasattr(primary_img, 'url') else None
                # #region agent log
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({'location': 'products/serializers.py:1028', 'message': 'ProductDetailSerializer.get_primary_image relative_url', 'data': {'relativeUrl': relative_url, 'hasRequest': 'request' in self.context}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'B'}) + '\n')
                except: pass
                # #endregion
                
                request = self.context.get('request')
                absolute_url = build_absolute_uri(request, relative_url)
                
                # #region agent log
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({'location': 'products/serializers.py:1035', 'message': 'ProductDetailSerializer.get_primary_image absolute_url', 'data': {'absoluteUrl': absolute_url, 'urlLength': len(absolute_url) if absolute_url else 0}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'B'}) + '\n')
                except: pass
                # #endregion
                
                return absolute_url
            except Exception as e:
                # #region agent log
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({'location': 'products/serializers.py:1042', 'message': 'ProductDetailSerializer.get_primary_image error', 'data': {'error': str(e), 'errorType': type(e).__name__}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'D'}) + '\n')
                except: pass
                # #endregion
                return None
        
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'location': 'products/serializers.py:1048', 'message': 'ProductDetailSerializer.get_primary_image returning None', 'data': {}, 'timestamp': int(time.time() * 1000), 'sessionId': 'debug-session', 'runId': 'run1', 'hypothesisId': 'A'}) + '\n')
        except: pass
        # #endregion
        
        return None
    
    def get_og_image_url(self, obj):
        """Return the full URL of the Open Graph image"""
        og_image_field = getattr(obj, 'og_image', None)
        if not og_image_field:
            return None
        
        storage = og_image_field.storage
        if not storage.exists(og_image_field.name):
            return None
        
        request = self.context.get('request')
        return build_absolute_uri(request, og_image_field.url)

    def get_promotional_labels(self, obj):
        # #region agent log
        initial_queries = len(connection.queries)
        start_time = time.time()
        # #endregion agent log
        
        result = LabelMinimalSerializer(obj.get_promotional_labels(), many=True, context=self.context).data
        
        # #region agent log
        queries_used = len(connection.queries) - initial_queries
        elapsed = time.time() - start_time
        log_debug(
            'debug-session',
            'post-fix',
            'D',
            'products/serializers.py:ProductDetailSerializer:get_promotional_labels',
            'Promotional labels queried',
            {
                'product_id': obj.id,
                'queries_count': queries_used,
                'time_ms': round(elapsed * 1000, 2)
            }
        )
        # #endregion agent log
        
        return result
    
    def to_representation(self, instance):
        """
        Hide دلیل عدم نمایش از کاربران عمومی؛ فقط ادمین یا فروشنده می‌بینند.
        """
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request else None
        is_owner = bool(user and user.is_authenticated and getattr(instance, 'vendor_id', None) == user.id)
        is_staff = bool(user and getattr(user, 'is_staff', False))
        if not (is_owner or is_staff):
            data.pop('marketplace_hide_reason', None)
        return data
    
    def get_comment_count(self, obj):
        """Get count of approved comments"""
        # #region agent log
        initial_queries = len(connection.queries)
        start_time = time.time()
        # #endregion agent log
        
        # Use prefetched comments if available
        if hasattr(obj, 'comments'):
            approved_comments = [c for c in obj.comments.all() if c.is_approved]
            result = len(approved_comments)
        else:
            result = obj.comments.filter(is_approved=True).count()
        
        # #region agent log
        queries_used = len(connection.queries) - initial_queries
        elapsed = time.time() - start_time
        log_debug(
            'debug-session',
            'post-fix',
            'E',
            'products/serializers.py:get_comment_count',
            'Comment count queried',
            {
                'product_id': obj.id,
                'queries_count': queries_used,
                'time_ms': round(elapsed * 1000, 2),
                'used_prefetch': hasattr(obj, 'comments')
            }
        )
        # #endregion agent log
        
        return result
    
    def get_average_rating(self, obj):
        """Get average rating from approved comments"""
        # #region agent log
        initial_queries = len(connection.queries)
        start_time = time.time()
        # #endregion agent log
        
        # Use prefetched comments if available
        if hasattr(obj, 'comments'):
            approved_comments = [c for c in obj.comments.all() if c.is_approved]
            if approved_comments:
                total = sum([comment.rating for comment in approved_comments])
                result = round(total / len(approved_comments), 1)
            else:
                result = 0
        else:
            approved_comments = obj.comments.filter(is_approved=True)
            if approved_comments.exists():
                total = sum([comment.rating for comment in approved_comments])
                result = round(total / approved_comments.count(), 1)
            else:
                result = 0
        
        # #region agent log
        queries_used = len(connection.queries) - initial_queries
        elapsed = time.time() - start_time
        log_debug(
            'debug-session',
            'post-fix',
            'E',
            'products/serializers.py:get_average_rating',
            'Average rating queried',
            {
                'product_id': obj.id,
                'queries_count': queries_used,
                'time_ms': round(elapsed * 1000, 2),
                'used_prefetch': hasattr(obj, 'comments')
            }
        )
        # #endregion agent log
        
        return result
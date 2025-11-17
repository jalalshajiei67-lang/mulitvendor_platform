# products/serializers.py
from rest_framework import serializers
from .models import (
    Product,
    Category,
    Subcategory,
    Department,
    ProductImage,
    ProductComment,
    Label,
    LabelGroup,
    LabelComboSeoPage,
)
from .utils import build_absolute_uri

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
    
    class Meta:
        model = Label
        fields = [
            'id', 'name', 'slug', 'description', 'label_group', 'color',
            'is_promotional', 'is_filterable', 'is_seo_page',
            'departments', 'categories',
            'subcategories',
            'seo_title', 'seo_description', 'seo_h1', 'seo_intro_text',
            'seo_faq', 'og_image', 'schema_markup', 'product_count',
            'display_order', 'is_active', 'created_at', 'updated_at'
        ]

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

class ProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.username', read_only=True)
    subcategory_name = serializers.CharField(source='primary_subcategory.name', read_only=True)
    subcategory_details = SubcategorySerializer(source='primary_subcategory', read_only=True)
    category_name = serializers.CharField(source='primary_category.name', read_only=True)
    category_slug = serializers.CharField(source='primary_category.slug', read_only=True)
    category_path = serializers.CharField(source='get_full_category_path', read_only=True)
    breadcrumb_hierarchy = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField(read_only=True)
    og_image_url = serializers.SerializerMethodField(read_only=True)
    labels = LabelMinimalSerializer(many=True, read_only=True)
    promotional_labels = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'subcategories', 'subcategory_name', 'subcategory_details',
            'primary_category', 'category_name', 'category_slug',
            'name', 'slug', 'description', 'price', 'stock', 'image', 'images', 'primary_image',
            'image_alt_text', 'og_image', 'og_image_url', 'meta_title', 'meta_description',
            'canonical_url', 'schema_markup', 'is_active', 'category_path', 'breadcrumb_hierarchy',
            'labels', 'promotional_labels', 'created_at', 'updated_at'
        ]

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
    
    def get_primary_image(self, obj):
        """Return the URL of the primary image"""
        primary_img = obj.primary_image
        if primary_img:
            request = self.context.get('request')
            return build_absolute_uri(request, primary_img.url)
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
        return LabelMinimalSerializer(
            obj.get_promotional_labels(),
            many=True,
            context=self.context
        ).data
    
    def create(self, validated_data):
        # Set the vendor to the current authenticated user, unless it's an admin specifying a different vendor
        request = self.context.get('request')
        if request and request.user.is_staff and 'vendor' in validated_data and validated_data['vendor']:
            # Admin can specify a specific vendor
            pass
        else:
            # Set vendor to current user (for both regular users and admins who didn't specify vendor)
            validated_data['vendor'] = request.user
        return super().create(validated_data)
    
    def validate(self, data):
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
                raise serializers.ValidationError("Maximum 20 images allowed per product.")
        
        return data

class ProductCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for product comments
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
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
    vendor_name = serializers.CharField(source='vendor.username', read_only=True)
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
    
    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'subcategories', 'subcategory_name', 'subcategory_details',
            'primary_category', 'category_name', 'category_slug',
            'name', 'slug', 'description', 'price', 'stock', 'image', 'images', 'primary_image',
            'image_alt_text', 'og_image', 'og_image_url', 'meta_title', 'meta_description',
            'canonical_url', 'schema_markup', 'is_active', 'category_path', 'breadcrumb_hierarchy',
            'comments', 'comment_count', 'average_rating',
            'labels', 'promotional_labels',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['vendor', 'created_at', 'updated_at']
    
    def get_breadcrumb_hierarchy(self, obj):
        """Return the breadcrumb hierarchy for the product"""
        return obj.get_breadcrumb_hierarchy
    
    def get_primary_image(self, obj):
        """Return the URL of the primary image"""
        primary_img = obj.primary_image
        if primary_img:
            request = self.context.get('request')
            return build_absolute_uri(request, primary_img.url)
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
        return LabelMinimalSerializer(obj.get_promotional_labels(), many=True, context=self.context).data
    
    def get_comment_count(self, obj):
        """Get count of approved comments"""
        return obj.comments.filter(is_approved=True).count()
    
    def get_average_rating(self, obj):
        """Get average rating from approved comments"""
        approved_comments = obj.comments.filter(is_approved=True)
        if approved_comments.exists():
            total = sum([comment.rating for comment in approved_comments])
            return round(total / approved_comments.count(), 1)
        return 0
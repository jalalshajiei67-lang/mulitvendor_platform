# products/serializers.py
from rest_framework import serializers
from .models import Product, Category, Subcategory, Department, ProductImage, ProductComment

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'slug', 'description', 'image', 'meta_title', 'meta_description', 'is_active', 'sort_order', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'meta_title', 'meta_description', 'departments', 'is_active', 'sort_order', 'created_at', 'updated_at']

class SubcategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    departments = serializers.SerializerMethodField(read_only=True)  # Computed from categories
    
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'description', 'image', 'meta_title', 'meta_description', 'departments', 'categories', 'is_active', 'sort_order', 'created_at', 'updated_at']
    
    def get_departments(self, obj):
        """Get departments through categories"""
        departments = obj.get_departments()
        return DepartmentSerializer(departments, many=True, context=self.context).data

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'is_primary', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """Return the full URL of the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

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
    
    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'subcategories', 'subcategory_name', 'subcategory_details',
            'primary_category', 'category_name', 'category_slug',
            'name', 'slug', 'description', 'price', 'stock', 'image', 'images', 'primary_image',
            'meta_title', 'meta_description', 'is_active', 'category_path', 'breadcrumb_hierarchy',
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
            if request:
                return request.build_absolute_uri(primary_img.url)
            return primary_img.url
        return None
    
    def create(self, validated_data):
        # Set the vendor to the current authenticated user
        validated_data['vendor'] = self.context['request'].user
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
    comments = ProductCommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'subcategories', 'subcategory_name', 'subcategory_details',
            'primary_category', 'category_name', 'category_slug',
            'name', 'slug', 'description', 'price', 'stock', 'image', 'images', 'primary_image',
            'meta_title', 'meta_description', 'is_active', 'category_path', 'breadcrumb_hierarchy',
            'comments', 'comment_count', 'average_rating',
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
            if request:
                return request.build_absolute_uri(primary_img.url)
            return primary_img.url
        return None
    
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
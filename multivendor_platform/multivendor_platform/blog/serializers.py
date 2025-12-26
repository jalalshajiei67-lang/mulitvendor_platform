# blog/serializers.py
from rest_framework import serializers
from .models import BlogPost, BlogCategory, BlogComment

class BlogCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for blog categories
    """
    # Import CategorySerializer locally to avoid circular import issues
    linked_product_category = serializers.SerializerMethodField()
    linked_product_category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    linked_subcategories = serializers.SerializerMethodField()
    linked_subcategory_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_null=True
    )
    # Use annotated field if available, otherwise fall back to method field
    post_count = serializers.IntegerField(read_only=True, required=False)
    
    def get_linked_product_category(self, obj):
        """Get linked product category data safely"""
        if obj.linked_product_category:
            try:
                from products.serializers import CategorySerializer
                return CategorySerializer(obj.linked_product_category).data
            except Exception:
                # Fallback to basic data if serializer fails
                return {
                    'id': obj.linked_product_category.id,
                    'name': obj.linked_product_category.name,
                    'slug': obj.linked_product_category.slug,
                }
        return None

    def get_linked_subcategories(self, obj):
        """Get linked subcategories data"""
        try:
            from products.serializers import SubcategorySerializer
            return SubcategorySerializer(
                obj.linked_subcategories.all(),
                many=True,
                context=self.context
            ).data
        except Exception:
            # Fallback to basic data if serializer fails
            return [
                {
                    'id': sub.id,
                    'name': sub.name,
                    'slug': sub.slug,
                }
                for sub in obj.linked_subcategories.all()
            ]
    
    class Meta:
        model = BlogCategory
        fields = [
            'id', 'name', 'slug', 'description', 'color', 'is_active',
            'linked_product_category', 'linked_product_category_id',
            'linked_subcategories', 'linked_subcategory_ids',
            'post_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        subcategory_ids = validated_data.pop('linked_subcategory_ids', [])
        instance = super().create(validated_data)
        if subcategory_ids:
            instance.linked_subcategories.set(subcategory_ids)
        return instance

    def update(self, instance, validated_data):
        subcategory_ids = validated_data.pop('linked_subcategory_ids', None)
        instance = super().update(instance, validated_data)
        if subcategory_ids is not None:
            instance.linked_subcategories.set(subcategory_ids)
        return instance
    
    def to_representation(self, instance):
        """Handle both annotated and non-annotated instances"""
        data = super().to_representation(instance)
        
        # If post_count annotation is not available, use method as fallback
        if 'post_count' not in data or data['post_count'] is None:
            try:
                data['post_count'] = instance.blog_posts.filter(status='published').count()
            except Exception:
                data['post_count'] = 0
        
        return data

class BlogCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for blog comments
    """
    author_name = serializers.SerializerMethodField()
    author_email = serializers.EmailField(source='author.email', read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogComment
        fields = [
            'id', 'post', 'author', 'author_name', 'author_email',
            'content', 'is_approved', 'parent', 'replies',
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
        return BlogCommentSerializer(replies, many=True, context=self.context).data

class BlogPostListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for blog post listings
    """
    author_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    # Use annotated field if available, otherwise fall back to method field
    comment_count = serializers.IntegerField(read_only=True, required=False)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'author', 'author_name', 'category', 'category_name', 'category_color',
            'status', 'is_featured', 'view_count', 'comment_count',
            'reading_time', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at', 'published_at']
    
    def get_author_name(self, obj):
        """Get author display name: first_name last_name"""
        name_parts = [obj.author.first_name, obj.author.last_name]
        return ' '.join(filter(None, name_parts)) or obj.author.username
    
    def to_representation(self, instance):
        """Handle both annotated and non-annotated instances"""
        data = super().to_representation(instance)
        
        # If comment_count annotation is not available, use method as fallback
        if 'comment_count' not in data or data['comment_count'] is None:
            try:
                data['comment_count'] = instance.comments.filter(is_approved=True).count()
            except Exception:
                data['comment_count'] = 0
        
        return data

class BlogPostDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for individual blog posts
    """
    author_name = serializers.SerializerMethodField()
    author_email = serializers.EmailField(source='author.email', read_only=True)
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    linked_subcategories = serializers.SerializerMethodField()
    linked_subcategory_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_null=True
    )
    comments = BlogCommentSerializer(many=True, read_only=True)
    # Use annotated field if available, otherwise fall back to method field
    comment_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'author', 'author_name', 'author_email', 'category', 'category_id',
            'linked_subcategories', 'linked_subcategory_ids',
            'status', 'is_featured', 'view_count', 'comment_count',
            'reading_time', 'meta_title', 'meta_description',
            'comments', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at', 'published_at']

    def get_author_name(self, obj):
        """Get author display name: first_name last_name"""
        name_parts = [obj.author.first_name, obj.author.last_name]
        return ' '.join(filter(None, name_parts)) or obj.author.username
    
    def to_representation(self, instance):
        """Handle both annotated and non-annotated instances"""
        data = super().to_representation(instance)
        
        # If comment_count annotation is not available, use method as fallback
        if 'comment_count' not in data or data['comment_count'] is None:
            try:
                data['comment_count'] = instance.comments.filter(is_approved=True).count()
            except Exception:
                data['comment_count'] = 0
        
        return data

    def get_linked_subcategories(self, obj):
        """Get linked subcategories data"""
        try:
            from products.serializers import SubcategorySerializer
            return SubcategorySerializer(
                obj.linked_subcategories.all(),
                many=True,
                context=self.context
            ).data
        except Exception:
            # Fallback to basic data if serializer fails
            return [
                {
                    'id': sub.id,
                    'name': sub.name,
                    'slug': sub.slug,
                }
                for sub in obj.linked_subcategories.all()
            ]

    def create(self, validated_data):
        subcategory_ids = validated_data.pop('linked_subcategory_ids', [])
        instance = super().create(validated_data)
        if subcategory_ids:
            instance.linked_subcategories.set(subcategory_ids)
        return instance

    def update(self, instance, validated_data):
        subcategory_ids = validated_data.pop('linked_subcategory_ids', None)
        instance = super().update(instance, validated_data)
        if subcategory_ids is not None:
            instance.linked_subcategories.set(subcategory_ids)
        return instance

class BlogPostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating blog posts
    """
    linked_subcategory_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = BlogPost
        fields = [
            'title', 'excerpt', 'content', 'featured_image',
            'category', 'linked_subcategory_ids', 'status', 'is_featured',
            'meta_title', 'meta_description'
        ]

    def create(self, validated_data):
        subcategory_ids = validated_data.pop('linked_subcategory_ids', [])
        instance = super().create(validated_data)
        if subcategory_ids:
            instance.linked_subcategories.set(subcategory_ids)
        return instance

class BlogCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating blog comments
    """
    class Meta:
        model = BlogComment
        fields = ['content', 'parent']

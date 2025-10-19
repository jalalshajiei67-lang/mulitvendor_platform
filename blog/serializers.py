# blog/serializers.py
from rest_framework import serializers
from .models import BlogPost, BlogCategory, BlogComment
from products.serializers import CategorySerializer

class BlogCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for blog categories
    """
    linked_product_category = CategorySerializer(read_only=True)
    linked_product_category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogCategory
        fields = [
            'id', 'name', 'slug', 'description', 'color', 'is_active',
            'linked_product_category', 'linked_product_category_id',
            'post_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_post_count(self, obj):
        """Get count of published posts in this category"""
        return obj.blog_posts.filter(status='published').count()

class BlogCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for blog comments
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
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
    
    def get_replies(self, obj):
        """Get nested replies for this comment"""
        replies = obj.replies.filter(is_approved=True).order_by('created_at')
        return BlogCommentSerializer(replies, many=True, context=self.context).data

class BlogPostListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for blog post listings
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'author', 'author_name', 'category', 'category_name', 'category_color',
            'status', 'is_featured', 'view_count', 'comment_count',
            'reading_time', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at', 'published_at']
    
    def get_comment_count(self, obj):
        """Get count of approved comments"""
        return obj.comments.filter(is_approved=True).count()

class BlogPostDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for individual blog posts
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    comments = BlogCommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'author', 'author_name', 'author_email', 'category', 'category_id',
            'status', 'is_featured', 'view_count', 'comment_count',
            'reading_time', 'meta_title', 'meta_description',
            'comments', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at', 'published_at']
    
    def get_comment_count(self, obj):
        """Get count of approved comments"""
        return obj.comments.filter(is_approved=True).count()
    
    def create(self, validated_data):
        """Set author to current user"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class BlogPostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating blog posts
    """
    class Meta:
        model = BlogPost
        fields = [
            'title', 'excerpt', 'content', 'featured_image',
            'category', 'status', 'is_featured',
            'meta_title', 'meta_description'
        ]
    
    def create(self, validated_data):
        """Set author to current user"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class BlogCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating blog comments
    """
    class Meta:
        model = BlogComment
        fields = ['content', 'parent']
    
    def create(self, validated_data):
        """Set author to current user"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

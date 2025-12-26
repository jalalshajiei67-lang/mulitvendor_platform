# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from django.conf import settings

# REST Framework imports
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# Local imports
from .models import BlogPost, BlogCategory, BlogComment
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer, BlogPostCreateSerializer,
    BlogCategorySerializer, BlogCommentSerializer, BlogCommentCreateSerializer
)
from .permissions import IsAuthorOrReadOnly

class BlogPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class BlogCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for blog categories
    """
    queryset = BlogCategory.objects.filter(is_active=True).order_by('name')
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        """Get queryset with safe select_related and annotations to avoid errors"""
        try:
            return BlogCategory.objects.filter(
                is_active=True
            ).select_related(
                'linked_product_category'
            ).prefetch_related(
                'linked_subcategories'
            ).annotate(
                post_count=Count(
                    'blog_posts',
                    filter=Q(blog_posts__status='published'),
                    distinct=True
                )
            ).order_by('name')
        except Exception:
            # Fallback if select_related fails
            return BlogCategory.objects.filter(is_active=True).order_by('name')
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """
        Get all published posts in this category
        Optimized with select_related and annotations
        """
        category = self.get_object()
        posts = BlogPost.objects.filter(
            category=category,
            status='published'
        ).select_related(
            'author',
            'category'
        ).annotate(
            comment_count=Count(
                'comments',
                filter=Q(comments__is_approved=True),
                distinct=True
            )
        ).order_by('-created_at')
        
        # Apply pagination
        paginator = BlogPagination()
        page = paginator.paginate_queryset(posts, request)
        
        if page is not None:
            serializer = BlogPostListSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for blog posts
    """
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_featured', 'author']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'updated_at', 'view_count', 'title']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'list':
            return BlogPostListSerializer
        elif self.action == 'create':
            return BlogPostCreateSerializer
        return BlogPostDetailSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions and status
        Optimized with select_related and prefetch_related
        """
        queryset = BlogPost.objects.select_related(
            'author',
            'category',
            'category__linked_product_category'
        ).prefetch_related(
            'linked_subcategories',
            Prefetch(
                'comments',
                queryset=BlogComment.objects.filter(is_approved=True).select_related('author')
            )
        ).annotate(
            comment_count=Count(
                'comments',
                filter=Q(comments__is_approved=True),
                distinct=True
            )
        )
        
        # If user is not authenticated or not the author, only show published posts
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        elif self.action == 'list':
            # For list view, show published posts to everyone, drafts only to authors
            if not self.request.user.is_staff:
                queryset = queryset.filter(
                    Q(status='published') | 
                    Q(status='draft', author=self.request.user)
                )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """
        Set author to current user
        """
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a blog post and increment view count
        Optimized with select_related and prefetch_related
        """
        # Get optimized queryset
        queryset = BlogPost.objects.select_related(
            'author',
            'category',
            'category__linked_product_category'
        ).prefetch_related(
            'linked_subcategories',
            Prefetch(
                'comments',
                queryset=BlogComment.objects.filter(is_approved=True).select_related('author').prefetch_related(
                    Prefetch(
                        'replies',
                        queryset=BlogComment.objects.filter(is_approved=True).select_related('author').order_by('created_at')
                    )
                )
            )
        ).annotate(
            comment_count=Count(
                'comments',
                filter=Q(comments__is_approved=True),
                distinct=True
            )
        )
        
        instance = queryset.get(slug=kwargs['slug'])
        
        # Only increment view count for published posts
        if instance.status == 'published':
            instance.increment_view_count()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured blog posts
        Optimized with select_related and annotations
        """
        featured_posts = BlogPost.objects.filter(
            status='published', 
            is_featured=True
        ).select_related(
            'author',
            'category'
        ).annotate(
            comment_count=Count(
                'comments',
                filter=Q(comments__is_approved=True),
                distinct=True
            )
        ).order_by('-created_at')[:6]
        
        serializer = BlogPostListSerializer(featured_posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent blog posts
        Optimized with select_related and annotations
        """
        recent_posts = BlogPost.objects.filter(
            status='published'
        ).select_related(
            'author',
            'category'
        ).annotate(
            comment_count=Count(
                'comments',
                filter=Q(comments__is_approved=True),
                distinct=True
            )
        ).order_by('-created_at')[:10]
        
        serializer = BlogPostListSerializer(recent_posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Get popular blog posts (by view count)
        Optimized with select_related and annotations
        """
        popular_posts = BlogPost.objects.filter(
            status='published'
        ).select_related(
            'author',
            'category'
        ).annotate(
            comment_count=Count(
                'comments',
                filter=Q(comments__is_approved=True),
                distinct=True
            )
        ).order_by('-view_count')[:10]
        
        serializer = BlogPostListSerializer(popular_posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """
        Get related blog posts (same category, excluding current post)
        Optimized with select_related and annotations
        """
        post = self.get_object()
        related_posts = BlogPost.objects.filter(
            category=post.category,
            status='published'
        ).exclude(id=post.id).select_related(
            'author',
            'category'
        ).annotate(
            comment_count=Count(
                'comments',
                filter=Q(comments__is_approved=True),
                distinct=True
            )
        ).order_by('-created_at')[:5]
        
        serializer = BlogPostListSerializer(related_posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        """
        Retrieve approved comments for a blog post.
        Optimized with select_related and prefetch_related
        """
        post = self.get_object()
        comments_qs = BlogComment.objects.filter(post=post).select_related(
            'author'
        ).prefetch_related(
            Prefetch(
                'replies',
                queryset=BlogComment.objects.filter(is_approved=True).select_related('author').order_by('created_at')
            )
        ).order_by('-created_at')
        
        if not request.user.is_staff:
            comments_qs = comments_qs.filter(is_approved=True)
        
        serializer = BlogCommentSerializer(comments_qs, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def comment(self, request, slug=None):
        """
        Add a comment to a blog post
        """
        post = self.get_object()
        serializer = BlogCommentCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogCommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for blog comments
    """
    queryset = BlogComment.objects.all().order_by('-created_at')
    serializer_class = BlogCommentSerializer
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

class MyBlogPostsView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for user's own blog posts
    """
    serializer_class = BlogPostListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BlogPagination
    
    def get_queryset(self):
        """
        Return only the current user's blog posts
        """
        return BlogPost.objects.filter(author=self.request.user).order_by('-created_at')

# Django Template Views for Dashboard
class BlogDashboardView(LoginRequiredMixin, TemplateView):
    """
    Blog dashboard view that redirects to Nuxt frontend
    """
    template_name = 'blog/dashboard.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect to Nuxt frontend blog dashboard
        frontend_url = getattr(settings, 'SITE_URL', 'http://localhost:3000')
        return redirect(f'{frontend_url.rstrip("/")}/admin/dashboard/blog')

class BlogCategoryManageView(LoginRequiredMixin, TemplateView):
    """
    Blog category management view that redirects to Nuxt frontend
    """
    template_name = 'blog/categories.html'
    
    def get(self, request, *args, **kwargs):
        # Redirect to Nuxt frontend blog categories page
        frontend_url = getattr(settings, 'SITE_URL', 'http://localhost:3000')
        return redirect(f'{frontend_url.rstrip("/")}/admin/dashboard/blog')
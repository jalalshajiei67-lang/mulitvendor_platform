# blog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogPostViewSet, BlogCategoryViewSet, BlogCommentViewSet, 
    MyBlogPostsView, BlogDashboardView, BlogCategoryManageView
)

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet)
router.register(r'categories', BlogCategoryViewSet)
router.register(r'comments', BlogCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-posts/', MyBlogPostsView.as_view({'get': 'list'}), name='my-blog-posts'),
    
    # Dashboard URLs (redirect to Vue.js frontend)
    path('dashboard/', BlogDashboardView.as_view(), name='blog-dashboard'),
    path('categories/manage/', BlogCategoryManageView.as_view(), name='blog-category-manage'),
]

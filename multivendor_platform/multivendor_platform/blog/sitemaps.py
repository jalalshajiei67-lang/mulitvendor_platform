"""
Sitemaps for Blog app
Auto-generates sitemap.xml with all published blog posts
Automatically updates when blog posts are published, updated, or deleted
"""
from django.contrib.sitemaps import Sitemap
from .models import BlogPost


class BlogSitemap(Sitemap):
    """Sitemap for blog posts - auto-updates when posts change"""
    changefreq = "weekly"
    priority = 0.7
    limit = 50000  # Maximum URLs per sitemap (Google's limit)
    
    def items(self):
        # Auto-updates: queries database each time sitemap is accessed
        # Only includes published posts
        return BlogPost.objects.filter(status='published').order_by('-updated_at')
    
    def lastmod(self, obj):
        # Auto-updates: returns latest modification time
        return obj.updated_at
    
    def location(self, obj):
        return f'/blog/{obj.slug}'



"""
Sitemaps for Blog app
Auto-generates sitemap.xml with all published blog posts
"""
from django.contrib.sitemaps import Sitemap
from .models import BlogPost


class BlogSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = "weekly"
    priority = 0.7
    
    def items(self):
        return BlogPost.objects.filter(status='published')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return f'/blog/{obj.slug}'



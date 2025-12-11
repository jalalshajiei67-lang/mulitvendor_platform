"""
Sitemaps for Products app
Auto-generates sitemap.xml with all products, departments, categories, and subcategories
Automatically updates when database changes occur
"""
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Department, Category, Subcategory


class ProductSitemap(Sitemap):
    """Sitemap for products - auto-updates when products change"""
    changefreq = "daily"
    priority = 0.8
    limit = 50000  # Maximum URLs per sitemap (Google's limit)
    
    def items(self):
        # Auto-updates: queries database each time sitemap is accessed
        return Product.objects.filter(is_active=True, is_marketplace_hidden=False).order_by('-updated_at')
    
    def lastmod(self, obj):
        # Auto-updates: returns latest modification time
        return obj.updated_at
    
    def location(self, obj):
        return f'/products/{obj.id}'


class DepartmentSitemap(Sitemap):
    """Sitemap for departments - auto-updates when departments change"""
    changefreq = "weekly"
    priority = 0.7
    limit = 50000
    
    def items(self):
        # Auto-updates: queries database each time sitemap is accessed
        return Department.objects.all().order_by('-id')
    
    def lastmod(self, obj):
        # Auto-updates: returns latest modification time if available
        if hasattr(obj, 'updated_at'):
            return obj.updated_at
        return None
    
    def location(self, obj):
        return f'/departments/{obj.slug}'


class CategorySitemap(Sitemap):
    """Sitemap for categories - auto-updates when categories change"""
    changefreq = "weekly"
    priority = 0.6
    limit = 50000
    
    def items(self):
        # Auto-updates: queries database each time sitemap is accessed
        return Category.objects.all().order_by('-id')
    
    def lastmod(self, obj):
        # Auto-updates: returns latest modification time if available
        if hasattr(obj, 'updated_at'):
            return obj.updated_at
        return None
    
    def location(self, obj):
        return f'/categories/{obj.slug}'


class SubcategorySitemap(Sitemap):
    """Sitemap for subcategories - auto-updates when subcategories change"""
    changefreq = "weekly"
    priority = 0.5
    limit = 50000
    
    def items(self):
        # Auto-updates: queries database each time sitemap is accessed
        return Subcategory.objects.all().order_by('-id')
    
    def lastmod(self, obj):
        # Auto-updates: returns latest modification time if available
        if hasattr(obj, 'updated_at'):
            return obj.updated_at
        return None
    
    def location(self, obj):
        return f'/subcategories/{obj.slug}'


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages - auto-updates when pages are added/removed"""
    changefreq = "monthly"
    priority = 0.5
    limit = 50000
    
    def items(self):
        # Auto-updates: list can be modified to include/exclude pages
        return ['home', 'about', 'contact', 'products', 'departments', 'suppliers', 'blog', 'sitemap']
    
    def lastmod(self, item):
        # Static pages don't have modification dates
        # Could be extended to read from a database if needed
        return None
    
    def location(self, item):
        if item == 'home':
            return '/'
        return f'/{item}'



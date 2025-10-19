"""
Sitemaps for Products app
Auto-generates sitemap.xml with all products, departments, categories, and subcategories
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Department, Category, Subcategory


class ProductSitemap(Sitemap):
    """Sitemap for products"""
    changefreq = "daily"
    priority = 0.8
    
    def items(self):
        return Product.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return f'/products/{obj.id}'


class DepartmentSitemap(Sitemap):
    """Sitemap for departments"""
    changefreq = "weekly"
    priority = 0.7
    
    def items(self):
        return Department.objects.all()
    
    def location(self, obj):
        return f'/departments/{obj.slug}'


class CategorySitemap(Sitemap):
    """Sitemap for categories"""
    changefreq = "weekly"
    priority = 0.6
    
    def items(self):
        return Category.objects.all()
    
    def location(self, obj):
        return f'/categories/{obj.slug}'


class SubcategorySitemap(Sitemap):
    """Sitemap for subcategories"""
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return Subcategory.objects.all()
    
    def location(self, obj):
        return f'/subcategories/{obj.slug}'


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    changefreq = "monthly"
    priority = 0.5
    
    def items(self):
        return ['home', 'about', 'products', 'departments', 'suppliers', 'blog']
    
    def location(self, item):
        if item == 'home':
            return '/'
        return f'/{item}'



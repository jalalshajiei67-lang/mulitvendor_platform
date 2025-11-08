"""
Sitemaps for Users app (Suppliers)
Auto-generates sitemap.xml with all approved suppliers
"""
from django.contrib.sitemaps import Sitemap
from .models import VendorProfile


class SupplierSitemap(Sitemap):
    """Sitemap for suppliers/vendors"""
    changefreq = "weekly"
    priority = 0.6
    
    def items(self):
        return VendorProfile.objects.filter(is_approved=True)
    
    def lastmod(self, obj):
        return obj.user.date_joined
    
    def location(self, obj):
        return f'/suppliers/{obj.id}'



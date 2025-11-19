"""
Sitemaps for Users app (Suppliers)
Auto-generates sitemap.xml with all approved suppliers
Automatically updates when suppliers are approved or updated
"""
from django.contrib.sitemaps import Sitemap
from .models import VendorProfile


class SupplierSitemap(Sitemap):
    """Sitemap for suppliers/vendors - auto-updates when suppliers change"""
    changefreq = "weekly"
    priority = 0.6
    limit = 50000  # Maximum URLs per sitemap (Google's limit)
    
    def items(self):
        # Auto-updates: queries database each time sitemap is accessed
        # Only includes approved suppliers
        return VendorProfile.objects.filter(is_approved=True).order_by('-user__date_joined')
    
    def lastmod(self, obj):
        # Auto-updates: returns user join date or updated_at if available
        if hasattr(obj, 'updated_at') and obj.updated_at:
            return obj.updated_at
        return obj.user.date_joined
    
    def location(self, obj):
        return f'/suppliers/{obj.id}'



# multivendor_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap

# Import sitemaps
from products.sitemaps import ProductSitemap, DepartmentSitemap, CategorySitemap, SubcategorySitemap, StaticViewSitemap
from blog.sitemaps import BlogSitemap
from users.sitemaps import SupplierSitemap

# Import the new dashboard views
from products.views import HomeView, VendorDashboardView, ProductCreateView

# Define sitemaps dictionary
sitemaps = {
    'products': ProductSitemap,
    'departments': DepartmentSitemap,
    'categories': CategorySitemap,
    'subcategories': SubcategorySitemap,
    'blog': BlogSitemap,
    'suppliers': SupplierSitemap,
    'static': StaticViewSitemap,
}

def favicon_view(request):
    """Simple favicon handler to prevent 404 errors"""
    return HttpResponse(status=204)  # No content response

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page
    path('', HomeView.as_view(), name='home'),
    
    # Favicon handler
    path('favicon.ico', favicon_view, name='favicon'),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # TinyMCE
    path('tinymce/', include('tinymce.urls')),
    
    # Your API URLs
    path('api/', include('products.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),  # For suppliers and user-related endpoints
    
    # --- DASHBOARD URLS ---
    path('dashboard/', VendorDashboardView.as_view(), name='vendor-dashboard'),
    path('dashboard/create/', ProductCreateView.as_view(), name='vendor-create-product'),
    
    
    # You can add other app URLs here
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in production (when WhiteNoise is not available)
# Note: This is not ideal for high-traffic production, but works for admin files
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# multivendor_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

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

def health_check(request):
    """Health check endpoint for monitoring and debugging"""
    return HttpResponse("OK", content_type="text/plain", status=200)

def robots_txt(request):
    """Serve robots.txt file to restrict crawlers from unnecessary sections"""
    # Determine protocol (Django's request.is_secure() handles proxy headers 
    # when SECURE_PROXY_SSL_HEADER is configured in settings)
    protocol = 'https' if request.is_secure() else 'http'
    domain = request.get_host()
    
    # Build robots.txt content line by line to ensure proper formatting
    robots_lines = [
        '# robots.txt for Multivendor Platform',
        '',
        '# Allow all crawlers',
        'User-agent: *',
        '',
        '# Disallow admin panel (private administration area)',
        'Disallow: /admin/',
        '',
        '# Disallow API endpoints (not for web crawling, API access only)',
        'Disallow: /api/',
        '',
        '# Disallow vendor dashboard (private vendor area)',
        'Disallow: /dashboard/',
        '',
        '# Disallow health check endpoint (internal monitoring)',
        'Disallow: /health/',
        '',
        '# Disallow TinyMCE editor (internal admin tool)',
        'Disallow: /tinymce/',
        '',
        '# Allow sitemap for better SEO indexing',
        f'Sitemap: {protocol}://{domain}/sitemap.xml',
        ''  # Final newline
    ]
    
    robots_content = '\n'.join(robots_lines)
    
    # Create response with proper content type (HttpResponse handles encoding automatically)
    response = HttpResponse(robots_content, content_type='text/plain; charset=utf-8')
    response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    response['X-Content-Type-Options'] = 'nosniff'
    return response

@csrf_exempt
@require_http_methods(["OPTIONS"])
def cors_preflight_handler(request):
    """Explicit handler for CORS preflight OPTIONS requests"""
    response = JsonResponse({}, status=200)
    # CORS headers will be added by corsheaders middleware
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health check endpoint
    path('health/', health_check, name='health'),
    
    # Robots.txt - placed early to ensure it's matched before catch-all routes
    path('robots.txt', robots_txt, name='robots_txt'),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Favicon handler
    path('favicon.ico', favicon_view, name='favicon'),
    
    # Home page
    path('', HomeView.as_view(), name='home'),
    
    # TinyMCE
    path('tinymce/', include('tinymce.urls')),
    
    # Your API URLs
    path('api/', include('products.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),  # For suppliers and user-related endpoints
    path('api/orders/', include('orders.urls')),  # For orders and RFQ endpoints
    
    # --- DASHBOARD URLS ---
    path('dashboard/', VendorDashboardView.as_view(), name='vendor-dashboard'),
    path('dashboard/create/', ProductCreateView.as_view(), name='vendor-create-product'),
    
    
    # You can add other app URLs here
]

# Serve static and media files
if settings.DEBUG:
    # Development: Use Django's static file serving
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production: Use Django's serve view directly (works without DEBUG=True)
    from django.views.static import serve
    from django.urls import re_path
    
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

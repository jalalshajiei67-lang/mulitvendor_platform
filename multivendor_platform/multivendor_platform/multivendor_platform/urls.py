# multivendor_platform/urls.py

import re
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse, JsonResponse
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.views.static import serve as static_serve

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

FRONTEND_DIST_DIR = Path(settings.BASE_DIR).parent / 'front_end' / 'dist'
FRONTEND_ASSETS_DIR = FRONTEND_DIST_DIR / 'assets'

def favicon_view(request):
    """Simple favicon handler to prevent 404 errors"""
    return HttpResponse(status=204)  # No content response

def health_check(request):
    """Health check endpoint for monitoring and debugging"""
    return HttpResponse("OK", content_type="text/plain", status=200)

def robots_txt(request):
    """
    Serve robots.txt file to restrict crawlers from unnecessary sections.
    Auto-updates based on SITE_URL setting or request host.
    """
    # Get SITE_URL from settings, fallback to request if not configured
    site_url = getattr(settings, 'SITE_URL', '').strip()
    
    if site_url:
        # Use SITE_URL from settings (auto-updates when environment variable changes)
        # Remove trailing slash if present
        site_url = site_url.rstrip('/')
        sitemap_url = f'{site_url}/sitemap.xml'
    else:
        # Fallback to request-based URL (for development or when SITE_URL not set)
        protocol = 'https' if request.is_secure() else 'http'
        domain = request.get_host()
        sitemap_url = f'{protocol}://{domain}/sitemap.xml'
    
    # Build robots.txt content line by line to ensure proper formatting
    robots_lines = [
        '# robots.txt for Multivendor Platform',
        '# Auto-generated - Updates automatically based on SITE_URL setting',
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
        f'Sitemap: {sitemap_url}',
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

class FrontendAppView(View):
    """Serve the built Vue SPA for non-API routes."""

    index_path = Path(settings.BASE_DIR).parent / 'front_end' / 'dist' / 'index.html'

    def get(self, request, *args, **kwargs):
        if not self.index_path.exists():
            return HttpResponse(
                "Frontend build not found. Run 'npm install && npm run build' inside front_end/.",
                status=503,
                content_type='text/plain'
            )

        with self.index_path.open('r', encoding='utf-8') as index_file:
            return HttpResponse(index_file.read(), content_type='text/html')

urlpatterns = [
    re_path(r'^admin/dashboard(?:/.*)?$', FrontendAppView.as_view(), name='spa-admin-dashboard'),
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
    path('api/gamification/', include('gamification.urls')),
    path('api/pages/', include('pages.urls')),  # For static pages (About Us, Contact Us)
    path('api/chat/', include('chat.urls')),  # For chat functionality
    
    # --- DASHBOARD URLS ---
    path('dashboard/', VendorDashboardView.as_view(), name='vendor-dashboard'),
    path('dashboard/create/', ProductCreateView.as_view(), name='vendor-create-product'),
    
    # Frontend built assets
    re_path(r'^assets/(?P<path>.*)$', static_serve, {'document_root': FRONTEND_ASSETS_DIR}, name='spa-assets'),
    
    # You can add other app URLs here
]

# Serve static and media files
if settings.DEBUG:
    # Development: Use Django's static file serving
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production: Use Django's serve view directly (works without DEBUG=True)
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', static_serve, {
            'document_root': settings.STATIC_ROOT,
        }),
        re_path(r'^media/(?P<path>.*)$', static_serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

SPA_EXCLUDED_PREFIXES = (
    'api/', 'admin/', 'static/', 'media/', 'assets/', 'health/', 'sitemap.xml',
    'robots.txt', 'tinymce/', 'favicon.ico'
)
SPA_PREFIX_PATTERN = '|'.join(re.escape(prefix.rstrip('/')) for prefix in SPA_EXCLUDED_PREFIXES)

urlpatterns += [
    re_path(
        rf'^(?!({SPA_PREFIX_PATTERN})).*$',
        FrontendAppView.as_view(),
        name='spa-entry'
    ),
]

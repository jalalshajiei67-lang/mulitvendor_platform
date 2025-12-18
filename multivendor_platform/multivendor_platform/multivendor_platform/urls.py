# multivendor_platform/urls.py

import re
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.views.static import serve as static_serve
from multivendor_platform.tinymce_views import tinymce_image_upload

# Import sitemaps
from products.sitemaps import ProductSitemap, DepartmentSitemap, CategorySitemap, SubcategorySitemap, StaticViewSitemap
from blog.sitemaps import BlogSitemap
from users.sitemaps import SupplierSitemap

# Ensure custom admin app/model ordering is applied
from . import admin_ordering  # noqa: F401

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

# Frontend is now served by separate Nuxt server - no longer needed
# FRONTEND_DIST_DIR = Path(settings.BASE_DIR).parent / 'front_end' / 'dist'
# FRONTEND_ASSETS_DIR = FRONTEND_DIST_DIR / 'assets'

def favicon_view(request):
    """Simple favicon handler to prevent 404 errors"""
    return HttpResponse(status=204)  # No content response

def health_check(request):
    """Health check endpoint for monitoring and debugging"""
    return HttpResponse("OK", content_type="text/plain", status=200)

def robots_txt(request):
    """
    Serve robots.txt file to restrict crawlers from unnecessary sections.
    Blocks all indexing on backend domains (production and staging).
    Allows indexing on frontend domains (indexo.ir, www.indexo.ir, staging.indexo.ir) except admin/API.
    """
    # Get the host from the request (remove port if present)
    host_with_port = request.get_host()
    # Split to get hostname without port
    host = host_with_port.split(':')[0].lower()
    
    # Define backend domains that should be completely blocked
    # Includes both production and staging backend domains
    backend_domains = [
        # Production backend domains
        'multivendor-backend.indexo.ir',
        'api.indexo.ir',
        # Staging backend domains
        'staging-api.indexo.ir',
        'staging-backend.indexo.ir',
    ]
    
    # Check if this is the backend domain (exact match or subdomain)
    # More precise matching: exact match or subdomain (e.g., api.multivendor-backend.indexo.ir)
    is_backend_domain = False
    for backend_domain in backend_domains:
        if host == backend_domain:
            is_backend_domain = True
            break
        # Check if host is a subdomain of backend domain
        # e.g., api.multivendor-backend.indexo.ir should match multivendor-backend.indexo.ir
        if host.endswith('.' + backend_domain):
            is_backend_domain = True
            break
    
    if is_backend_domain:
        # Backend domain: Block everything
        robots_lines = [
            '# robots.txt for Multivendor Platform - Backend API',
            '# This is the backend API domain - all pages should be blocked from indexing',
            '',
            'User-agent: *',
            'Disallow: /',  # Block everything
            '',
        ]
    else:
        # Frontend domain (indexo.ir, www.indexo.ir, or any other domain): 
        # Allow most content, block only admin/API
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
            # Use host without port for sitemap URL
            domain = host
            sitemap_url = f'{protocol}://{domain}/sitemap.xml'
        
        robots_lines = [
            '# robots.txt for Multivendor Platform - Frontend Website',
            '# Allow indexing of products, categories, blog, and all public content',
            '',
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
            '',
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

def get_frontend_url(request):
    """
    Helper function to get frontend URL from settings or environment.
    Used by redirect views to redirect backend URLs to frontend.
    """
    import os
    
    # In development, always use port 3000 for frontend (Nuxt dev server)
    if settings.DEBUG:
        protocol = 'https' if request.is_secure() else 'http'
        host = request.get_host().split(':')[0]  # Get hostname without port
        return f'{protocol}://{host}:3000'
    else:
        # Production: Get frontend URL from settings or environment
        frontend_url = getattr(settings, 'FRONTEND_URL', None)
        
        # If FRONTEND_URL is not set in settings, try environment variable
        if not frontend_url:
            frontend_url = os.environ.get('FRONTEND_URL', '').strip()
        
        # If FRONTEND_URL is not set, try SITE_URL (which should point to frontend)
        if not frontend_url:
            frontend_url = getattr(settings, 'SITE_URL', '').strip()
            # Also check environment variable
            if not frontend_url:
                frontend_url = os.environ.get('SITE_URL', '').strip()
        
        # If still not set, return None (caller should handle error)
        return frontend_url.rstrip('/') if frontend_url else None

def register_redirect_view(request):
    """
    Redirect /register requests to the frontend registration page.
    This handles invitation links that point to the backend URL.
    Preserves the 'ref' query parameter for invitation codes.
    """
    frontend_url = get_frontend_url(request)
    
    if not frontend_url:
        return HttpResponse(
            "Frontend URL not configured. Please set FRONTEND_URL environment variable.",
            status=500,
            content_type='text/plain'
        )
    
    # Build redirect URL with query parameters preserved
    redirect_url = f'{frontend_url}/register'
    
    # Preserve query parameters (especially 'ref' for invitation codes)
    query_string = request.META.get('QUERY_STRING', '')
    if query_string:
        redirect_url = f'{redirect_url}?{query_string}'
    
    return redirect(redirect_url, permanent=False)

def backend_to_frontend_redirect(request, path=''):
    """
    Generic redirect view for backend URLs that should be served by frontend.
    Redirects product, category, subcategory, and department URLs to frontend.
    This prevents backend pages from being indexed by search engines.
    """
    frontend_url = get_frontend_url(request)
    
    if not frontend_url:
        return HttpResponse(
            "Frontend URL not configured. Please set FRONTEND_URL environment variable.",
            status=500,
            content_type='text/plain'
        )
    
    # Build redirect URL preserving the path
    redirect_url = f'{frontend_url}/{path}'.rstrip('/')
    
    # Preserve query parameters
    query_string = request.META.get('QUERY_STRING', '')
    if query_string:
        redirect_url = f'{redirect_url}?{query_string}'
    
    # Use 301 permanent redirect to signal search engines this is permanent
    # This helps with SEO and tells Google to update the indexed URL
    return redirect(redirect_url, permanent=True)

def product_redirect_view(request, path):
    """Redirect product URLs from backend to frontend"""
    return backend_to_frontend_redirect(request, f'products/{path}')

def category_redirect_view(request, path):
    """Redirect category URLs from backend to frontend"""
    return backend_to_frontend_redirect(request, f'categories/{path}')

def subcategory_redirect_view(request, path):
    """Redirect subcategory URLs from backend to frontend"""
    return backend_to_frontend_redirect(request, f'subcategories/{path}')

def department_redirect_view(request, path):
    """Redirect department URLs from backend to frontend"""
    return backend_to_frontend_redirect(request, f'departments/{path}')

# FrontendAppView removed - Frontend is now served by separate Nuxt server
# No longer needed since Nuxt runs as a separate service

urlpatterns = [
    # Removed old Vue dashboard route - now handled by Nuxt
    # re_path(r'^admin/dashboard(?:/.*)?$', FrontendAppView.as_view(), name='spa-admin-dashboard'),
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
    
    # Register redirect (redirects to frontend registration page)
    # This handles invitation links that may point to backend URL
    # Handle both with and without trailing slash
    path('register/', register_redirect_view, name='register-redirect'),
    path('register', register_redirect_view, name='register-redirect-no-slash'),
    
    # Redirect product/category URLs from backend to frontend
    # This prevents backend pages from being indexed by search engines
    # These routes must come BEFORE the API routes to catch these paths
    re_path(r'^products/(?P<path>.*)$', product_redirect_view, name='product-redirect'),
    re_path(r'^categories/(?P<path>.*)$', category_redirect_view, name='category-redirect'),
    re_path(r'^subcategories/(?P<path>.*)$', subcategory_redirect_view, name='subcategory-redirect'),
    re_path(r'^departments/(?P<path>.*)$', department_redirect_view, name='department-redirect'),
    
    # TinyMCE
    path('tinymce/', include('tinymce.urls')),
    # TinyMCE image upload endpoint
    path('tinymce/upload-image/', tinymce_image_upload, name='tinymce-upload-image'),
    
    # Your API URLs
    path('api/', include('products.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),  # For suppliers and user-related endpoints
    path('api/orders/', include('orders.urls')),  # For orders and RFQ endpoints
    path('api/gamification/', include('gamification.urls')),
    path('api/pages/', include('pages.urls')),  # For static pages (About Us, Contact Us)
    path('api/chat/', include('chat.urls')),  # For chat functionality
    path('api/payments/', include('payments.urls')),  # For payment processing
    path('api/auctions/', include('auctions.urls')),  # For auction system
    
    # --- DASHBOARD URLS ---
    path('dashboard/', VendorDashboardView.as_view(), name='vendor-dashboard'),
    path('dashboard/create/', ProductCreateView.as_view(), name='vendor-create-product'),
    
    # Frontend assets are now served by Nuxt server - no longer needed here
    # re_path(r'^assets/(?P<path>.*)$', static_serve, {'document_root': FRONTEND_ASSETS_DIR}, name='spa-assets'),
    
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

# Removed SPA catch-all route - Frontend is now served by separate Nuxt server
# No longer needed since Nuxt runs as a separate service on port 3000
# SPA_EXCLUDED_PREFIXES = (
#     'api/', 'admin/', 'static/', 'media/', 'assets/', 'health/', 'sitemap.xml',
#     'robots.txt', 'tinymce/', 'favicon.ico'
# )
# SPA_PREFIX_PATTERN = '|'.join(re.escape(prefix.rstrip('/')) for prefix in SPA_EXCLUDED_PREFIXES)
# 
# urlpatterns += [
#     re_path(
#         rf'^(?!({SPA_PREFIX_PATTERN})).*$',
#         FrontendAppView.as_view(),
#         name='spa-entry'
#     ),
# ]

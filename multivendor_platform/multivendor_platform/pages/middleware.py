# pages/middleware.py
"""
Middleware to handle manual redirects from the admin dashboard.
This middleware checks for redirects before other routes are processed.
"""

from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Redirect


class RedirectMiddleware:
    """
    Middleware that checks for manual redirects and applies them.
    This should be placed early in the middleware stack.
    """
    
    # Paths that should be excluded from redirect checking
    EXCLUDED_PATHS = [
        '/admin/',
        '/api/',
        '/static/',
        '/media/',
        '/robots.txt',
        '/sitemap.xml',
        '/health/',
        '/tinymce/',
        '/favicon.ico',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if this path should be excluded
        path = request.path
        
        # Skip redirect checking for excluded paths
        if any(path.startswith(excluded) for excluded in self.EXCLUDED_PATHS):
            return self.get_response(request)
        
        # Check for active redirects matching this path
        try:
            redirect_obj = Redirect.objects.filter(
                from_path=path,
                is_active=True
            ).first()
            
            if redirect_obj:
                # Get the destination URL
                to_path = redirect_obj.to_path
                
                # If it's a relative path, make it absolute
                if to_path.startswith('/'):
                    # Relative path - use current request to build absolute URL
                    protocol = 'https' if request.is_secure() else 'http'
                    host = request.get_host()
                    to_path = f'{protocol}://{host}{to_path}'
                
                # Preserve query parameters
                query_string = request.META.get('QUERY_STRING', '')
                if query_string:
                    separator = '&' if '?' in to_path else '?'
                    to_path = f'{to_path}{separator}{query_string}'
                
                # Determine redirect status code
                status_code = 301 if redirect_obj.redirect_type == '301' else 302
                
                # Perform redirect
                return redirect(to_path, permanent=(status_code == 301))
        
        except Exception:
            # If there's any error (e.g., database not ready), continue normally
            pass
        
        # No redirect found, continue with normal request processing
        return self.get_response(request)


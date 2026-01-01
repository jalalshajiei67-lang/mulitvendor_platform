"""
Middleware to exempt API routes from CSRF validation.
This ensures API endpoints work correctly without CSRF tokens.
"""
from django.utils.deprecation import MiddlewareMixin


class CsrfExemptApiMiddleware(MiddlewareMixin):
    """
    Middleware that exempts API routes from CSRF validation.
    This should be placed before CsrfViewMiddleware in the middleware stack.
    """
    
    def process_request(self, request):
        # Exempt all API routes from CSRF
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None


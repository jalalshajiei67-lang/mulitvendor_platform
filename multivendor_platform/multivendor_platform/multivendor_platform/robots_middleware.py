# multivendor_platform/robots_middleware.py
"""
Middleware to add X-Robots-Tag: noindex header to all responses from backend domains.
This prevents search engines from indexing backend API pages even if they're accessible.
"""


class BackendRobotsNoIndexMiddleware:
    """
    Middleware that adds X-Robots-Tag: noindex to all responses from backend domains.
    This ensures that backend API pages are never indexed by search engines.
    """
    
    # Backend domains that should have noindex header
    BACKEND_DOMAINS = [
        # Production backend domains
        'multivendor-backend.indexo.ir',
        'api.indexo.ir',
        # Staging backend domains
        'staging-api.indexo.ir',
        'staging-backend.indexo.ir',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Get the host from the request (remove port if present)
        host_with_port = request.get_host()
        host = host_with_port.split(':')[0].lower()
        
        # Check if this is a backend domain
        is_backend_domain = False
        for backend_domain in self.BACKEND_DOMAINS:
            if host == backend_domain:
                is_backend_domain = True
                break
            # Check if host is a subdomain of backend domain
            if host.endswith('.' + backend_domain):
                is_backend_domain = True
                break
        
        # Add X-Robots-Tag: noindex header for backend domains
        # Exception: Don't add to robots.txt itself (it needs to be readable)
        if is_backend_domain and not request.path == '/robots.txt':
            response['X-Robots-Tag'] = 'noindex, nofollow, noarchive, nosnippet'
        
        return response


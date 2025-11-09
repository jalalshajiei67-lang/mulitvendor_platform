# products/utils.py
"""
Utility functions for products app
"""
from django.conf import settings


def ensure_https_url(url):
    """
    Ensure a URL uses HTTPS protocol.
    If the URL is relative or uses HTTP, convert it to HTTPS.
    
    Args:
        url: The URL string (can be relative or absolute)
    
    Returns:
        str: URL with HTTPS protocol
    """
    if not url:
        return None
    
    # If already HTTPS, return as is
    if url.startswith('https://'):
        return url
    
    # If HTTP, replace with HTTPS
    if url.startswith('http://'):
        return url.replace('http://', 'https://', 1)
    
    # If relative URL, prepend HTTPS base URL
    if url.startswith('/'):
        # Get base URL from settings or use production backend URL
        base_url = getattr(settings, 'BASE_URL', 'https://multivendor-backend.indexo.ir')
        # Ensure base_url doesn't end with /
        base_url = base_url.rstrip('/')
        return f"{base_url}{url}"
    
    # If no protocol, assume relative and prepend HTTPS base URL
    base_url = getattr(settings, 'BASE_URL', 'https://multivendor-backend.indexo.ir')
    base_url = base_url.rstrip('/')
    return f"{base_url}/{url}"


def build_absolute_uri(request, relative_url):
    """
    Build absolute URI with HTTPS, using request if available, otherwise fallback.
    
    Args:
        request: Django request object (can be None)
        relative_url: Relative URL path
    
    Returns:
        str: Absolute HTTPS URL
    """
    if request:
        # Use request.build_absolute_uri which respects SECURE_PROXY_SSL_HEADER
        absolute_url = request.build_absolute_uri(relative_url)
        # Ensure HTTPS (in case SECURE_PROXY_SSL_HEADER is not set)
        if absolute_url.startswith('http://'):
            return absolute_url.replace('http://', 'https://', 1)
        return absolute_url
    else:
        # Fallback: build URL manually with HTTPS
        return ensure_https_url(relative_url)


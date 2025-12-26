# products/utils.py
"""
Utility functions for products app
"""
import os
import json
import time
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
    Preserves HTTP for localhost/127.0.0.1 in development.
    
    Args:
        request: Django request object (can be None)
        relative_url: Relative URL path
    
    Returns:
        str: Absolute URL (HTTPS for production, HTTP for localhost)
    """
    if request:
        # Use request.build_absolute_uri which respects SECURE_PROXY_SSL_HEADER
        absolute_url = request.build_absolute_uri(relative_url)
        # Only force HTTPS if not localhost/127.0.0.1 (for production)
        host = request.get_host()
        is_localhost = host.startswith('localhost') or host.startswith('127.0.0.1') or ':' in host and host.split(':')[0] in ['localhost', '127.0.0.1']
        
        if absolute_url.startswith('http://') and not is_localhost:
            # Only convert to HTTPS for non-localhost (production)
            return absolute_url.replace('http://', 'https://', 1)
        return absolute_url
    else:
        # Fallback: build URL manually
        # Check if we're in development (localhost)
        if 'localhost' in str(relative_url) or '127.0.0.1' in str(relative_url):
            # For localhost, use HTTP
            base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
            base_url = base_url.rstrip('/')
            if relative_url.startswith('/'):
                return f"{base_url}{relative_url}"
            return f"{base_url}/{relative_url}"
        # For production, use HTTPS
        return ensure_https_url(relative_url)


def log_debug(session_id, run_id, hypothesis_id, location, message, data=None):
    """
    Safely log debug information to file.
    Silently fails if the log file path doesn't exist (e.g., in production/Docker).
    
    Args:
        session_id: Session identifier
        run_id: Run identifier
        hypothesis_id: Hypothesis identifier
        location: Code location (e.g., 'products/serializers.py:get_promotional_labels')
        message: Log message
        data: Optional data dictionary
    """
    # Only log in development if the debug log path exists
    log_path = "/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log"
    
    try:
        # Check if the directory exists before trying to write
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            return  # Silently fail if directory doesn't exist (e.g., in Docker/production)
        
        log_entry = {
            "sessionId": session_id,
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000)
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except (OSError, IOError, PermissionError):
        # Silently fail if file doesn't exist, can't be written, or permission denied
        pass
    except Exception:
        # Silently fail on any other error
        pass


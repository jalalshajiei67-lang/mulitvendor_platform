"""
ASGI config for multivendor_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.conf import settings
from urllib.parse import urlparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns

# Custom WebSocket origin validator that allows both frontend and backend domains
class CustomOriginValidator:
    """
    Custom origin validator that allows connections from allowed hosts
    and also allows cross-subdomain connections (e.g., indexo.ir -> multivendor-backend.indexo.ir)
    """
    def __init__(self, application):
        self.application = application
        allowed_hosts_list = list(getattr(settings, 'ALLOWED_HOSTS', []))
        # Also allow common frontend domains
        allowed_hosts_list.extend(['indexo.ir', 'www.indexo.ir', 'multivendor-frontend.indexo.ir'])
        self.allowed_hosts = set(allowed_hosts_list)
        print(f"[WebSocket] Allowed hosts: {self.allowed_hosts}")
    
    async def __call__(self, scope, receive, send):
        if scope.get('type') == 'websocket':
            # Get origin from headers - headers are list of (name, value) tuples in ASGI
            origin = None
            headers = scope.get('headers', [])
            
            # Headers in ASGI are list of tuples: [(b'header-name', b'header-value'), ...]
            for header_tuple in headers:
                if isinstance(header_tuple, (list, tuple)) and len(header_tuple) >= 2:
                    header_name, header_value = header_tuple[0], header_tuple[1]
                    if header_name == b'origin':
                        try:
                            origin = header_value.decode('latin-1') if isinstance(header_value, bytes) else header_value
                            break
                        except Exception as e:
                            print(f"[WebSocket] Error decoding origin header: {e}")
                            continue
            
            if origin:
                try:
                    parsed = urlparse(origin)
                    origin_host = parsed.hostname
                    
                    print(f"[WebSocket] Connection attempt from origin: {origin} (hostname: {origin_host})")
                    
                    # Check if origin host is in allowed hosts
                    if origin_host and origin_host in self.allowed_hosts:
                        print(f"[WebSocket] Origin allowed: {origin_host}")
                        # Origin is allowed, proceed
                        return await self.application(scope, receive, send)
                    else:
                        # Log for debugging
                        print(f"[WebSocket] Origin rejected: {origin_host} (not in allowed hosts: {self.allowed_hosts})")
                        # Reject connection
                        await send({
                            'type': 'websocket.close',
                            'code': 1008,  # Policy violation
                        })
                        return
                except Exception as e:
                    print(f"[WebSocket] Error validating WebSocket origin: {e}")
                    import traceback
                    traceback.print_exc()
                    # On error, reject for security
                    await send({
                        'type': 'websocket.close',
                        'code': 1008,
                    })
                    return
            else:
                # No origin header - allow for same-origin connections
                print("[WebSocket] No origin header, allowing connection")
                return await self.application(scope, receive, send)
        
        # Not a websocket, pass through
        return await self.application(scope, receive, send)

# Configure WebSocket origin validation
# Use custom validator that allows frontend domains
websocket_application = CustomOriginValidator(
    AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": websocket_application,
})

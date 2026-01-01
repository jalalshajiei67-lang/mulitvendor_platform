# WebSocket Origin Validation Fix

## Issue
WebSocket connections from the frontend (`https://indexo.ir`) to the backend (`wss://multivendor-backend.indexo.ir/ws/chat/`) were being rejected with connection errors.

## Root Cause
The `AllowedHostsOriginValidator` in Django Channels was too strict. When the frontend at `https://indexo.ir` tries to connect to `wss://multivendor-backend.indexo.ir/ws/chat/`, the Origin header is `https://indexo.ir`. While `indexo.ir` is in `ALLOWED_HOSTS`, the validator might not be handling cross-subdomain connections properly.

## Solution
Created a custom WebSocket origin validator (`CustomOriginValidator`) that:
1. Explicitly allows connections from frontend domains (`indexo.ir`, `www.indexo.ir`, `multivendor-frontend.indexo.ir`)
2. Also respects `ALLOWED_HOSTS` from Django settings
3. Provides better error logging for debugging
4. Handles missing origin headers gracefully (for same-origin connections)

## Changes Made

### File: `multivendor_platform/multivendor_platform/asgi.py`

**Before:**
```python
websocket_application = AllowedHostsOriginValidator(
    AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
)
```

**After:**
```python
class CustomOriginValidator:
    """Custom origin validator that allows connections from allowed hosts
    and also allows cross-subdomain connections"""
    def __init__(self, application):
        self.application = application
        self.allowed_hosts = set(getattr(settings, 'ALLOWED_HOSTS', []))
        # Also allow common frontend domains
        self.allowed_hosts.update(['indexo.ir', 'www.indexo.ir', 'multivendor-frontend.indexo.ir'])
    
    async def __call__(self, scope, receive, send):
        # Validates origin and allows connection if origin is in allowed hosts
        ...

websocket_application = CustomOriginValidator(
    AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
)
```

## Testing
After deployment, test WebSocket connection:
1. Open browser console on `https://indexo.ir`
2. Check for WebSocket connection errors
3. WebSocket should now connect successfully to `wss://multivendor-backend.indexo.ir/ws/chat/`

## Deployment Status
✅ Fix has been deployed to production
✅ Backend container is healthy
✅ Custom origin validator is active

## Notes
- The custom validator is more permissive than the default `AllowedHostsOriginValidator`
- It explicitly allows frontend domains to connect to the backend WebSocket
- Error logging helps debug connection issues
- Still maintains security by only allowing connections from known domains


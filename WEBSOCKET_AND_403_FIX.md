# WebSocket and 403 Error Fix

## Issues Identified

1. **WebSocket Connection Refused**: WebSocket connections to `wss://multivendor-backend.indexo.ir/ws/chat/` were being refused
2. **403 Errors on API Endpoints**: `/api/auth/buyer/orders/` was returning 403 Forbidden

## Root Causes

### WebSocket Issues:
1. Traefik WebSocket routes were missing the `backend-headers` middleware, which is needed to properly forward headers like `X-Forwarded-Proto` and `Origin`
2. The `AllowedHostsOriginValidator` in ASGI configuration validates WebSocket origins against `ALLOWED_HOSTS`, but without proper header forwarding from Traefik, the validation might fail

### 403 Error Issues:
1. REST_FRAMEWORK had no default authentication classes configured
2. Views using `@permission_classes([IsAuthenticated])` require authentication, but without a default authentication class, DRF couldn't authenticate requests properly

## Fixes Applied

### 1. Traefik WebSocket Configuration (`docker-compose.production.yml`)
- Added `backend-headers` middleware to both WebSocket routes (`backend-ws` and `backend-ws-http`)
- This ensures proper header forwarding for WebSocket upgrade requests

```yaml
- "traefik.http.routers.backend-ws.middlewares=backend-headers"
- "traefik.http.routers.backend-ws-http.middlewares=backend-headers"
```

### 2. REST Framework Authentication (`settings.py`)
- Added `TokenAuthentication` and `SessionAuthentication` as default authentication classes
- This ensures API endpoints can properly authenticate requests using token headers

```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',  # For admin panel
],
```

### 3. ASGI Configuration (`asgi.py`)
- Improved code organization and comments
- The `AllowedHostsOriginValidator` uses `ALLOWED_HOSTS` to validate WebSocket origins
- With proper Traefik header forwarding, this should now work correctly

## Deployment Steps

1. **Update docker-compose.production.yml**:
   ```bash
   # The file has been updated with WebSocket middleware configuration
   ```

2. **Update settings.py**:
   ```bash
   # The file has been updated with default authentication classes
   ```

3. **Redeploy Backend**:
   ```bash
   ssh root@46.249.101.84
   cd /path/to/project
   docker-compose -f docker-compose.production.yml up -d --build backend
   ```

4. **Verify WebSocket Connection**:
   - Check browser console for WebSocket connection errors
   - WebSocket should now connect successfully to `wss://multivendor-backend.indexo.ir/ws/chat/`

5. **Verify API Endpoints**:
   - Test `/api/auth/buyer/orders/` with proper Authorization header
   - Should return 200 OK instead of 403 Forbidden

## Testing

### WebSocket Test:
```bash
# From browser console or using wscat
wscat -c "wss://multivendor-backend.indexo.ir/ws/chat/?token=YOUR_TOKEN"
```

### API Test:
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
     https://multivendor-backend.indexo.ir/api/auth/buyer/orders/
```

## Notes

- The CSRF middleware (`CsrfExemptApiMiddleware`) already exempts all `/api/` routes from CSRF validation
- `ALLOWED_HOSTS` includes all necessary domains: `indexo.ir`, `www.indexo.ir`, `multivendor-backend.indexo.ir`
- WebSocket origin validation uses `ALLOWED_HOSTS`, so frontend origins must match allowed hosts


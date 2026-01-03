# Short Link Fix - Summary

## Problem
Short links (e.g., `https://indexo.ir/s/notif`) were not working and returning 404 errors.

## Root Causes

### 1. Traefik Routing Configuration
The short link routes were configured to work on `${API_DOMAIN}` (multivendor-backend.indexo.ir) instead of `${MAIN_DOMAIN}` (indexo.ir). Short links need to be accessible from the main public domain.

### 2. Path Prefix Matching Issue
The Traefik rule used `PathPrefix(`/s`)` which incorrectly matched ALL paths starting with `/s`, including:
- `/seller`
- `/sw.js`
- `/static`
- `/subcategories`

This caused requests to these frontend routes to be incorrectly routed to the backend.

### 3. Relative URL Redirection
The Django view was redirecting to relative URLs (e.g., `/seller`) which stayed within the backend context instead of redirecting to the frontend domain.

### 4. Migration Error
A broken migration file (`0002_alter_suppliersmsnewsletter_mobile.py`) was preventing the backend from starting.

## Solutions

### 1. Fixed Traefik Routing Domain
Changed short link routes from:
```yaml
Host(`${API_DOMAIN}`) && PathPrefix(`/s`)
```
to:
```yaml
(Host(`${MAIN_DOMAIN}`) || Host(`www.${MAIN_DOMAIN}`)) && Path(`/s/{code:.*}`)
```

### 2. Fixed Path Matching
Used `Path(`/s/{code:.*}`)` instead of `PathPrefix(`/s`)` to match ONLY paths that start with `/s/` followed by a code, not all paths starting with `/s`.

### 3. Fixed URL Redirection
Updated `short_link_redirect` view in `pages/views.py` to convert relative URLs to absolute URLs:
```python
if target_url.startswith('/'):
    site_url = getattr(settings, 'SITE_URL', 'https://indexo.ir')
    target_url = f"{site_url.rstrip('/')}{target_url}"
```

### 4. Removed Broken Migration
Deleted the problematic migration file `0002_alter_suppliersmsnewsletter_mobile.py` that was referencing a non-existent model name.

### 5. Set Frontend Priority
Set frontend router priority to 1 (lower than short link priority of 15) to ensure specific routes are matched before the catch-all frontend route.

## Files Modified

1. `docker-compose.production.yml` - Fixed Traefik routing labels for short links
2. `multivendor_platform/multivendor_platform/pages/views.py` - Added absolute URL conversion
3. Deleted: `multivendor_platform/multivendor_platform/sms_newsletter/migrations/0002_alter_suppliersmsnewsletter_mobile.py`

## Testing

### Before Fix
```bash
curl -I https://indexo.ir/s/notif
# Result: 404 Not Found (from frontend - Nuxt)
```

### After Fix
```bash
curl -IL https://indexo.ir/s/notif
# Result: 
# 302 Redirect to https://indexo.ir/seller (from backend - daphne)
# 200 OK (from frontend - Nuxt)
```

### Verification
- ✅ `/s/notif` redirects correctly to `/seller`
- ✅ `/seller` loads from frontend (Nuxt)
- ✅ `/sw.js` loads from frontend (not intercepted by short link route)
- ✅ Click tracking is working (ShortLinkClick records created)
- ✅ Other `/s*` routes (seller, static, subcategories) work normally

## Deployment Steps

1. Updated docker-compose.production.yml
2. Copied updated files to production server
3. Rebuilt backend image (to remove broken migration)
4. Recreated backend and frontend containers with new Traefik labels
5. Verified routing in Traefik logs

## Future Recommendations

1. Always use `Path()` with parameter patterns instead of `PathPrefix()` for specific routes
2. Ensure Django redirects to absolute URLs when the target is on a different service/domain
3. Test Traefik routing changes in staging before production
4. Monitor Traefik logs for routing errors using: `docker logs traefik 2>&1 | grep -i error`

## Date
2026-01-03


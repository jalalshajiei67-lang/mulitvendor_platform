# Traefik Backend Routing Fix

## Issue Description

Traefik was returning 404 errors for both HTTP and HTTPS requests to the backend API, even though:
- Backend works when accessed directly (bypassing Traefik)
- Backend logs show 200 responses (requests reach backend sometimes)
- Backend container is running and healthy

## Root Cause

The backend router configuration was missing a **path prefix rule**, causing routing conflicts:

1. **Backend router** matched: `Host(api.indexo.ir)` - This matches ALL paths on the domain
2. **Nginx router** matched: `Host(api.indexo.ir) && (PathPrefix('/static') || PathPrefix('/media'))`
3. **Conflict**: Both routers could match requests, causing Traefik to route incorrectly

Additionally, the backend router didn't explicitly specify which paths it should handle, leading to ambiguous routing.

## Solution

### Changes Made

1. **Added PathPrefix to backend router**:
   - Changed from: `Host(\`${API_DOMAIN}\`)`
   - Changed to: `Host(\`${API_DOMAIN}\`) && PathPrefix('/api')`
   - This explicitly tells Traefik that the backend handles `/api` paths

2. **Added router priorities**:
   - Backend router: `priority=10`
   - Nginx router: `priority=20` (higher priority for static/media files)
   - This ensures nginx handles `/static` and `/media` before backend handles `/api`

### Updated Configuration

**Before:**
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.backend.rule=Host(`${API_DOMAIN}`)"
  - "traefik.http.routers.backend.entrypoints=websecure"
  - "traefik.http.routers.backend.tls.certresolver=myresolver"
  - "traefik.http.services.backend.loadbalancer.server.port=8000"
```

**After:**
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.backend.rule=Host(`${API_DOMAIN}`) && PathPrefix(`/api`)"
  - "traefik.http.routers.backend.entrypoints=websecure"
  - "traefik.http.routers.backend.tls.certresolver=myresolver"
  - "traefik.http.routers.backend.priority=10"
  - "traefik.http.services.backend.loadbalancer.server.port=8000"
```

## How to Apply the Fix

### Option 1: Using the Fix Script (Recommended)

1. **Deploy scripts to VPS:**
   ```bash
   ./deploy-traefik-fix.sh
   ```

2. **SSH to VPS:**
   ```bash
   ssh root@46.249.101.84
   ```

3. **Run diagnostics first:**
   ```bash
   ./diagnose-traefik-routing.sh
   ```

4. **Apply the fix:**
   ```bash
   # For production
   ./fix-traefik-backend.sh production
   
   # For staging
   ./fix-traefik-backend.sh staging
   ```

### Option 2: Manual Fix

1. **Update docker-compose file:**
   - Edit `docker-compose.production.yml` or `docker-compose.staging.yml`
   - Update backend labels as shown above

2. **Recreate backend container:**
   ```bash
   docker-compose -f docker-compose.production.yml up -d --no-deps backend
   ```

3. **Verify:**
   ```bash
   docker inspect multivendor_backend | grep -A 10 "traefik"
   ```

## Verification

After applying the fix:

1. **Check Traefik discovered the service:**
   ```bash
   docker exec traefik wget -qO- http://localhost:8080/api/http/services | grep backend
   ```

2. **Check router configuration:**
   ```bash
   docker exec traefik wget -qO- http://localhost:8080/api/http/routers | grep -A 5 backend
   ```

3. **Test API endpoint:**
   ```bash
   curl -k https://api.indexo.ir/api/
   ```

4. **Check Traefik logs:**
   ```bash
   docker logs traefik --tail 50
   ```

## Router Priority Explanation

Traefik evaluates routers in order of priority (higher priority first). Our configuration:

1. **Nginx (priority=20)**: Handles `/static` and `/media` paths
2. **Backend (priority=10)**: Handles `/api` paths

This ensures:
- `https://api.indexo.ir/static/...` → Nginx
- `https://api.indexo.ir/media/...` → Nginx
- `https://api.indexo.ir/api/...` → Backend

## Troubleshooting

### If 404 errors persist:

1. **Check Traefik can discover backend:**
   ```bash
   ./diagnose-traefik-routing.sh
   ```

2. **Verify network connectivity:**
   ```bash
   docker network inspect multivendor_network
   ```

3. **Check backend container labels:**
   ```bash
   docker inspect multivendor_backend | grep -A 20 "Labels"
   ```

4. **Restart Traefik (if needed):**
   ```bash
   docker restart traefik
   ```

5. **Check for multiple Traefik instances:**
   ```bash
   docker ps | grep traefik
   ```

### Common Issues

- **Backend not on same network**: Ensure backend is on `multivendor_network`
- **Traefik not watching Docker**: Check `--providers.docker=true` in Traefik command
- **Environment variables not set**: Verify `${API_DOMAIN}` is set correctly
- **Port conflicts**: Ensure backend is listening on port 8000

## Files Modified

- `docker-compose.production.yml` - Production backend router configuration
- `docker-compose.staging.yml` - Staging backend router configuration

## Scripts Created

- `diagnose-traefik-routing.sh` - Comprehensive diagnostic script
- `fix-traefik-backend.sh` - Automated fix script
- `deploy-traefik-fix.sh` - Script to deploy fix scripts to VPS


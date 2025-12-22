# 🔧 Fix API 404 Error - Docker Compose Deployment

## 🔴 Problem
Frontend is trying to call `https://api.indexo.ir/api/categories/` but getting **404 Not Found** errors.

## 🔍 Root Cause Analysis

The error occurs because:
1. Frontend is configured to use `https://api.indexo.ir/api/` (from `API_DOMAIN=api.indexo.ir` in `.env`)
2. Traefik should route `api.indexo.ir` → Backend container (port 8000)
3. But the backend might not be accessible or Traefik routing isn't working

## ✅ Solution Steps

### Step 1: Run Diagnostic Script

SSH into your VPS and run:

```bash
cd /root/indexo-production  # or wherever your project is
./diagnose-api-404.sh
```

This will check:
- Container status
- Backend health
- Traefik routing
- External API accessibility
- Environment variables

### Step 2: Verify Backend is Accessible

Test if backend responds internally:

```bash
# Test from inside backend container
docker exec multivendor_backend curl -s http://localhost:8000/api/ | head -20

# Test from inside backend container - categories endpoint
docker exec multivendor_backend curl -s http://localhost:8000/api/categories/ | head -20
```

If these fail, the backend has an issue (check backend logs).

### Step 3: Test Traefik Routing

Test if Traefik can reach the backend:

```bash
# Test from Traefik container to backend
docker exec traefik wget -qO- http://multivendor_backend:8000/api/ 2>/dev/null | head -20
```

### Step 4: Test External Access

Test from your local machine or VPS:

```bash
# Test API root
curl -k https://api.indexo.ir/api/

# Test categories endpoint
curl -k https://api.indexo.ir/api/categories/

# Check HTTP status
curl -I -k https://api.indexo.ir/api/categories/
```

### Step 5: Check Environment Variables

Verify `.env` file has correct values:

```bash
cd /root/indexo-production  # or your project directory
cat .env | grep -E "API_DOMAIN|ALLOWED_HOSTS|CORS"
```

Should see:
```
API_DOMAIN=api.indexo.ir
ALLOWED_HOSTS=...,api.indexo.ir,...
CORS_ALLOWED_ORIGINS=...,https://indexo.ir,...
```

### Step 6: Check Traefik Labels

Verify backend container has correct Traefik labels:

```bash
docker inspect multivendor_backend --format='{{range $key, $value := .Config.Labels}}{{$key}}={{$value}}{{"\n"}}{{end}}' | grep traefik
```

Should see:
```
traefik.enable=true
traefik.http.routers.backend.rule=Host(`api.indexo.ir`)
traefik.http.routers.backend.entrypoints=websecure
traefik.http.services.backend.loadbalancer.server.port=8000
```

### Step 7: Check DNS

Verify DNS is pointing to your VPS:

```bash
# On VPS
nslookup api.indexo.ir

# Should return your VPS IP: 91.107.172.234
```

### Step 8: Common Fixes

#### Fix 1: Restart Backend Container

```bash
docker-compose restart backend
docker-compose logs -f backend
```

#### Fix 2: Rebuild and Restart All Services

```bash
cd /root/indexo-production
docker-compose down
docker-compose up -d --build
docker-compose logs -f
```

#### Fix 3: Check Backend Logs for Errors

```bash
docker logs multivendor_backend --tail 50
```

Look for:
- Database connection errors
- Migration errors
- Django startup errors
- Permission errors

#### Fix 4: Verify Backend is Listening on Port 8000

```bash
docker exec multivendor_backend netstat -tlnp | grep 8000
# or
docker exec multivendor_backend ss -tlnp | grep 8000
```

Should see: `0.0.0.0:8000` or `:::8000`

#### Fix 5: Check Traefik Logs

```bash
docker logs traefik --tail 50
```

Look for:
- SSL certificate errors
- Routing errors
- Backend connection errors

#### Fix 6: Rebuild Frontend (if backend is working)

If backend is accessible at `api.indexo.ir` but frontend still fails:

```bash
# Rebuild frontend to ensure it has correct API URL
docker-compose build --no-cache frontend
docker-compose up -d frontend
docker-compose logs -f frontend
```

### Step 9: Verify Fix

After applying fixes, verify:

```bash
# 1. Backend responds internally
docker exec multivendor_backend curl -s http://localhost:8000/api/categories/ | head -5

# 2. Backend responds externally
curl -k https://api.indexo.ir/api/categories/ | head -5

# 3. Frontend can reach backend (check frontend logs)
docker logs multivendor_frontend --tail 20 | grep -i "categories\|error"
```

## 🚨 If Still Not Working

### Check Backend Django Settings

Verify `ALLOWED_HOSTS` includes `api.indexo.ir`:

```bash
docker exec multivendor_backend python manage.py shell -c "from django.conf import settings; print(settings.ALLOWED_HOSTS)"
```

### Check CORS Settings

Verify CORS allows your frontend domain:

```bash
docker exec multivendor_backend python manage.py shell -c "from django.conf import settings; print(settings.CORS_ALLOWED_ORIGINS)"
```

### Manual Test from Frontend Container

```bash
# Test API call from frontend container
docker exec multivendor_frontend curl -s https://api.indexo.ir/api/categories/ | head -5
```

If this fails, it's a network/routing issue.

## 📝 Summary

**Most Common Issues:**
1. Backend container not running or unhealthy
2. Traefik routing misconfigured
3. DNS not pointing to VPS
4. SSL certificate issues
5. Backend Django settings (ALLOWED_HOSTS, CORS)
6. Frontend built with wrong API URL

**Quick Fix Command:**
```bash
cd /root/indexo-production
docker-compose restart backend traefik
sleep 10
curl -k https://api.indexo.ir/api/categories/
```


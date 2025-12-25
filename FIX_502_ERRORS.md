# Fix 502 Bad Gateway Errors

This guide helps you diagnose and fix 502 Bad Gateway errors between nginx and the Django backend.

## 🔍 Quick Diagnosis

Run the diagnostic script to identify the issue:

```bash
./diagnose-502.sh
```

This script will check:
- Container status and health
- Network connectivity
- DNS resolution
- Nginx configuration
- Backend logs

## 🛠️ Quick Fix

If you know the issue is nginx-backend connectivity, run:

```bash
./fix-nginx-backend.sh
```

This script will:
- Get the backend container IP
- Create an improved nginx config with fallback mechanisms
- Test and reload nginx

## 🧪 Local Testing

To test the production setup locally:

```bash
./test-local-502.sh
```

This will:
1. Start services using `docker-compose.simple.yml`
2. Wait for services to be healthy
3. Run diagnostics
4. Test API endpoints
5. Attempt automatic fixes if needed

## 📋 Common Issues & Solutions

### Issue 1: DNS Resolution Failure

**Symptoms:**
- Nginx cannot resolve `backend` hostname
- 502 errors in nginx logs

**Solution:**
```bash
# Check if containers are on the same network
docker network inspect multivendor_network

# Verify service names match in docker-compose.yml
# Backend service should be named "backend"
# Nginx should use "backend:8000" in config
```

### Issue 2: Backend Not Ready

**Symptoms:**
- Backend container is running but not responding
- Health check fails

**Solution:**
```bash
# Check backend logs
docker logs multivendor_backend

# Check if backend is listening
docker exec multivendor_backend netstat -tlnp | grep 8000

# Test backend directly
docker exec multivendor_nginx wget -O- http://backend:8000/health/
```

### Issue 3: Network Isolation

**Symptoms:**
- Containers on different networks
- Cannot ping between containers

**Solution:**
```bash
# Ensure both services use the same network in docker-compose.yml
networks:
  - multivendor_network

# Restart services
docker-compose down
docker-compose up -d
```

### Issue 4: Backend Crashes

**Symptoms:**
- Backend starts then stops
- Errors in backend logs

**Solution:**
```bash
# Check backend logs for errors
docker logs multivendor_backend --tail 100

# Common issues:
# - Database connection failures
# - Missing environment variables
# - Migration errors
```

## 🔧 Manual Fix Steps

If automated scripts don't work, follow these steps:

### Step 1: Verify Backend is Running

```bash
docker ps | grep multivendor_backend
docker logs multivendor_backend --tail 50
```

### Step 2: Test Backend Directly

```bash
# From host
curl http://localhost:8000/health/

# From nginx container
docker exec multivendor_nginx wget -O- http://backend:8000/health/
```

### Step 3: Check Network Connectivity

```bash
# Get backend IP
BACKEND_IP=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' multivendor_backend)

# Test from nginx
docker exec multivendor_nginx wget -O- http://$BACKEND_IP:8000/health/
```

### Step 4: Update Nginx Config

If DNS fails, use IP address as fallback:

```nginx
upstream backend {
    server backend:8000 max_fails=3 fail_timeout=30s;
    server <BACKEND_IP>:8000 backup;  # Replace <BACKEND_IP> with actual IP
}
```

Then reload nginx:
```bash
docker exec multivendor_nginx nginx -t
docker exec multivendor_nginx nginx -s reload
```

## 📝 Production Deployment

For production (CapRover), the issue is usually:

1. **Service name mismatch**: CapRover uses container names, not service names
2. **Network isolation**: Services not on the same network
3. **Backend not ready**: Backend takes longer to start than nginx expects

### CapRover Specific Fix

```bash
# SSH to your VPS
ssh root@185.208.172.76

# Check container names
docker ps

# Update nginx config to use container name instead of service name
# If backend container is "multivendor_backend", use:
# server multivendor_backend:8000;
```

## 🎯 Verification

After applying fixes, verify:

```bash
# Test API endpoint
curl http://localhost/api/health/

# Check nginx logs
docker logs multivendor_nginx --tail 20

# Check backend logs
docker logs multivendor_backend --tail 20
```

## 📚 Related Files

- `nginx/nginx-simple.conf` - Simple nginx config for local testing
- `nginx/nginx-improved.conf` - Improved config with better error handling
- `nginx/nginx.conf` - Production config with HTTPS
- `docker-compose.simple.yml` - Local test setup
- `docker-compose.production.yml` - Production setup

## 🆘 Still Having Issues?

1. Check all container logs: `docker-compose logs`
2. Verify environment variables: `docker exec multivendor_backend env | grep DB`
3. Test database connection: `docker exec multivendor_backend python manage.py check --database default`
4. Check nginx error logs: `docker exec multivendor_nginx cat /var/log/nginx/error.log`


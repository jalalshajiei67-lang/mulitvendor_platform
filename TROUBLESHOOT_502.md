# Troubleshooting 502 Bad Gateway Error

## Quick Diagnosis Steps

### 1. Check Backend App Status in CapRover

1. Go to CapRover Dashboard → Apps → `multivendor-backend`
2. Check if the app is **Running** (green status)
3. If not running, check **App Logs** for errors

### 2. Check App Logs

In CapRover Dashboard:
- Go to your backend app → **App Logs**
- Look for:
  - Database connection errors
  - Migration errors
  - Collectstatic errors
  - Gunicorn startup errors
  - Import errors

### 3. Common Issues and Solutions

#### Issue 1: Database Connection Failed

**Symptoms:**
- Logs show: `could not connect to server`
- Logs show: `FATAL: password authentication failed`

**Solution:**
1. Check database credentials in CapRover App Config → Environment Variables
2. Verify database service name: `srv-captain--postgres-db`
3. Ensure database is running: CapRover → One-Click Apps → PostgreSQL

#### Issue 2: Migration Failed

**Symptoms:**
- Logs show: `django.db.utils.OperationalError`
- Logs show migration errors

**Solution:**
1. Check database connection first
2. Run migrations manually if needed
3. Check if database exists

#### Issue 3: Collectstatic Failed

**Symptoms:**
- Logs show: `ImproperlyConfigured`
- Logs show permission errors

**Solution:**
1. Check if STATIC_ROOT is set correctly
2. Verify persistent directories are mounted
3. Check file permissions

#### Issue 4: Port Not Exposed Correctly

**Symptoms:**
- App appears running but 502 error
- No connection errors in logs

**Solution:**
1. Verify Dockerfile has `EXPOSE 80`
2. Check CapRover HTTP Settings → Port Mapping
3. Ensure gunicorn binds to `0.0.0.0:80`

#### Issue 5: Container Crashes Immediately

**Symptoms:**
- App status shows "Restarting" or "Stopped"
- Logs show immediate crash

**Solution:**
1. Check startup command syntax
2. Verify all dependencies installed
3. Check Python/Django version compatibility

## Manual Diagnosis Commands

### Check Container Status (SSH to VPS)

```bash
ssh root@185.208.172.76
docker ps -a | grep multivendor-backend
```

### Check Container Logs

```bash
# Via CapRover Dashboard (recommended)
# Or via SSH:
docker logs srv-captain--multivendor-backend --tail 100
```

### Check Database Connection

```bash
# SSH to VPS, then exec into backend container:
docker exec -it srv-captain--multivendor-backend bash
python manage.py check --database default
```

### Test Gunicorn Directly

```bash
# Inside backend container:
gunicorn multivendor_platform.wsgi:application --bind 0.0.0.0:80 --workers 1
```

## Quick Fixes

### Fix 1: Restart Backend App

1. CapRover Dashboard → Apps → `multivendor-backend`
2. Click **"Save & Restart"**

### Fix 2: Check Environment Variables

Verify these are set in CapRover App Config:
- `DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover`
- `DB_HOST=srv-captain--postgres-db`
- `DB_NAME=multivendor_db`
- `DB_USER=postgres`
- `DB_PASSWORD=your-password`
- `SECRET_KEY=your-secret-key`
- `ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir`

### Fix 3: Verify Database Service

1. CapRover → One-Click Apps/Databases
2. Check if PostgreSQL is running
3. Verify database name matches your config

### Fix 4: Check HTTP Settings

1. Backend App → HTTP Settings
2. Ensure HTTPS is enabled
3. Check domain is set correctly
4. Verify no custom port mapping conflicts

## Emergency Fix: Simplified Startup

If the issue persists, try a simplified startup script that handles errors better:

See `Dockerfile.backend.emergency` for a version with better error handling.

## Next Steps After Fix

1. ✅ Verify app is running (green status)
2. ✅ Check logs for successful startup message
3. ✅ Test endpoint: `https://multivendor-backend.indexo.ir/api/departments/`
4. ✅ Verify database connection works
5. ✅ Check static files are collected






# Debug Backend Container Crash (0/1)

## 🚨 Problem

Backend container shows `0/1` (crashed), causing 502 errors:
- Container: `srv-captain--multivendor-backend` → `replicated 0/1`
- 502 Bad Gateway when accessing static files
- Container keeps crashing on startup

## 🔍 Diagnosis Steps

### Step 1: Check Container Logs

**Via CapRover Dashboard:**
1. Go to CapRover Dashboard → `multivendor-backend` app
2. Click **"App Logs"** tab
3. Look for error messages

**Via SSH:**
```bash
ssh root@185.208.172.76

# Find the container ID
docker ps -a | grep multivendor-backend

# Check logs (replace CONTAINER_ID with actual ID)
docker logs srv-captain--multivendor-backend.1.<container-id> --tail 200
```

### Step 2: Check Build Logs

**Via CapRover Dashboard:**
1. Go to Backend App → **"Build Logs"** or **"Deployment Logs"**
2. Look for build errors or deployment failures

### Step 3: Check for Common Issues

Look for these errors in logs:

#### Issue 1: Volume Mount Error
```
Error: invalid mount config
Error: path /captain/data/backend-static is not absolute
```
**Fix:** Verify host paths are correct in CapRover

#### Issue 2: Permission Error
```
Permission denied
Cannot access /app/staticfiles
```
**Fix:** CapRover should handle permissions, but check if directories exist

#### Issue 3: Python Import Error
```
ModuleNotFoundError: No module named '...'
ImportError: ...
```
**Fix:** Check requirements.txt and dependencies

#### Issue 4: Database Connection Error
```
could not connect to server
FATAL: password authentication failed
```
**Fix:** Check database environment variables

#### Issue 5: Settings Import Error
```
ModuleNotFoundError: No module named 'multivendor_platform.settings_caprover'
```
**Fix:** Verify DJANGO_SETTINGS_MODULE environment variable

## 🔧 Quick Fixes

### Fix 1: Restart Container

1. Go to CapRover Dashboard → Backend App
2. Click **"Save & Restart"**
3. Wait 2-3 minutes
4. Check logs again

### Fix 2: Check Environment Variables

In CapRover Dashboard → Backend App → App Configs → Environment Variables:

**Required variables:**
```env
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
```

### Fix 3: Temporarily Remove Persistent Volumes

If persistent volumes are causing the crash:

1. Go to CapRover Dashboard → Backend App → App Configs
2. **Remove** persistent directories temporarily
3. Click **"Save & Update"**
4. Check if container starts
5. If it starts, add persistent volumes back one at a time

### Fix 4: Check Disk Space

```bash
ssh root@185.208.172.76
df -h
```

If disk is full, clean up:
```bash
docker system prune -a
```

## 📋 Diagnostic Commands

Run these commands to gather information:

```bash
# 1. Check container status
docker ps -a | grep multivendor-backend

# 2. Check container logs
docker logs srv-captain--multivendor-backend.1.<container-id> --tail 200

# 3. Check if volumes are mounted
docker inspect srv-captain--multivendor-backend.1.<container-id> | grep -A 20 "Mounts"

# 4. Check if host directories exist
ls -la /captain/data/backend-static
ls -la /captain/data/backend-media

# 5. Check container exit code
docker inspect srv-captain--multivendor-backend.1.<container-id> | grep -A 10 "State"

# 6. Try to start container manually (if possible)
docker start srv-captain--multivendor-backend.1.<container-id>
docker logs -f srv-captain--multivendor-backend.1.<container-id>
```

## 🎯 Most Likely Causes

Based on the symptoms:

1. **Volume mount conflict** (most likely)
   - Both volumes pointing to same path (you fixed this)
   - Path doesn't exist or has wrong permissions

2. **Python/Django error**
   - Import error
   - Settings error
   - Database connection error

3. **Startup script error**
   - collectstatic failing
   - migrate failing
   - Gunicorn failing to start

## 📝 Next Steps

1. **Get the logs** (most important!)
   - Share the error messages from container logs
   - This will tell us exactly why it's crashing

2. **Check the most recent deployment**
   - Did it work before adding persistent volumes?
   - What changed?

3. **Try removing persistent volumes temporarily**
   - If container starts without volumes, the issue is volume-related
   - If it still crashes, the issue is in code/config

---

**Action Required**: Share the container logs so we can identify the exact error!


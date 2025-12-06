# 🚀 Deploy Chat System NOW - Quick Guide

## Current Setup Status

✅ **You Have:**
- PostgreSQL database (`postgres-db`)
- Redis server (`multivendor-redis`) with password
- Backend app (`multivendor-backend`)

❌ **You Need to Add:**
- Redis configuration to backend
- Frontend app
- Update some environment variables

---

## Step 1: Update Backend Environment Variables

### Go to: CapRover → Apps → multivendor-backend → App Configs

**Add these NEW variables:**

```env
REDIS_HOST=srv-captain--multivendor-redis
REDIS_PORT=6379
REDIS_PASSWORD=strongPassword*67
CSRF_TRUSTED_ORIGINS=https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir
USE_TLS=True
SITE_URL=https://indexo.ir
```

**Fix this variable** (change underscore to dash):

```env
DB_NAME=multivendor-db
```

Click **Save & Update** → Backend will restart automatically

---

## Step 2: Create Frontend App

### A. Create the App

1. **CapRover → Apps → Create New App**
2. **App Name:** `multivendor-frontend`
3. **Has Persistent Data:** NO
4. Click **Create New App**

### B. Configure Frontend

1. Go to **HTTP Settings** tab
2. ✅ Enable **HTTPS**
3. Add custom domains:
   - `indexo.ir`
   - `www.indexo.ir`

### C. Add Environment Variables

Go to **App Configs** tab, add:

```env
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://indexo.ir
NUXT_HOST=0.0.0.0
NUXT_PORT=3000
```

Click **Save & Update**

### D. Enable App Token (for GitHub deployment)

1. Go to **Deployment** tab
2. Click **"Enable App Token"**
3. **Copy the token** - you'll need it for GitHub

---

## Step 3: Run Database Migration

The chat system needs database tables created.

### CapRover → Apps → multivendor-backend → Deployment tab

In the **"Execute Command"** section, run:

```bash
python manage.py migrate
```

Wait for success message. You should see:
```
Running migrations:
  Applying chat.0001_initial... OK
```

---

## Step 4: Deploy Apps

### Option A: Deploy via GitHub Actions (Recommended)

1. **Add GitHub Secret for Frontend:**
   - Go to: GitHub → Settings → Secrets and variables → Actions
   - Add new secret:
     - Name: `CAPROVER_APP_TOKEN_FRONTEND`
     - Value: `<token from Step 2D>`

2. **Make sure you also have these secrets:**
   - `CAPROVER_SERVER` = `https://captain.indexo.ir`
   - `CAPROVER_APP_BACKEND` = `multivendor-backend`
   - `CAPROVER_APP_FRONTEND` = `multivendor-frontend`
   - `CAPROVER_APP_TOKEN_BACKEND` = `<backend token>`

3. **Deploy:**
   ```bash
   git add .
   git commit -m "Add chat system with Redis password support"
   git push origin main
   ```

4. **Monitor:** GitHub → Actions tab

### Option B: Deploy Manually (Alternative)

```bash
# Install CapRover CLI (if not installed)
npm install -g caprover

# Deploy backend
cd /media/jalal/New\ Volume/project/mulitvendor_platform
caprover deploy -a multivendor-backend

# Deploy frontend
cd multivendor_platform/front_end/nuxt
caprover deploy -a multivendor-frontend
```

---

## Step 5: Test Everything

### A. Test Backend

1. Visit: `https://multivendor-backend.indexo.ir/api/`
   - Should show API response

2. Visit: `https://multivendor-backend.indexo.ir/admin/`
   - Should show Django admin login

3. Check Redis connection:
   - CapRover → multivendor-backend → App Logs
   - Look for: No Redis errors
   - Should see: "Daphne" starting

### B. Test Frontend

1. Visit: `https://indexo.ir`
   - Homepage should load

2. Open browser console (F12)
   - Look for: "WebSocket connected"
   - Should see: "Chat connection established"

### C. Test Chat System

1. **Register/Login** to the site
2. **Find a product**
3. **Click "Chat with Vendor"** button
4. **Send a message**
5. **Check if message appears**

---

## 🔍 Troubleshooting

### Issue: Redis Connection Failed

**Error in logs:** `Error connecting to Redis`

**Solution:**
```bash
# Check if Redis is running
CapRover → Apps → multivendor-redis → should show "Running"

# Verify backend has Redis variables
CapRover → Apps → multivendor-backend → App Configs
- REDIS_HOST=srv-captain--multivendor-redis
- REDIS_PORT=6379
- REDIS_PASSWORD=strongPassword*67
```

### Issue: Database Connection Failed

**Error:** `database "multivendor_db" does not exist`

**Solution:**
The database name was wrong. It's fixed now to `multivendor-db` (with dash).
Restart backend after saving the fix.

### Issue: WebSocket Not Connecting

**Check:**
1. Redis is running
2. Backend has Redis variables
3. Frontend has correct API URL
4. Browser console for errors

### Issue: CORS Errors

**Check:**
1. `CORS_ALLOWED_ORIGINS` includes frontend domain
2. `CSRF_TRUSTED_ORIGINS` includes frontend domain
3. Domains use `https://` not `http://`

---

## ✅ Success Checklist

After deployment, verify:

- [ ] Backend app shows "Running" in CapRover
- [ ] Frontend app shows "Running" in CapRover
- [ ] Redis shows "Running"
- [ ] PostgreSQL shows "Running"
- [ ] https://multivendor-backend.indexo.ir/api/ works
- [ ] https://indexo.ir loads
- [ ] Can login/register
- [ ] Browser console shows "WebSocket connected"
- [ ] Can open chat widget
- [ ] Can send chat messages
- [ ] Messages appear in real-time

---

## 📊 Your Complete Backend Configuration

Here's the full list of environment variables your backend should have:

```env
# Django Core
SECRET_KEY=tfu9y@exp6tdda$%f_+u&o80jd!%ld5@y=iua)$176x5bf(aut
DEBUG=False
DJANGO_SETTINGS_MODULE=multivendor_platform.settings

# Database (UPDATED)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor-db
DB_USER=postgres
DB_PASSWORD=thisIsAsimplePassword09
DB_HOST=srv-captain--postgres-db
DB_PORT=5432

# Redis (NEW - REQUIRED FOR CHAT)
REDIS_HOST=srv-captain--multivendor-redis
REDIS_PORT=6379
REDIS_PASSWORD=strongPassword*67

# Security & CORS
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
CORS_ALLOWED_ORIGINS=https://multivendor-frontend.indexo.ir,https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_ALL_ORIGINS=False
CSRF_TRUSTED_ORIGINS=https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir
USE_TLS=True

# Site
SITE_URL=https://indexo.ir

# Static & Media
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
```

---

## 🎯 What Changed in Code

I updated `settings.py` to support Redis password:

**Before:**
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],  # No password support
        },
    },
}
```

**After:**
```python
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [REDIS_URL],  # Uses password
            },
        },
    }
```

This change is already committed and ready to deploy.

---

## 🚦 Quick Start - Do This Now!

1. **Update backend config** (5 minutes)
   - Add Redis variables
   - Fix DB_NAME
   - Add CSRF_TRUSTED_ORIGINS

2. **Create frontend app** (10 minutes)
   - Create app
   - Add environment variables
   - Enable app token

3. **Run migration** (2 minutes)
   - Execute: `python manage.py migrate`

4. **Deploy** (15 minutes)
   - Push to GitHub OR
   - Deploy manually with CapRover CLI

5. **Test** (10 minutes)
   - Check all URLs work
   - Test chat functionality

**Total Time: ~45 minutes**

---

**Ready to Deploy?** Start with Step 1! 🚀

**Questions?** Check the logs in CapRover for any errors.

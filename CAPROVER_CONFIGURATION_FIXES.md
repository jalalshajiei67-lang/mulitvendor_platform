# CapRover Configuration Fixes - Action Required

**Date:** 2025-01-27  
**Status:** ⚠️ **CRITICAL - Manual Action Required in CapRover Dashboard**

---

## 🔴 CRITICAL: Backend App Configuration

You need to update the backend app environment variables in CapRover dashboard:

### Current Issue:
- Backend app uses: `DJANGO_SETTINGS_MODULE=multivendor_platform.settings` ❌
- Should use: `DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover` ✅

### Steps to Fix:

1. Go to CapRover Dashboard: https://captain.indexo.ir
2. Click on **multivendor-backend** app
3. Go to **App Configs** tab
4. Find **Environmental Variables** section
5. Update or add this variable:
   ```
   DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
   ```
6. Click **Save & Update**
7. Wait for app to restart

---

## 🔴 CRITICAL: Frontend App Configuration

You need to update the frontend app environment variables in CapRover dashboard:

### Current Issues:
- Uses `VITE_API_BASE_URL` (wrong for Nuxt 3) ❌
- Uses `VUE_APP_*` variables (wrong for Nuxt 3) ❌
- Missing `NUXT_PUBLIC_API_BASE` (required) ❌

### Steps to Fix:

1. Go to CapRover Dashboard: https://captain.indexo.ir
2. Click on **multivendor-frontend** app
3. Go to **App Configs** tab
4. Find **Environmental Variables** section
5. **Remove** these old variables:
   - `VITE_API_BASE_URL`
   - `VITE_DJANGO_ADMIN_URL`
   - `VUE_APP_TITLE`
   - `VUE_APP_DESCRIPTION`
6. **Add** these new variables:
   ```
   NODE_ENV=production
   NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
   NUXT_PUBLIC_SITE_URL=https://indexo.ir
   NUXT_PUBLIC_DJANGO_ADMIN_URL=https://multivendor-backend.indexo.ir/admin/
   NUXT_HOST=0.0.0.0
   NUXT_PORT=3000
   ```
7. Click **Save & Update**
8. **IMPORTANT:** After saving, you need to **rebuild** the frontend app because environment variables are used at build time for Nuxt 3
9. Go to **Deployment** tab → Click **Force Rebuild**

---

## ✅ Verified Correct Configurations

These are already correct in your CapRover setup:

### Backend:
- ✅ Database name: `multivendor_db`
- ✅ Database host: `srv-captain--postgres-db`
- ✅ Redis host: `srv-captain--multivendor-redis`
- ✅ Allowed hosts and CORS settings
- ✅ Static and media paths

### Frontend:
- ✅ App name: `multivendor-frontend`

---

## 📋 Complete Backend Environment Variables

After fixing, your backend app should have these variables:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=thisIsAsimplePassword09
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
SECRET_KEY=tfu9y@exp6tdda$%f_+u&o80jd!%ld5@y=iua)$176x5bf(aut
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
CORS_ALLOWED_ORIGINS=https://multivendor-frontend.indexo.ir,https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_ALL_ORIGINS=False
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
REDIS_HOST=srv-captain--multivendor-redis
REDIS_PORT=6379
REDIS_PASSWORD=strongPassword*67
CSRF_TRUSTED_ORIGINS=https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir
USE_TLS=True
SITE_URL=https://indexo.ir
```

---

## 📋 Complete Frontend Environment Variables

After fixing, your frontend app should have these variables:

```env
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://indexo.ir
NUXT_PUBLIC_DJANGO_ADMIN_URL=https://multivendor-backend.indexo.ir/admin/
NUXT_HOST=0.0.0.0
NUXT_PORT=3000
```

---

## ⚠️ Important Notes

1. **Frontend Rebuild Required:** After updating frontend environment variables, you MUST rebuild the app because Nuxt 3 embeds `NUXT_PUBLIC_*` variables at build time.

2. **Backend Restart:** Backend will automatically restart after saving environment variables.

3. **Verify Settings:** After making changes, check the app logs to ensure:
   - Backend is using `settings_caprover.py`
   - Frontend can connect to backend API
   - No environment variable errors

---

## 🔍 Verification Steps

After making changes:

### Backend Verification:
1. Go to backend app → **App Logs**
2. Look for: `Using settings module: multivendor_platform.settings_caprover`
3. Check for any database connection errors
4. Verify Redis connection

### Frontend Verification:
1. Go to frontend app → **App Logs**
2. Check build logs for correct API URL
3. Verify no environment variable warnings
4. Test frontend → backend API connection

---

## 📝 Summary of Changes Made

### Files Updated in Repository:
- ✅ `Dockerfile` - Fixed port from 8000 to 80
- ✅ `.github/workflows/deploy-caprover.yml` - Uses CAPROVER_SERVER secret
- ✅ `caprover-env-backend.txt` - Updated to match actual config
- ✅ `caprover-env-frontend.txt` - Fixed to use NUXT_PUBLIC_* variables
- ✅ `ENV_VARIABLES.md` - Updated documentation
- ✅ `GITHUB_SECRETS_SETUP.md` - Fixed secret names
- ✅ `REQUIREMENTS_CI_CD_CAPROVER.md` - Updated configuration

### Manual Actions Required in CapRover:
- ⚠️ **Backend:** Update `DJANGO_SETTINGS_MODULE` to `settings_caprover`
- ⚠️ **Frontend:** Replace `VITE_*` and `VUE_APP_*` with `NUXT_PUBLIC_*` variables
- ⚠️ **Frontend:** Force rebuild after updating environment variables

---

**After completing these manual steps, your deployment configuration will be fully aligned!**





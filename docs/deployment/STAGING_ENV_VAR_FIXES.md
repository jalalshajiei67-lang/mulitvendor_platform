# Fix Staging Backend Environment Variables

## Issues Found in Your Current Configuration

### ✅ Correct Settings:
- `DB_USER=postgres` ✅
- `DB_HOST=srv-captain--postgres-db-staging` ✅
- `DB_PORT=5432` ✅

### ❌ Issues to Fix:

1. **DJANGO_SETTINGS_MODULE is wrong**
   - Current: `multivendor_platform.settings`
   - Should be: `multivendor_platform.settings_caprover`
   - **Impact:** Settings might not work correctly for CapRover deployment

2. **ALLOWED_HOSTS is incomplete**
   - Current: `multivendor-backend-staging.indexo.ir`
   - Should include: `staging-api.indexo.ir,staging-backend.indexo.ir,staging.indexo.ir`
   - **Impact:** Requests from other domains will be rejected

3. **CORS_ALLOWED_ORIGINS needs staging-frontend domain**
   - Current: `https://multivendor-frontend-staging.indexo.ir`
   - Should also include: `https://staging.indexo.ir`
   - **Impact:** Frontend might not be able to make API calls

4. **Database credentials need verification**
   - The error shows it's trying to connect but failing
   - Need to verify PostgreSQL staging app has matching credentials

## ✅ Corrected Environment Variables

Copy and paste this into CapRover → Apps → `multivendor-backend-staging` → App Configs → Environment Variables → Bulk Edit:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor-db-staging
DB_USER=postgres
DB_PASSWORD=thisIsAsimplePassword09-staging
DB_HOST=srv-captain--postgres-db-staging
DB_PORT=5432

SECRET_KEY=b75duf)tc8__9%_ur(#+q9^@r%-(5)==@z$e8d4q1ss!=#qa!n
DEBUG=False
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover

ALLOWED_HOSTS=staging-api.indexo.ir,staging-backend.indexo.ir,staging.indexo.ir,multivendor-backend-staging.indexo.ir
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir,https://multivendor-frontend-staging.indexo.ir
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_ALL_ORIGINS=False
CSRF_TRUSTED_ORIGINS=https://staging-api.indexo.ir,https://staging.indexo.ir,https://multivendor-backend-staging.indexo.ir

STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media

REDIS_HOST=srv-captain--multivendor-redis-staging
REDIS_PORT=6379
REDIS_PASSWORD=strongPassword*67-staging

USE_TLS=True
SITE_URL=https://staging.indexo.ir
```

## 🔍 Database Verification Steps

The error shows authentication is failing. Verify these:

### Step 1: Check PostgreSQL Staging App Credentials

1. Go to CapRover → Apps → `postgres-db-staging`
2. Click **App Configs** → **Environment Variables**
3. Verify these match your backend settings:
   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=thisIsAsimplePassword09-staging
   POSTGRES_DB=multivendor-db-staging
   ```

### Step 2: Verify Database Exists

If the database doesn't exist, you may need to create it. The error might be that PostgreSQL is creating a default database, but your backend is looking for `multivendor-db-staging`.

**Option A:** Set PostgreSQL to create the database automatically
- In `postgres-db-staging` app, set `POSTGRES_DB=multivendor-db-staging`

**Option B:** Change backend to use default database
- In backend, change `DB_NAME=postgres` (if PostgreSQL creates default `postgres` database)

## 🚀 After Making Changes

1. Click **Save & Update** in the backend staging app
2. Wait 30-60 seconds for restart
3. Check logs - should see successful migrations
4. Frontend deployment will automatically trigger after backend succeeds







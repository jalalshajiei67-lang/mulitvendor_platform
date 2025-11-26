# Fix Staging Backend Environment Variables

## 🔴 Critical Issues to Fix

### Issue 1: Database Name Mismatch (Most Likely Cause)

**Your backend has:**
```
DB_NAME=multivendor-db-staging
```

**But PostgreSQL staging app might be creating database:** `postgres` (default)

### Issue 2: Wrong Django Settings Module

**Current:**
```
DJANGO_SETTINGS_MODULE=multivendor_platform.settings
```

**Should be:**
```
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
```

### Issue 3: Incomplete ALLOWED_HOSTS

**Current:**
```
ALLOWED_HOSTS=multivendor-backend-staging.indexo.ir
```

**Should include all staging domains.**

## ✅ Complete Fixed Environment Variables

Copy this into CapRover → Apps → `multivendor-backend-staging` → App Configs → Environment Variables → **Bulk Edit**:

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

## 🔍 Verify PostgreSQL Staging App Configuration

**Critical Step:** Check your PostgreSQL staging app has matching database name.

1. Go to CapRover → Apps → `postgres-db-staging`
2. Click **App Configs** → **Environment Variables**
3. Verify it has:
   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=thisIsAsimplePassword09-staging
   POSTGRES_DB=multivendor-db-staging
   ```

**If `POSTGRES_DB` is missing or set to `postgres`:**
- Add/change: `POSTGRES_DB=multivendor-db-staging`
- This will create the database with the correct name when PostgreSQL starts

**⚠️ Important:** If PostgreSQL was already initialized with a different database name, you may need to:
1. Delete and recreate the PostgreSQL staging app (will lose data), OR
2. Manually create the database (see below)

## 🔧 If Database Doesn't Exist - Create It Manually

If PostgreSQL staging app already exists but doesn't have the `multivendor-db-staging` database:

1. SSH to your server:
   ```bash
   ssh root@185.208.172.76
   ```

2. Connect to PostgreSQL:
   ```bash
   docker exec -it srv-captain--postgres-db-staging psql -U postgres
   ```

3. Create the database:
   ```sql
   CREATE DATABASE "multivendor-db-staging";
   \q
   ```

## ✅ After Making Changes

1. **Save & Update** in backend staging app
2. Wait 30-60 seconds for restart
3. Check logs - should see:
   - ✅ `Database connection successful!`
   - ✅ `Migrations completed successfully!`

## 📋 Key Changes Summary

1. ✅ Changed `DJANGO_SETTINGS_MODULE` to `settings_caprover`
2. ✅ Added missing domains to `ALLOWED_HOSTS`
3. ✅ Added missing domains to `CSRF_TRUSTED_ORIGINS`
4. ✅ Verified database credentials match PostgreSQL app


# Fix Staging Database Authentication Error

## Problem
```
password authentication failed for user "postgres-staging"
```

The backend is trying to connect with user `postgres-staging`, but it should be `postgres`.

## Solution: Fix Database Credentials in CapRover

### Step 1: Check PostgreSQL Staging Database Credentials

1. Go to CapRover Dashboard: `https://captain.indexo.ir`
2. Navigate to **Apps** → **postgres-db-staging**
3. Click **App Configs** → **Environment Variables**
4. Note the following values:
   - `POSTGRES_USER` (should be `postgres`)
   - `POSTGRES_PASSWORD` (copy this password!)
   - `POSTGRES_DB` (should be `postgres`)

### Step 2: Fix Backend Staging App Environment Variables

1. Go to **Apps** → **multivendor-backend-staging**
2. Click **App Configs** → **Environment Variables**
3. Click **Bulk Edit**
4. Make sure these are set correctly:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<paste-the-password-from-postgres-db-staging>
DB_HOST=srv-captain--postgres-db-staging
DB_PORT=5432
```

**Critical:**
- `DB_USER` must be `postgres` (NOT `postgres-staging`)
- `DB_PASSWORD` must match the password from `postgres-db-staging` app
- `DB_NAME` should be `postgres` (or whatever is set in POSTGRES_DB)

### Step 3: Verify All Required Environment Variables

While you're in the backend staging app configs, make sure all these are set:

```env
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<your-staging-postgres-password>
DB_HOST=srv-captain--postgres-db-staging
DB_PORT=5432

# Django Configuration
SECRET_KEY=<generate-a-strong-secret-key>
DEBUG=True
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover

# Security
ALLOWED_HOSTS=staging-api.indexo.ir,staging-backend.indexo.ir,staging.indexo.ir
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir,https://staging-frontend.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True
CSRF_TRUSTED_ORIGINS=https://staging-api.indexo.ir,https://staging.indexo.ir

# Static Files
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media

# Redis
REDIS_HOST=srv-captain--multivendor-redis-staging
REDIS_PORT=6379

# Site
USE_TLS=True
SITE_URL=https://staging.indexo.ir
```

### Step 4: Save and Restart

1. Click **Save & Update** button
2. Wait 30-60 seconds for the app to restart
3. Check **Logs** tab - you should see successful migrations

### Step 5: Verify the Fix

Look for these in the logs:
- ✅ `Database connection successful!`
- ✅ `Migrations completed successfully!`
- ❌ No more `password authentication failed` errors

## Common Issues

### Issue 1: DB_USER is wrong
**Check:** Make sure `DB_USER=postgres` (not `postgres-staging` or anything else)

### Issue 2: Password doesn't match
**Fix:** Get the exact password from `postgres-db-staging` app's `POSTGRES_PASSWORD` env var

### Issue 3: DB_NAME doesn't match
**Fix:** Check what `POSTGRES_DB` is set to in the postgres app, and match it in backend

## Quick Reference

The error message shows it's trying to connect as `postgres-staging`, which means somewhere the `DB_USER` env var is set incorrectly. Make sure it's exactly `postgres`.






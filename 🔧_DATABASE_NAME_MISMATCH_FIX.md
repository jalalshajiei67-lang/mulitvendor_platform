# 🔧 Database Name Mismatch - Quick Fix

## Problem Identified

Your backend is failing with:
```
FATAL: password authentication failed for user "postgres"
```

**Root Cause:** Database name mismatch between apps!

### Current Configuration:

**Backend App (multivendor-backend):**
```
DB_NAME=multivendor-db  ← Trying to connect to this database
```

**Database App (multivendor_db):**
```
POSTGRES_DB=postgres  ← But creating this database instead
```

## ✅ Solution

You need to update your PostgreSQL app's environment variable to match what your backend expects.

### Step 1: Update Database App Environment Variable

In CapRover dashboard for `multivendor_db` app:

**Change:**
```
POSTGRES_DB=postgres
```

**To:**
```
POSTGRES_DB=multivendor-db
```

### Step 2: Restart Both Apps

After updating the environment variable:

1. **Restart the database app first:**
   - Go to `multivendor_db` app in CapRover
   - Click "Save & Update" (this will recreate the database with the correct name)
   
2. **Then restart the backend app:**
   - Go to `multivendor-backend` app
   - Click "Save & Update" or restart

### Alternative Solution (If you prefer to keep database as "postgres")

If you want to keep the database named "postgres", update your **backend app** instead:

**Change in multivendor-backend:**
```
DB_NAME=multivendor-db
```

**To:**
```
DB_NAME=postgres
```

## ⚠️ Important Notes

1. **Changing POSTGRES_DB will create a new empty database** - any existing data in the old database won't be automatically transferred.

2. **If you have existing data you want to keep:**
   - You need to backup first
   - Or manually create the database with the correct name
   - Or use PostgreSQL tools to rename the database

3. **Recommended approach:** Use the first solution (change POSTGRES_DB to multivendor-db) as it matches your backend configuration.

## Complete Environment Variables (Corrected)

### multivendor_db App:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=thisIsAsimplePassword09
POSTGRES_DB=multivendor-db  ← CHANGED HERE
POSTGRES_INITDB_ARGS=
```

### multivendor-backend App:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor-db  ← Matches above
DB_USER=postgres
DB_PASSWORD=thisIsAsimplePassword09
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
SECRET_KEY=tfu9y@exp6tdda$%f_+u&o80jd!%ld5@y=iua)$176x5bf(aut
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
CORS_ALLOWED_ORIGINS=https://multivendor-frontend.indexo.ir,https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
```

## Verification

After making the change and restarting, check the backend logs. You should see:
```
✅ Operations to perform:
✅ Applying migrations...
✅ Starting server...
```

Instead of:
```
❌ password authentication failed for user "postgres"
```

## Next Steps

1. Update the environment variable
2. Restart both apps
3. Check logs to confirm connection
4. Run migrations if needed
5. Create superuser if it's a fresh database

## Quick Commands to Run After Fix

If you need to access the backend container to run migrations or create superuser:

```bash
# In CapRover, use "App Configs" → "Deployment" → "Edit Default Dockerfile Commands"
# Or SSH into your server and run:

# Enter the backend container
docker exec -it $(docker ps -q -f name=srv-captain--multivendor-backend) bash

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

**Status:** Ready to implement
**Estimated Time:** 5 minutes
**Risk Level:** Low (just environment variable change)








# 🔧 Deployment Fix Guide - Database Migration & Static Files

## 🚨 Issues Found

1. **Database migrations not running** - PostgreSQL tables don't exist
2. **API returning 403 Forbidden** - Due to missing database tables
3. **Silent failures** - Migrations failed but server continued running

## ✅ Fixes Applied

### 1. Updated Dockerfile.backend

**Problem:** Migrations were failing silently with `|| echo "warning" && continue`

**Solution:** Created proper entrypoint script that:
- ✅ Waits for database to be ready
- ✅ Tests database connection
- ✅ Runs migrations (fails container if migrations fail)
- ✅ Collects static files
- ✅ Sets up media directories
- ✅ Only starts Gunicorn if everything succeeds

### 2. Updated settings_caprover.py

**Problem:** REST API permissions were too restrictive

**Solution:** Changed from `IsAuthenticatedOrReadOnly` to `AllowAny` for public API access

### 3. Created docker-entrypoint.sh

**Problem:** No proper health checks or startup validation

**Solution:** Comprehensive startup script with:
- Database readiness checks (30 retries, 2s intervals)
- Database connection testing
- Migration execution with error handling
- Static files collection
- Directory setup
- Django configuration validation

## 📋 Deployment Steps

### Option 1: Automatic Deployment (GitHub Actions)

Simply push to main branch:

```bash
git add .
git commit -m "fix: Database migrations and static files collection"
git push origin main
```

The GitHub Actions workflow will:
1. Deploy backend to CapRover
2. Run migrations automatically via entrypoint script
3. Collect static files
4. Deploy frontend

### Option 2: Manual Deployment via CapRover Dashboard

1. **Go to CapRover Dashboard**
   - URL: https://captain.indexo.ir/
   - Navigate to your backend app: `multivendor-backend`

2. **Check Environment Variables**
   Make sure these are set in App Configs → Environment Variables:
   
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   DB_HOST=srv-captain--postgres-db
   DB_PORT=5432
   
   SECRET_KEY=your_secret_key_here
   DEBUG=False
   ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
   
   CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
   CORS_ALLOW_ALL_ORIGINS=False
   ```

3. **Deploy the Updated Code**
   - Method A: Use GitHub Actions (push to main)
   - Method B: Manual deployment from CapRover dashboard

4. **Monitor Deployment Logs**
   - Go to App Details → App Logs
   - Watch for the startup sequence:
     ```
     [1/7] Waiting for database to be ready...
     [2/7] Testing database connection...
     [3/7] Running database migrations...
     [4/7] Setting up media directories...
     [5/7] Collecting static files...
     [6/7] Verifying Django configuration...
     [7/7] Starting Gunicorn server...
     ```

### Option 3: Manual Commands (If Needed)

If you need to run migrations manually, SSH into the container:

```bash
# SSH into CapRover host
ssh root@185.208.172.76

# Find the backend container
docker ps | grep multivendor-backend

# Execute commands in the container
docker exec -it <container_id> bash

# Inside container:
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # If needed
```

## 🔍 Verification Steps

### 1. Check Backend Logs

In CapRover Dashboard → multivendor-backend → Logs:

**✅ Success indicators:**
- `✅ Database is ready!`
- `✅ Database connection successful!`
- `✅ Migrations completed successfully!`
- `✅ Static files collected successfully!`
- `[INFO] Starting gunicorn`

**❌ Failure indicators:**
- `❌ Database is not ready`
- `❌ Database connection failed!`
- `❌ Migrations failed!`

### 2. Check Database Logs

In CapRover Dashboard → postgres-db → Logs:

**Should NOT see:**
- `ERROR: relation "products_category" does not exist`
- `ERROR: relation "products_product" does not exist`
- `ERROR: relation "authtoken_token" does not exist`

### 3. Test API Endpoints

Open your browser or use curl:

```bash
# Test categories endpoint
curl https://multivendor-backend.indexo.ir/api/categories/

# Test products endpoint  
curl https://multivendor-backend.indexo.ir/api/products/

# Test suppliers endpoint
curl https://multivendor-backend.indexo.ir/api/users/suppliers/
```

**✅ Should return:** JSON data or empty arrays `[]`
**❌ Should NOT return:** `{"detail": "Authentication credentials were not provided."}` or 403 errors

### 4. Check Static Files

Visit admin panel:

```
https://multivendor-backend.indexo.ir/admin/
```

**✅ Should see:** Modern Django Unfold admin theme with proper styling
**❌ Should NOT see:** Plain HTML without CSS

### 5. Test Frontend

Visit your website:

```
https://indexo.ir/
```

**✅ Should see:** Products, categories, and data from backend
**❌ Should NOT see:** Empty pages or loading errors

## 🐛 Troubleshooting

### Issue: Migrations Still Failing

**Symptom:** Logs show `❌ Migrations failed!`

**Solution:**
1. Check database connection settings
2. Verify postgres-db app is running
3. Check database credentials
4. Try connecting manually:
   ```bash
   docker exec -it <backend_container> bash
   python manage.py dbshell
   \dt  # List tables
   ```

### Issue: Static Files Not Loading

**Symptom:** Admin panel has no CSS styling

**Solution:**
1. Check if collectstatic succeeded in logs
2. Verify STATIC_ROOT and STATIC_URL settings
3. Check file permissions:
   ```bash
   ls -la /app/staticfiles/
   ```
4. Manually run collectstatic:
   ```bash
   docker exec -it <backend_container> python manage.py collectstatic --noinput
   ```

### Issue: 403 Forbidden on API

**Symptom:** API endpoints return 403 errors

**Solution:**
1. Verify migrations completed successfully
2. Check REST_FRAMEWORK settings in settings_caprover.py
3. Ensure `DEFAULT_PERMISSION_CLASSES` is set to `AllowAny`
4. Check CORS settings

### Issue: Database Connection Refused

**Symptom:** `❌ Database is not ready after 30 attempts!`

**Solution:**
1. Verify postgres-db app is running in CapRover
2. Check DB_HOST environment variable: `srv-captain--postgres-db`
3. Verify database credentials
4. Check postgres-db logs for errors

## 📝 Files Changed

1. ✅ `Dockerfile.backend` - Updated to use entrypoint script
2. ✅ `docker-entrypoint.sh` - New startup script with proper health checks
3. ✅ `multivendor_platform/multivendor_platform/settings_caprover.py` - Updated REST permissions

## 🚀 Next Steps After Successful Deployment

1. **Create superuser** (if not exists):
   ```bash
   docker exec -it <container_id> python manage.py createsuperuser
   ```

2. **Populate initial data** (if needed):
   ```bash
   docker exec -it <container_id> python manage.py populate_categories
   docker exec -it <container_id> python manage.py populate_products
   ```

3. **Test admin panel**:
   - Login at: https://multivendor-backend.indexo.ir/admin/
   - Verify all models are accessible
   - Check that products and categories display correctly

4. **Test frontend**:
   - Visit: https://indexo.ir/
   - Verify data loads from API
   - Test navigation and filtering

## 📞 Support

If issues persist after following this guide:

1. Check CapRover logs for both:
   - multivendor-backend app
   - postgres-db app

2. Share the following information:
   - Backend startup logs (first 100 lines)
   - Database error logs
   - Output of API test requests

3. Verify all environment variables are set correctly in CapRover dashboard

## ✅ Success Criteria

Deployment is successful when:

- ✅ Backend container starts without errors
- ✅ All 7 startup steps complete successfully
- ✅ API endpoints return data (not 403 errors)
- ✅ Admin panel loads with proper styling
- ✅ Frontend displays products and categories
- ✅ No database relation errors in postgres logs

---

**Last Updated:** 2025-11-11
**Version:** 1.0

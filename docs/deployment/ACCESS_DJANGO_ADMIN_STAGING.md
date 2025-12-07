# 🔐 Access Django Admin Dashboard on Staging

## 🎯 Django Admin URL

**Primary URL:**
```
https://staging-api.indexo.ir/admin/
```

**Alternative (if configured):**
```
https://staging-backend.indexo.ir/admin/
```

---

## 🔍 Troubleshooting: "Nothing here yet :/" Error

This error means the backend app isn't running or the domain isn't configured correctly.

### Step 1: Check Backend App Status in CapRover

1. Go to **CapRover Dashboard**: `https://captain.indexo.ir`
2. Navigate to **Apps** → **multivendor-backend-staging**
3. Check the status badge:
   - 🟢 **Running** - App is running (but might still have issues)
   - 🟡 **Building** - Still deploying, wait 2-5 minutes
   - 🔴 **Error** - Something is wrong, check logs

### Step 2: Verify Domain Configuration

1. In CapRover → **multivendor-backend-staging** app
2. Click **HTTP Settings** tab
3. Check **Custom Domain** section:
   - Should have: `staging-api.indexo.ir`
   - Optionally: `staging-backend.indexo.ir`
4. If missing, **Add** `staging-api.indexo.ir`
5. Click **Save & Update**
6. Wait 30-60 seconds

### Step 3: Check Backend App Logs

1. In CapRover → **multivendor-backend-staging** app
2. Click **Logs** tab
3. Look for these patterns:

#### ✅ **Good Signs (Should See):**
```
Starting application server...
Database connection successful!
Migrations completed successfully!
Application startup complete.
```

#### ❌ **Bad Signs (Errors):**
```
Error: Database connection failed
Error: Cannot find module
Error: Migration failed
Error: Port 8000 already in use
```

**If you see errors, copy the error message and share it!**

### Step 4: Verify Environment Variables

1. In CapRover → **multivendor-backend-staging** app
2. Click **App Configs** → **Environment Variables**
3. Verify these are set:

```env
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
ALLOWED_HOSTS=staging-api.indexo.ir,staging-backend.indexo.ir,staging.indexo.ir
DEBUG=False
```

### Step 5: Test Backend Health

Try these URLs to verify backend is working:

1. **Health Check:**
   ```
   https://staging-api.indexo.ir/health/
   ```
   Should return: `OK`

2. **API Endpoint:**
   ```
   https://staging-api.indexo.ir/api/
   ```
   Should return: API response (not "Nothing here yet :/")

3. **Django Admin:**
   ```
   https://staging-api.indexo.ir/admin/
   ```
   Should show: Django admin login page

---

## 👤 Create Django Superuser

If the admin page loads but you can't login, you need to create a superuser.

### Method 1: Using CapRover Terminal (Recommended)

1. Go to CapRover → **multivendor-backend-staging** app
2. Click **One-Click Apps/Databases** tab (or **App Configs** → **Terminal**)
3. Click **Terminal** button
4. Run this command:

```bash
python manage.py createsuperuser
```

5. Follow the prompts:
   - Username: `admin` (or your choice)
   - Email: `admin@indexo.ir` (or your email)
   - Password: (enter a strong password)

### Method 2: Using SSH (Alternative)

1. SSH into your VPS:
   ```bash
   ssh root@185.208.172.76
   ```

2. Execute command in backend container:
   ```bash
   docker exec -it srv-captain--multivendor-backend-staging python manage.py createsuperuser
   ```

3. Follow the prompts to create superuser

### Method 3: Using Script (Non-Interactive)

1. SSH into your VPS:
   ```bash
   ssh root@185.208.172.76
   ```

2. Copy the create_superuser_production.py script to the container:
   ```bash
   docker cp create_superuser_production.py srv-captain--multivendor-backend-staging:/app/
   ```

3. Run the script:
   ```bash
   docker exec -it srv-captain--multivendor-backend-staging python create_superuser_production.py
   ```

   Or with custom credentials:
   ```bash
   docker exec -it srv-captain--multivendor-backend-staging bash -c "SUPERUSER_USERNAME=admin SUPERUSER_EMAIL=admin@indexo.ir SUPERUSER_PASSWORD=your_secure_password python create_superuser_production.py"
   ```

---

## ✅ After Creating Superuser

1. Go to: `https://staging-api.indexo.ir/admin/`
2. Login with your superuser credentials
3. You should see the Django admin dashboard

---

## 🔧 Common Issues & Fixes

### Issue 1: Backend App Shows "Error" Status

**Fix:**
1. Check logs for specific error
2. Verify database is running and accessible
3. Check environment variables are correct
4. Try restarting the app: **App Configs** → **Save & Update**

### Issue 2: Domain Not Resolving

**Fix:**
1. Verify domain is added in CapRover HTTP Settings
2. Check DNS records point to your VPS IP: `185.208.172.76`
3. Wait 5-10 minutes for DNS propagation

### Issue 3: Database Connection Error

**Fix:**
1. Verify PostgreSQL app is running in CapRover
2. Check database credentials in environment variables
3. Verify database name matches: `multivendor-db-staging`

### Issue 4: 502 Bad Gateway

**Fix:**
1. Backend container might be crashing
2. Check logs for startup errors
3. Verify all environment variables are set
4. Check if port 8000 is configured correctly

---

## 📋 Quick Checklist

- [ ] Backend app status is "Running" (green) in CapRover
- [ ] Domain `staging-api.indexo.ir` is configured in HTTP Settings
- [ ] Backend logs show "Application startup complete"
- [ ] Health check endpoint returns "OK"
- [ ] Superuser account created
- [ ] Can access `https://staging-api.indexo.ir/admin/` and see login page
- [ ] Can login with superuser credentials

---

## 🆘 Still Having Issues?

If you're still seeing "Nothing here yet :/", check:

1. **Backend app exists in CapRover?**
   - Go to CapRover → Apps
   - Look for `multivendor-backend-staging`
   - If missing, the app needs to be created first

2. **Backend app is deployed?**
   - Check GitHub Actions for deployment status
   - Verify the backend deployment workflow completed successfully

3. **Share the following information:**
   - Backend app status (Running/Error/Building)
   - Last 20 lines of backend logs
   - Environment variables (without sensitive data)
   - Error message from browser console (F12 → Console tab)





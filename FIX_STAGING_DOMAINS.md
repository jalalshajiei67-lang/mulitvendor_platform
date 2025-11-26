# Fix Staging Domain Configuration

## 🔴 Problem

1. Backend app has wrong domain: `multivendor-backend-staging.indexo.ir`
2. Backend redirects to `http://localhost:5173/` (development URL)
3. Frontend shows "Nothing here yet :/"

## ✅ Solution: Fix Domain Configuration in CapRover

### Step 1: Fix Backend Domain

1. Go to CapRover Dashboard: `https://captain.indexo.ir`
2. Navigate to **Apps** → **multivendor-backend-staging**
3. Click **HTTP Settings** tab
4. In **Custom Domain** section:
   - **Remove:** `multivendor-backend-staging.indexo.ir` (if present)
   - **Add:** `staging-api.indexo.ir`
   - Optionally add: `staging-backend.indexo.ir` (for admin access)
5. Click **Save & Update**
6. Wait 30-60 seconds for changes to apply

### Step 2: Fix Frontend Domain

1. Go to CapRover Dashboard: `https://captain.indexo.ir`
2. Navigate to **Apps** → **multivendor-frontend-staging`
3. Click **HTTP Settings** tab
4. In **Custom Domain** section:
   - **Verify:** `staging.indexo.ir` is set
   - If not, **Add:** `staging.indexo.ir`
5. Click **Save & Update**

### Step 3: Update Backend Environment Variables

The redirect to `localhost:5173` might be in Django settings. Update backend env vars:

1. Go to CapRover → Apps → **multivendor-backend-staging**
2. Click **App Configs** → **Environment Variables**
3. **Bulk Edit** and ensure these are set:

```env
# Site Configuration - IMPORTANT: Remove localhost references!
SITE_URL=https://staging.indexo.ir

# Frontend URL (if your Django settings use this)
FRONTEND_URL=https://staging.indexo.ir

# Allowed Hosts - MUST include staging-api.indexo.ir
ALLOWED_HOSTS=staging-api.indexo.ir,staging-backend.indexo.ir,staging.indexo.ir

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://staging-api.indexo.ir,https://staging.indexo.ir

# CORS Origins
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir
```

4. Click **Save & Update**

### Step 4: Check Django Settings for Localhost Redirect

The redirect to `localhost:5173` might be hardcoded in Django settings. Let's check:

1. SSH into your VPS:
   ```bash
   ssh root@185.208.172.76
   ```

2. Check backend app logs for redirect settings:
   ```bash
   docker logs srv-captain--multivendor-backend-staging --tail 100
   ```

3. Look for any hardcoded `localhost:5173` or `127.0.0.1:5173` references

## 🔍 Verify Correct Domain Configuration

After fixing:

### Backend URLs should be:
- ✅ `https://staging-api.indexo.ir/api` - API endpoint
- ✅ `https://staging-api.indexo.ir/admin` - Django admin
- ❌ `https://multivendor-backend-staging.indexo.ir` - Should redirect or be removed

### Frontend URL should be:
- ✅ `https://staging.indexo.ir` - Main frontend

## ✅ Code Fix Applied

The hardcoded `localhost:5173` redirects in `products/views.py` have been fixed! The views now use `settings.SITE_URL` which reads from the `SITE_URL` environment variable.

**What changed:**
- `HomeView`, `VendorDashboardView`, and `ProductCreateView` now use `settings.SITE_URL` instead of hardcoded localhost URLs
- Fallback to `http://localhost:5173` for local development
- In staging/production, they'll use `https://staging.indexo.ir` (from `SITE_URL` env var)

**After deployment:**
1. Make sure `SITE_URL=https://staging.indexo.ir` is set in backend environment variables
2. Restart backend app
3. Redirects will now go to the correct staging frontend URL

## 📋 Quick Checklist

- [ ] Backend domain changed to `staging-api.indexo.ir` in CapRover
- [ ] Frontend domain verified as `staging.indexo.ir` in CapRover
- [ ] Backend environment variables updated (SITE_URL, ALLOWED_HOSTS)
- [ ] Backend app restarted (Save & Update)
- [ ] Test `https://staging-api.indexo.ir/api` - should return API response
- [ ] Test `https://staging.indexo.ir` - should show frontend
- [ ] No more redirects to `localhost:5173`


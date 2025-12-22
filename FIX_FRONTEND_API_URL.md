# Fix Frontend API URL Error

## 🔴 Problem
Frontend is trying to call `https://api.indexo.ir/api/categories/` but getting 502/404 errors.

**Correct backend URL:** `https://multivendor-backend.indexo.ir/api/`

## ✅ Solution: Update CapRover Frontend Environment Variables

### Step 1: Access CapRover Dashboard
1. Go to: `https://captain.indexo.ir`
2. Login with your credentials

### Step 2: Update Frontend App Environment Variables
1. Navigate to **Apps** → **multivendor-frontend** (or your frontend app name)
2. Click **App Configs** tab
3. Click **Environment Variables** section
4. **Remove** any of these if they exist:
   - `VITE_API_BASE_URL`
   - `VITE_DJANGO_ADMIN_URL`
   - `NUXT_PUBLIC_API_BASE` (if it's set to wrong value)
5. **Add/Update** these variables:
   ```
   NODE_ENV=production
   NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
   NUXT_PUBLIC_SITE_URL=https://indexo.ir
   NUXT_PUBLIC_DJANGO_ADMIN_URL=https://multivendor-backend.indexo.ir/admin/
   NUXT_HOST=0.0.0.0
   NUXT_PORT=3000
   ```
6. Click **Save & Update**

### Step 3: Force Rebuild Frontend (CRITICAL)
⚠️ **IMPORTANT:** Nuxt embeds environment variables at **build time**, not runtime!

1. In the same app, go to **Deployment** tab
2. Click **Force Rebuild** button
3. Wait for the build to complete (5-10 minutes)
4. Check build logs to verify `NUXT_PUBLIC_API_BASE` is set correctly

### Step 4: Verify Backend is Running
Before rebuilding, verify backend is accessible:

```bash
# Test backend API
curl https://multivendor-backend.indexo.ir/api/
curl https://multivendor-backend.indexo.ir/api/categories/
```

If these fail, fix backend first.

## 🔍 Verification After Rebuild

1. Check frontend logs:
   ```bash
   # In CapRover, go to frontend app → Logs
   # Look for successful startup messages
   ```

2. Test in browser:
   - Open: `https://indexo.ir`
   - Open browser console (F12)
   - Check for API errors
   - Should see successful API calls to `multivendor-backend.indexo.ir`

3. Check network tab:
   - All API calls should go to `https://multivendor-backend.indexo.ir/api/`
   - NOT `https://api.indexo.ir/api/`

## 🚨 If Still Not Working

### Check Backend Status
```bash
# SSH to your server
ssh root@185.208.172.76

# Check backend container
docker ps | grep backend

# Check backend logs
docker logs <backend-container-id>
```

### Check Backend Environment Variables
In CapRover → multivendor-backend → App Configs:
- Verify `ALLOWED_HOSTS` includes `multivendor-backend.indexo.ir`
- Verify `CORS_ALLOWED_ORIGINS` includes `https://indexo.ir`

### Alternative: Quick Test via SSH
```bash
# SSH to server
ssh root@185.208.172.76

# Check frontend container environment
docker exec <frontend-container-id> env | grep NUXT_PUBLIC_API_BASE

# Should show: NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
```

## 📝 Summary

**Root Cause:** Frontend was built with wrong `NUXT_PUBLIC_API_BASE` value (`https://api.indexo.ir/api` instead of `https://multivendor-backend.indexo.ir/api`)

**Fix:** Update environment variable in CapRover and force rebuild

**Time Required:** 5-10 minutes for rebuild


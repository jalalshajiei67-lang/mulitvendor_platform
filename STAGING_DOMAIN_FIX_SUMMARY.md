# 🔧 Staging Domain Fix - Action Required

## ✅ Code Fixed (Already Done)

The hardcoded `localhost:5173` redirects in the code have been fixed. Views now use `settings.SITE_URL` which reads from environment variables.

## 🔴 What You Need to Do in CapRover

### Step 1: Fix Backend Domain (CRITICAL)

1. Go to **CapRover Dashboard**: `https://captain.indexo.ir`
2. Click **Apps** → **multivendor-backend-staging**
3. Click **HTTP Settings** tab
4. In **Custom Domain** section:
   - **Remove** (if present): `multivendor-backend-staging.indexo.ir`
   - **Add**: `staging-api.indexo.ir`
5. Click **Save & Update**
6. Wait 30-60 seconds

### Step 2: Verify Frontend Domain

1. Go to **Apps** → **multivendor-frontend-staging**
2. Click **HTTP Settings** tab
3. Verify **Custom Domain** is: `staging.indexo.ir`
4. If missing, **Add** it
5. Click **Save & Update**

### Step 3: Update Backend Environment Variables

1. Go to **Apps** → **multivendor-backend-staging**
2. Click **App Configs** → **Environment Variables**
3. **Bulk Edit** and ensure `SITE_URL` is set:

```env
SITE_URL=https://staging.indexo.ir
```

4. Also verify these are set:
```env
ALLOWED_HOSTS=staging-api.indexo.ir,staging-backend.indexo.ir,staging.indexo.ir
CSRF_TRUSTED_ORIGINS=https://staging-api.indexo.ir,https://staging.indexo.ir
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir
```

5. Click **Save & Update**

## ✅ After Fixing

### Test These URLs:

1. **Backend API**: `https://staging-api.indexo.ir/api/` 
   - Should return API response (not redirect to localhost)

2. **Backend Admin**: `https://staging-api.indexo.ir/admin/`
   - Should show Django admin login

3. **Frontend**: `https://staging.indexo.ir/`
   - Should show your frontend (not "Nothing here yet :/")

## 🔍 Why This Happened

1. **Wrong Domain**: Backend app was configured with `multivendor-backend-staging.indexo.ir` instead of `staging-api.indexo.ir`
2. **Hardcoded Redirects**: Django views had hardcoded `localhost:5173` URLs (now fixed in code)
3. **Missing SITE_URL**: Backend didn't have `SITE_URL` environment variable set correctly

## 📋 Checklist

- [ ] Backend domain changed to `staging-api.indexo.ir` in CapRover
- [ ] Frontend domain verified as `staging.indexo.ir` in CapRover  
- [ ] Backend `SITE_URL` environment variable set to `https://staging.indexo.ir`
- [ ] Backend app restarted (Save & Update triggered restart)
- [ ] Test `https://staging-api.indexo.ir/api` works
- [ ] Test `https://staging.indexo.ir` shows frontend
- [ ] No more redirects to `localhost:5173`

## 🚀 Next Push

After you fix the domain in CapRover, the next push to staging will deploy the code fix, and everything should work correctly!





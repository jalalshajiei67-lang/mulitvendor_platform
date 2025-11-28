# Debug "Nothing here yet :/" on Staging Frontend

## 🔍 Quick Diagnostic Steps

### Step 1: Check if Frontend Workflow Ran

1. Go to GitHub → **Actions** tab
2. Look for "Deploy Frontend to Staging" workflow
3. Check if it:
   - ✅ Completed successfully (green checkmark)
   - ⚠️ Failed (red X)
   - ⏳ Still running (yellow circle)
   - ❌ Never ran (doesn't exist)

**If workflow never ran or failed:**
- Check the backend workflow status (frontend only runs after backend succeeds)
- Re-run the failed workflow if needed

### Step 2: Check Frontend Staging App Status in CapRover

1. Go to CapRover Dashboard: `https://captain.indexo.ir`
2. Navigate to **Apps** → **multivendor-frontend-staging**
3. Check the status:
   - ✅ **Running** (Green) - App is running
   - ⚠️ **Building** (Yellow) - Still deploying, wait
   - ❌ **Error** (Red) - Something failed

### Step 3: Check Frontend Staging App Logs

1. Go to CapRover → Apps → **multivendor-frontend-staging**
2. Click **Logs** tab
3. Look for:

**Good signs:**
- `Starting Nuxt build (STAGING)...`
- `Build completed! Checking .output folder...`
- `listening on port 3000`
- `Nuxt server started`

**Bad signs:**
- Build errors (npm errors, missing files)
- `Error: Cannot find module`
- Port binding errors
- Empty `.output` folder

### Step 4: Verify Environment Variables

1. Go to CapRover → Apps → **multivendor-frontend-staging**
2. Click **App Configs** → **Environment Variables**
3. Verify these are set:

```env
NUXT_PUBLIC_API_BASE=https://staging-api.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://staging.indexo.ir
NODE_ENV=production
NUXT_HOST=0.0.0.0
NUXT_PORT=3000
```

### Step 5: Check Port Configuration

1. Go to CapRover → Apps → **multivendor-frontend-staging**
2. Click **HTTP Settings** tab
3. Verify:
   - Container Port: `3000` (Nuxt default)
   - HTTPS is enabled
   - Custom domain: `staging.indexo.ir` (or your staging domain)

## 🔧 Common Issues & Fixes

### Issue 1: Frontend Workflow Never Ran

**Problem:** Backend workflow might have failed silently, or workflow trigger is broken.

**Fix:**
1. Check GitHub Actions → "Deploy Backend to Staging" - did it complete?
2. Manually trigger frontend workflow:
   - Go to Actions → "Deploy Frontend to Staging"
   - Click "Run workflow" → Select `staging` branch → Run

### Issue 2: Build Failed in Docker

**Problem:** Nuxt build failed during Docker build.

**Check logs for:**
- `npm ERR!` errors
- Missing dependencies
- Build timeout
- Memory issues

**Fix:** Check the Docker build logs in CapRover → App → Deployment tab

### Issue 3: Nuxt Server Not Starting

**Problem:** Build succeeded but server isn't running.

**Check logs for:**
- `Error: Cannot find module '.output/server/index.mjs'`
- Port already in use
- Missing environment variables

**Fix:**
- Verify `.output` folder exists after build
- Check port 3000 is not conflicting
- Ensure all env vars are set

### Issue 4: Wrong Port Configuration

**Problem:** CapRover is routing to wrong port.

**Fix:**
- CapRover HTTP Settings → Container Port should be `3000`
- App should listen on `0.0.0.0:3000` (Dockerfile already sets this)

### Issue 5: Environment Variables Missing

**Problem:** Nuxt can't find API base URL.

**Symptoms:**
- Empty page
- Console errors about API calls
- Runtime config errors

**Fix:**
- Add missing environment variables in CapRover app configs
- Restart the app after adding

## 🚀 Quick Fix: Force Redeploy

If nothing else works, force a fresh deployment:

1. **Via GitHub Actions:**
   - Go to Actions → "Deploy Frontend to Staging"
   - Click "Run workflow" → `staging` branch → Run

2. **Via CapRover (Manual):**
   - Go to App → **Deployment** tab
   - Upload tarball or trigger from GitHub branch

## 📋 What to Check in Logs

When checking logs, look for these patterns:

### ✅ Successful Deployment:
```
Starting Nuxt build (STAGING)...
NUXT_PUBLIC_API_BASE: https://staging-api.indexo.ir/api
NUXT_PUBLIC_SITE_URL: https://staging.indexo.ir
Build completed! Checking .output folder...
listening on port 3000
```

### ❌ Failed Deployment:
```
npm ERR!
Error: Cannot find module
Build failed
Port 3000 already in use
```




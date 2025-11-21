# SSR Instance Unavailable Fix - Deployment Guide

## Problem Summary

Your Nuxt frontend was experiencing the error:
```
Error: [nuxt] instance unavailable
    at useNuxtApp
    at useRuntimeConfig
    at useApiFetch
    at fetchProducts
```

This error occurs during Server-Side Rendering (SSR) when Nuxt composables (`useRuntimeConfig`, `useCookie`, etc.) are called before the Nuxt app instance is fully initialized.

## Root Cause

1. **SSR Timing Issue**: During SSR, when `useAsyncData` calls store actions that use `useApiFetch`, the Nuxt app context may not be available yet
2. **Missing Runtime Environment Variable**: The `NUXT_PUBLIC_API_BASE` was only set at build time, not at runtime in the Docker container

## Changes Made

### 1. Fixed `useApiFetch.ts` Composable
**File**: `/multivendor_platform/front_end/nuxt/composables/useApiFetch.ts`

**Changes**:
- Added `tryUseNuxtApp()` check to gracefully handle cases where Nuxt instance is not available
- Added fallback to environment variables when composables are not accessible
- Wrapped composable calls in try-catch for robust error handling

**Key improvements**:
```typescript
// Now handles SSR context gracefully
try {
  const nuxtApp = tryUseNuxtApp()
  if (nuxtApp) {
    // Use composables when available
    config = useRuntimeConfig()
    // ... get auth token from cookies
  } else {
    // Fallback to environment variables
    config = {
      public: {
        apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
      }
    }
  }
} catch (error) {
  // Additional fallback if composables fail
  config = { /* ... */ }
}
```

### 2. Updated Dockerfile
**File**: `/Dockerfile.frontend.nuxt`

**Changes**:
- Added `ENV NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api` in the production stage (line 61)
- This ensures the API base URL is available at runtime, not just build time

## Deployment Steps

### Step 1: Commit and Push Changes

```bash
cd /media/jalal/New\ Volume/project/mulitvendor_platform

# Check what changed
git status

# Add the changed files
git add multivendor_platform/front_end/nuxt/composables/useApiFetch.ts
git add Dockerfile.frontend.nuxt

# Commit with clear message
git commit -m "fix: resolve SSR 'nuxt instance unavailable' error

- Add graceful Nuxt instance availability check in useApiFetch
- Fallback to environment variables when composables unavailable
- Set NUXT_PUBLIC_API_BASE at Docker runtime for SSR
- Fixes infinite error loop during server-side rendering"

# Push to trigger CI/CD
git push origin main
```

### Step 2: Monitor GitHub Actions

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Watch the workflow run for the frontend build
4. Ensure the build completes successfully

### Step 3: Verify CapRover Deployment

1. Go to https://captain.indexo.ir/
2. Navigate to your frontend app
3. Check the "App Logs" to ensure:
   - No more "[nuxt] instance unavailable" errors
   - Server starts successfully with "Listening on http://[::]:3000"
   - No error loops

### Step 4: Test the Application

1. **Homepage Test**:
   ```bash
   curl -I https://indexo.ir/
   # Should return 200 OK without errors
   ```

2. **Browser Test**:
   - Open https://indexo.ir/
   - Check browser console for errors
   - Verify products load correctly
   - Test page navigation

3. **SSR Verification**:
   - View page source (Ctrl+U)
   - Verify that product data is rendered in the HTML (not just client-side)
   - Should see actual product content, not loading states

### Step 5: Monitor Server Logs

SSH into your server and check container logs:

```bash
ssh root@185.208.172.76

# Find your frontend container
docker ps | grep frontend

# Check logs (replace CONTAINER_ID with actual ID)
docker logs -f CONTAINER_ID --tail 100

# Should see:
# - "Listening on http://[::]:3000"
# - No "Error fetching products" messages
# - Clean startup without error loops
```

## Optional: Set Environment Variable in CapRover

If you want to be able to change the API base URL without rebuilding:

1. Go to CapRover dashboard: https://captain.indexo.ir/
2. Click on your frontend app
3. Go to "App Configs" tab
4. Add environment variable:
   - **Key**: `NUXT_PUBLIC_API_BASE`
   - **Value**: `https://multivendor-backend.indexo.ir/api`
5. Click "Save & Restart"

**Note**: The Dockerfile already sets this, so this step is optional. It's useful if you need to change backends or test different configurations.

## Troubleshooting

### If errors persist after deployment:

1. **Clear CapRover build cache**:
   ```bash
   # In CapRover UI, go to your app
   # Click "Force Rebuild" instead of regular deploy
   ```

2. **Check environment variables are set**:
   ```bash
   docker exec -it <container-id> env | grep NUXT_PUBLIC_API_BASE
   # Should output: NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
   ```

3. **Verify runtime config in container**:
   ```bash
   docker exec -it <container-id> cat /app/.output/server/config/nitro.json
   # Should contain apiBase configuration
   ```

4. **Check if backend is accessible**:
   ```bash
   curl -I https://multivendor-backend.indexo.ir/api/products/
   # Should return 200 OK
   ```

### Common Issues:

1. **"Connection refused" errors**: Backend might be down or unreachable
   - Check backend container is running
   - Verify network connectivity between containers

2. **Still seeing "instance unavailable"**: Old build might be cached
   - Force rebuild in CapRover
   - Clear browser cache
   - Try incognito/private browsing mode

3. **Products not loading**: API endpoint might have changed
   - Check Django backend API structure
   - Verify `/api/products/` endpoint exists and returns data

## Technical Details

### Why `tryUseNuxtApp()`?

Nuxt 3 provides `tryUseNuxtApp()` which safely checks if a Nuxt instance is available without throwing an error. This is crucial for:

- **SSR scenarios**: During initial server-side rendering
- **Edge cases**: When composables are called outside Vue setup context
- **Store actions**: When Pinia store actions are called during app initialization

### Environment Variable Priority

The application follows this priority for API base URL:

1. **Runtime environment variable** (from CapRover or Docker)
2. **Build-time environment variable** (from Dockerfile ARG)
3. **Fallback default**: `http://localhost:8000/api`

### SSR vs. Client-Side Rendering

- **SSR (Server)**: Uses environment variables directly, no window object
- **CSR (Client)**: Can access `localStorage` and `window` for auth tokens
- **Both**: Now gracefully handle missing Nuxt context

## Verification Checklist

After deployment, verify:

- [ ] Homepage loads without console errors
- [ ] Products are visible on the page
- [ ] No "[nuxt] instance unavailable" errors in server logs
- [ ] Page source shows rendered product data (View Source)
- [ ] Navigation works correctly
- [ ] Search functionality works
- [ ] Filters and pagination work
- [ ] Backend API is responding (check Network tab)

## Next Steps

Once deployed and verified:

1. Monitor error rates in production
2. Check performance metrics
3. Consider adding error tracking (e.g., Sentry)
4. Document any additional issues that arise

## Support

If you encounter issues:

1. Check the logs: `docker logs -f <container-id>`
2. Verify environment variables are set correctly
3. Ensure backend is accessible from frontend container
4. Check GitHub Actions for build errors

---

**Date**: 2025-01-21  
**Status**: Ready for Deployment  
**Tested**: Local SSR context handling  
**Impact**: Critical bug fix for production stability


# Quick Fix Commands - SSR Error Resolution

## 🚀 Quick Deploy (Copy & Paste)

```bash
# Navigate to project directory
cd "/media/jalal/New Volume/project/mulitvendor_platform"

# Add and commit the fixes
git add multivendor_platform/front_end/nuxt/composables/useApiFetch.ts
git add Dockerfile.frontend.nuxt
git add SSR_FIX_DEPLOYMENT_GUIDE.md
git add QUICK_FIX_COMMANDS.md
git add NITRO_CONFIG_FIX.md

git commit -m "fix(ssr): comprehensive fix for Nuxt instance unavailable error

**Problem**: 
- Nitro runtime config showing empty: config: {}
- useRuntimeConfig() failing during SSR
- Infinite error loop: 'nuxt instance unavailable'

**Solutions**:
1. Enhanced Dockerfile with better env var handling
2. Made useApiFetch SSR-safe with fallbacks
3. Added comprehensive debugging and verification

Fixes: #SSR-ERROR"

# Push to trigger deployment
git push origin main
```

## 📊 Monitor Deployment

### GitHub Actions Build Logs

Watch for these key indicators:

```
✅ "Verifying env vars are set:"
✅ "NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api"
✅ "NUXT_PUBLIC_SITE_URL=https://indexo.ir"
✅ "Checking nitro.json for runtime config..."
✅ Build completed successfully
```

### CapRover Deployment

```bash
# SSH into server
ssh root@185.208.172.76

# Find frontend container
docker ps | grep frontend

# Watch logs in real-time
docker logs -f <CONTAINER_ID> --tail 50

# Look for:
✅ "Listening on http://[::]:3000"
❌ NO "Error fetching products"
❌ NO "[nuxt] instance unavailable"
```

## ✅ Verify Fix

```bash
# 1. Find your container
CONTAINER_ID=$(docker ps | grep frontend | awk '{print $1}')

# 2. Test homepage
curl -I https://indexo.ir/
# Should return: HTTP/2 200

# 3. Check environment variables
docker exec -it $CONTAINER_ID env | grep NUXT
# Should show:
#   NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
#   NUXT_PUBLIC_SITE_URL=https://indexo.ir

# 4. Check for errors in logs
docker logs $CONTAINER_ID 2>&1 | grep "Error fetching products"
# Should return nothing (no errors)

# 5. Check startup is clean
docker logs $CONTAINER_ID --tail 20
# Should see: "Listening on http://[::]:3000"

# 6. Verify nitro config (even if empty, that's OK now)
docker exec -it $CONTAINER_ID cat /app/.output/nitro.json
```

## 🔧 If Still Having Issues

```bash
# Force rebuild in CapRover
# 1. Go to https://captain.indexo.ir/
# 2. Select your frontend app
# 3. Click "Force Rebuild" instead of normal deploy
# 4. Wait for completion

# Or manually restart container
docker restart <CONTAINER_ID>
```

## 📝 What Was Fixed

### 1. **useApiFetch.ts** - Made SSR-Safe
- Added `tryUseNuxtApp()` check
- Graceful fallback when Nuxt context unavailable
- Better error handling

### 2. **Dockerfile.frontend.nuxt** - Added Runtime ENV
- Set `NUXT_PUBLIC_API_BASE` at runtime
- Ensures API URL available during SSR

## 🎯 Expected Results

**Before Fix:**
```
Error fetching products: Error: [nuxt] instance unavailable
    at useNuxtApp (file:///app/.output/server/chunks/build/server.mjs:1:2768)
    at useRuntimeConfig (file:///app/.output/server/chunks/build/server.mjs:1:2854)
```

**After Fix:**
```
Listening on http://[::]:3000
```
(Clean startup, no errors)

## 🔍 Files Changed

1. `multivendor_platform/front_end/nuxt/composables/useApiFetch.ts`
2. `Dockerfile.frontend.nuxt`

## ⚡ Emergency Rollback

If the fix causes issues:

```bash
git revert HEAD
git push origin main
```

This will undo the changes and redeploy the previous version.

---

**Ready to deploy?** Just run the commands in the "Quick Deploy" section above! 🚀


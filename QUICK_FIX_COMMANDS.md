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

git commit -m "fix: resolve SSR 'nuxt instance unavailable' error

- Add graceful Nuxt instance check in useApiFetch
- Set NUXT_PUBLIC_API_BASE at Docker runtime
- Fixes infinite error loop during SSR"

# Push to trigger deployment
git push origin main
```

## 📊 Monitor Deployment

```bash
# Watch GitHub Actions
# Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions

# Or check CapRover logs directly
ssh root@185.208.172.76

# Find frontend container
docker ps | grep frontend

# Watch logs in real-time
docker logs -f <CONTAINER_ID> --tail 50
```

## ✅ Verify Fix

```bash
# Test homepage
curl -I https://indexo.ir/

# Should return: HTTP/2 200

# Check for errors in logs
docker logs <CONTAINER_ID> 2>&1 | grep "Error fetching products"
# Should return nothing (no errors)

# Check environment variable is set
docker exec -it <CONTAINER_ID> env | grep NUXT_PUBLIC_API_BASE
# Should output: NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
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


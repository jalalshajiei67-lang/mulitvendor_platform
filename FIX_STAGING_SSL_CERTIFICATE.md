# Fix SSL Certificate Error in Staging Frontend

## Problem
Frontend staging app fails with SSL certificate errors when making API calls:
```
Error: self-signed certificate
code: 'DEPTH_ZERO_SELF_SIGNED_CERT'
Error fetching categories for filters: FetchError: [GET] "https://staging-api.indexo.ir/api/categories/": <no response> fetch failed
```

## Root Cause
CapRover uses self-signed SSL certificates for staging domains. When Nuxt.js runs server-side (SSR), Node.js rejects these self-signed certificates by default.

## ✅ Solution Applied

### 1. Added Environment Variable to Dockerfile

Added `NODE_TLS_REJECT_UNAUTHORIZED=0` to `Dockerfile.frontend.staging.nuxt` to allow Node.js to accept self-signed certificates.

**File:** `Dockerfile.frontend.staging.nuxt`
```dockerfile
# Allow self-signed SSL certificates for staging (CapRover uses self-signed certs)
# ⚠️ Only for staging environment - do NOT use in production!
ENV NODE_TLS_REJECT_UNAUTHORIZED=0
```

### 2. Alternative: Set via CapRover Environment Variables

You can also set this via CapRover dashboard (if you prefer not to rebuild the image):

1. Go to CapRover → Apps → `multivendor-frontend-staging`
2. App Configs → Environment Variables
3. Add:
   ```
   NODE_TLS_REJECT_UNAUTHORIZED=0
   ```
4. Save & Update

## ⚠️ Important Security Note

**This setting disables SSL certificate validation!** 
- ✅ **Safe for staging environments** where you control the infrastructure
- ❌ **NEVER use in production** with real user data

For production, you should:
- Use properly signed SSL certificates (Let's Encrypt, etc.)
- Remove `NODE_TLS_REJECT_UNAUTHORIZED=0`

## Testing

After deploying:

1. Check frontend logs - should no longer see SSL errors
2. Visit `https://staging.indexo.ir`
3. Verify categories and API calls work

## Related Files

- `Dockerfile.frontend.staging.nuxt` - Staging-specific Dockerfile
- `multivendor_platform/front_end/nuxt/composables/useApiFetch.ts` - API fetch composable
- `multivendor_platform/front_end/nuxt/nuxt.config.ts` - Nuxt configuration




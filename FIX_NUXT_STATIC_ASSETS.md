# Fix for Nuxt Static Assets (NS_ERROR_CORRUPTED_CONTENT)

## Problem
Browser shows `NS_ERROR_CORRUPTED_CONTENT` and MIME type errors for `/_nuxt/` assets:
- CSS files return `application/json` instead of `text/css`
- JS files return `application/json` instead of `application/javascript`
- 404 errors for font files

## Root Cause
The Nuxt configuration had conflicting settings:
1. `features.inlineStyles: true` - Inlines styles but browser still requests separate files
2. `cssCodeSplit: false` - Prevents CSS code splitting
3. Client assets not being generated properly

## Changes Made

### 1. Updated `nuxt.config.ts`

**Changed CSS code splitting:**
```typescript
// Before
cssCodeSplit: false,

// After
cssCodeSplit: true,  // Generate separate CSS files
```

**Changed inline styles feature:**
```typescript
// Before
features: {
  inlineStyles: true
},

// After
features: {
  inlineStyles: false  // Generate separate asset files for better caching
},
```

## Solution

The frontend container needs to be **rebuilt** with the new configuration to generate the client assets properly.

### On VPS:

```bash
# SSH to VPS
ssh root@46.249.101.84

# Navigate to project directory
cd /root/multivendor_platform

# Rebuild frontend with new config
docker-compose -f docker-compose.production.yml build --no-cache frontend

# Restart frontend
docker-compose -f docker-compose.production.yml up -d frontend

# Wait for build to complete and check logs
docker logs multivendor_frontend --tail 50 -f
```

### Verify Assets Are Generated

After rebuild, check if assets are now generated:

```bash
# Check if CSS files are generated
docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.css" | head -10

# Check if JS files are generated
docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.js" | head -10

# Test if assets are accessible
curl -I https://indexo.ir/_nuxt/assets/style-*.css
```

### Expected Result

After rebuild, you should see:
- CSS files in `/app/.output/public/_nuxt/assets/`
- JS files in `/app/.output/public/_nuxt/chunks/` and `/app/.output/public/_nuxt/entry-*.js`
- Assets return correct MIME types (text/css, application/javascript)
- No more `NS_ERROR_CORRUPTED_CONTENT` errors

## Alternative: Quick Fix (If Rebuild Takes Too Long)

If you need a quick fix while waiting for rebuild, you can temporarily serve assets from nginx by mounting the frontend's `.output/public/_nuxt` directory, but rebuilding is the proper solution.

## Notes

- The changes are already applied to your local `nuxt.config.ts`
- You need to commit and push these changes, then rebuild on VPS
- The rebuild will take 5-10 minutes depending on your VPS resources


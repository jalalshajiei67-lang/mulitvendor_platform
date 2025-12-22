# Fix for Missing Nuxt Client Assets

## Problem
The Nuxt build was not generating client-side CSS/JS assets in `.output/public/_nuxt/`, causing 404 errors and MIME type mismatches in the browser.

## Root Cause
The build configuration was missing explicit settings to ensure:
1. CSS extraction (not inlining)
2. Proper Nitro public asset configuration
3. Client bundle generation

## Changes Made

### 1. Updated `nuxt.config.ts`

**Added Nitro publicAssets configuration:**
```typescript
nitro: {
  // ... existing config ...
  publicAssets: [
    {
      baseURL: '/_nuxt/',
      dir: 'public/_nuxt',
      maxAge: 31536000
    }
  ],
  // ... rest of config ...
}
```

**Added CSS code splitting:**
```typescript
vite: {
  build: {
    // ... existing config ...
    cssCodeSplit: true,  // Ensure CSS is extracted
    // ... rest of config ...
  }
}
```

**Removed duplicate `app` section** that was causing configuration conflicts.

## Next Steps

### Rebuild the Frontend Container

On your VPS, run:

```bash
cd ~/indexo-production

# Rebuild frontend with no cache to ensure clean build
docker-compose -f docker-compose.production.yml build --no-cache frontend

# Restart the frontend container
docker-compose -f docker-compose.production.yml up -d frontend

# Check logs to verify build succeeded
docker logs multivendor_frontend --tail 50 -f
```

### Verify Assets Are Generated

After rebuild, verify assets exist:

```bash
# Check if CSS files are now generated
docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.css" | head -10

# Check if JS files are now generated
docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.js" | head -10

# Test if Nuxt can serve them
docker exec multivendor_frontend curl -I http://localhost:3000/_nuxt/entry-*.js 2>/dev/null | head -5
```

### Expected Result

After rebuild, you should see:
- CSS files in `/app/.output/public/_nuxt/assets/`
- JS files in `/app/.output/public/_nuxt/chunks/` and `/app/.output/public/_nuxt/entry-*.js`
- Browser should load assets without 404 errors
- No more MIME type mismatch errors

## Notes

- The build process may take 5-10 minutes depending on your VPS resources
- Ensure you have at least 2GB RAM available for the build
- If build fails due to memory, add swap space to your VPS
- The `--no-cache` flag ensures a clean build with the new configuration


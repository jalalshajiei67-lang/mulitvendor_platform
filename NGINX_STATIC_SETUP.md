# CapRover Volume + Nginx Caching Setup Guide

This guide explains how to set up a dedicated Nginx static server with caching for serving static and media files in CapRover.

## Architecture Overview

```
┌─────────────────┐
│  CapRover Nginx │  (Reverse Proxy)
│  (captain nginx)│
└────────┬────────┘
         │
         ├─── /static/* ───> Nginx Static Server (with caching)
         │
         └─── /media/*  ───> Nginx Static Server (with caching)
         │
         └─── /api/*    ───> Django Backend App
```

## Step 1: Configure Backend App Persistent Directories

In CapRover Dashboard → Your Backend App → App Configs → Persistent Directories:

1. **Add Static Files Directory:**
   - Path in App: `/app/staticfiles`
   - Label: `backend-static-files`
   - Click "Set specific host path" → `/captain/data/backend-static`

2. **Add Media Files Directory:**
   - Path in App: `/app/media`
   - Label: `backend-media-files`
   - Click "Set specific host path" → `/captain/data/backend-media`

3. Click **"Save & Restart"**

## Step 2: Create Nginx Static Server App

1. In CapRover Dashboard, click **"One-Click Apps/Databases"**
2. Click **"Custom App"**
3. App Name: `nginx-static-server` (or `multivendor-static`)
4. Click **"Create New App"**

## Step 3: Configure Nginx Static Server

1. Go to the new app → **App Configs**
2. **Build Method:** Select "Dockerfile"
3. **Dockerfile Path:** `./Dockerfile.nginx-static`
4. **Repository:** Your GitHub repository URL

### Add Persistent Directories

In the Nginx Static Server app → Persistent Directories:

1. **Add Static Files Mount:**
   - Path in App: `/captain/data/backend-static`
   - Label: `static-files`
   - Click "Set specific host path" → `/captain/data/backend-static`

2. **Add Media Files Mount:**
   - Path in App: `/captain/data/backend-media`
   - Label: `media-files`
   - Click "Set specific host path" → `/captain/data/backend-media`

3. Click **"Save & Restart"**

## Step 4: Configure HTTP Settings

1. In the Nginx Static Server app → **HTTP Settings**
2. **Enable HTTPS** (if you have SSL certificates)
3. **Domain:** Set a subdomain like `static.indexo.ir` (optional, or use routing)

### Option A: Use CapRover Routing (Recommended)

In your **Backend App** → **HTTP Settings** → **Custom Nginx Configuration**, add:

```nginx
# Route static files to Nginx static server
location /static/ {
    proxy_pass http://nginx-static-server;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Route media files to Nginx static server
location /media/ {
    proxy_pass http://nginx-static-server;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### Option B: Use Separate Domain

If you set up a separate domain (e.g., `static.indexo.ir`), update your Django settings:

```python
# In settings_caprover.py or environment variables
STATIC_URL = 'https://static.indexo.ir/static/'
MEDIA_URL = 'https://static.indexo.ir/media/'
```

## Step 5: Deploy and Test

1. **Deploy Backend App:**
   ```bash
   # Make sure collectstatic runs during deployment
   # This is already in Dockerfile.backend CMD
   ```

2. **Deploy Nginx Static Server:**
   - Push your code to GitHub
   - In CapRover, trigger deployment for `nginx-static-server` app

3. **Verify Static Files:**
   ```bash
   # Check if files are in the volume
   # You can exec into the backend container:
   ls -la /app/staticfiles/
   ls -la /app/media/
   ```

4. **Test Endpoints:**
   - Visit: `https://your-domain.com/static/admin/css/base.css`
   - Visit: `https://your-domain.com/media/product_images/example.jpg`
   - Check response headers for `X-Cache-Status: HIT` or `MISS`

## Step 6: Verify Caching

1. **Check Cache Headers:**
   ```bash
   curl -I https://your-domain.com/static/admin/css/base.css
   # Should see: Cache-Control: public, immutable
   # Should see: Expires: (1 year from now)
   ```

2. **Verify File Serving:**
   ```bash
   # Request should return 200 OK with file content
   curl -I https://your-domain.com/media/product_images/example.jpg
   # Should see: Cache-Control: public, max-age=604800
   ```

## Configuration Details

### Cache Settings

- **Static Files Cache:**
  - Browser Cache: 1 year (`Cache-Control: public, immutable`)
  - Open File Cache: 10,000 files, 60s validity
  - Optimized for static assets that don't change

- **Media Files Cache:**
  - Browser Cache: 7 days (`Cache-Control: public, max-age=604800`)
  - Open File Cache: 10,000 files, 60s validity
  - Shorter cache for user-uploaded content that may change

### Cache Invalidation

Since we're using browser caching (not proxy cache), cache invalidation happens via:

1. **Browser Cache:** Users need to clear browser cache or wait for expiration
2. **File Versioning:** Add version/hash to filenames (e.g., `style-v1.2.3.css`)
3. **For Static Files:** Run `collectstatic` with `--clear` flag to force new files
4. **For Media Files:** Update file modification time or use unique filenames

## Troubleshooting

### Files Not Found (404)

1. **Check Persistent Directories:**
   - Verify both apps have the same host paths
   - Check that files exist in `/captain/data/backend-static`

2. **Check Backend Collectstatic:**
   ```bash
   # In backend app, run:
   python manage.py collectstatic --noinput
   ```

3. **Check Nginx Logs:**
   ```bash
   # In CapRover, check nginx-static-server logs
   # Look for errors in static-error.log or media-error.log
   ```

### Cache Not Working

1. **Check Cache Headers:**
   ```bash
   curl -I https://your-domain.com/static/admin/css/base.css
   # Should see: Cache-Control: public, immutable
   # Should see: Expires header
   ```

2. **Verify File Serving:**
   ```bash
   # Check if files are being served correctly
   curl -I https://your-domain.com/static/admin/css/base.css
   # Should return 200 OK, not 404
   ```

### Performance Issues

1. **Increase Cache Size:**
   - Edit `nginx/static-server.conf`
   - Increase `max_size` in `proxy_cache_path`

2. **Adjust Worker Processes:**
   - Edit `nginx/static-server.conf`
   - Set `worker_processes` to match CPU cores

## Benefits of This Setup

✅ **Performance:** Nginx serves static files much faster than Django  
✅ **Caching:** Reduces load on backend and improves response times  
✅ **Scalability:** Can handle high traffic for static content  
✅ **Separation:** Static serving separated from application logic  
✅ **CDN-Ready:** Easy to add CDN layer later  

## Comparison with Backend-Only Setup

| Feature | Backend Only | Nginx + Volume |
|---------|--------------|----------------|
| Static File Serving | Django/Gunicorn | Nginx (optimized) |
| Caching | None | Built-in proxy cache |
| Response Time | Slower | Faster |
| Backend Load | Higher | Lower |
| Scalability | Limited | Better |
| Setup Complexity | Simple | Moderate |

## Next Steps

1. ✅ Set up persistent directories
2. ✅ Deploy Nginx static server
3. ✅ Configure routing
4. ✅ Monitor cache hit rates
5. 🔄 Consider adding CDN layer (Cloudflare, etc.)


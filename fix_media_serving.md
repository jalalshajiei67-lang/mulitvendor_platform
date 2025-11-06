# Fix Media File Serving Issue

## Problem
Media files (images) are returning HTML error pages (179 bytes) instead of actual images when accessed via `/media/category_images/road-sign-361513_1280.webp`.

## Root Cause
1. Media files are not being properly served by Django in production
2. The media directory might not exist or have incorrect permissions
3. CapRover might need persistent volume configuration for media files

## Solution

### Option 1: Ensure Media Directory Exists and Has Proper Permissions

Add to your Dockerfile.backend CMD to create media directories:

```dockerfile
CMD python manage.py migrate --noinput && \
    mkdir -p /app/media/category_images /app/media/subcategory_images /app/media/product_images /app/media/department_images && \
    chmod -R 755 /app/media && \
    python manage.py collectstatic --noinput --clear && \
    gunicorn multivendor_platform.wsgi:application --bind 0.0.0.0:80 --workers 4 --timeout 120
```

### Option 2: Configure CapRover Persistent Volume

In CapRover dashboard:
1. Go to your backend app
2. Add a persistent volume: `/app/media` → `/captain/data/backend-media`
3. This ensures media files persist across deployments

### Option 3: Verify Django Media Serving

The Django URLs already handle media serving in production (lines 76-78 in urls.py), but we need to ensure:
1. MEDIA_ROOT exists: `/app/media`
2. Files are uploaded to the correct location
3. Django has permission to read files

### Quick Fix: Check Media Directory

SSH into your server and check:
```bash
# Inside the backend container
ls -la /app/media/
ls -la /app/media/category_images/
```

If files don't exist, you may need to:
1. Upload media files to the server
2. Or sync from a backup
3. Or re-upload through Django admin

## Immediate Action Items

1. **Check if media files exist on server**
2. **Add persistent volume in CapRover for `/app/media`**
3. **Ensure media directory structure exists**
4. **Verify file permissions (755 or 644)**



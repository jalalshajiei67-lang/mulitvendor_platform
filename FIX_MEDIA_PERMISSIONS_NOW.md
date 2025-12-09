# 🔧 Fix Media Upload Permission Error

## The Problem

```
PermissionError: [Errno 13] Permission denied: '/app/media/product_images/1_ciEJCGd.jpg'
```

The backend container can't write to the `/app/media/` directory because of incorrect file permissions.

## Quick Fix (Run on Server)

### Step 1: Upload and Run the Fix Script

**From your local machine:**
```powershell
scp fix-media-permissions.sh root@185.208.172.76:/home/deploy/docker-deploy/
```

**On the server:**
```bash
cd /home/deploy/docker-deploy
chmod +x fix-media-permissions.sh
sed -i 's/\r$//' fix-media-permissions.sh  # Fix line endings
./fix-media-permissions.sh
```

### Step 2: Manual Fix (If Script Doesn't Work)

```bash
# Fix permissions directly
docker exec -u root multivendor_backend chmod -R 777 /app/media
docker exec -u root multivendor_backend chown -R appuser:appuser /app/media

# Create subdirectories if they don't exist
docker exec multivendor_backend mkdir -p /app/media/product_images
docker exec multivendor_backend mkdir -p /app/media/category_images
docker exec multivendor_backend mkdir -p /app/media/subcategory_images
docker exec multivendor_backend mkdir -p /app/media/department_images
docker exec multivendor_backend mkdir -p /app/media/blog_images
docker exec multivendor_backend mkdir -p /app/media/user_images

# Set permissions on subdirectories
docker exec -u root multivendor_backend chmod -R 755 /app/media
docker exec -u root multivendor_backend chown -R appuser:appuser /app/media
```

### Step 3: Verify It Works

```bash
# Test write access
docker exec multivendor_backend touch /app/media/test.txt
docker exec multivendor_backend rm /app/media/test.txt

# If that works, try uploading an image in Django admin
```

## Permanent Fix: Update Dockerfile

To prevent this issue in future deployments, we should ensure the media directory has correct permissions on container startup. However, since you're using volumes, the volume permissions take precedence.

## Why This Happens

1. Docker volumes are created with root ownership by default
2. Your container runs as `appuser` (non-root for security)
3. When the volume is mounted, `appuser` can't write to it

## Long-term Solution

Update your `docker-compose.production.yml` command to fix permissions on startup:

```yaml
command: >
  sh -c "python manage.py migrate --noinput &&
         python manage.py collectstatic --noinput &&
         mkdir -p /app/media/product_images /app/media/category_images &&
         chmod -R 755 /app/media &&
         daphne -b 0.0.0.0 -p 8000 --application-close-timeout 60 multivendor_platform.asgi:application"
```

But this requires running as root initially, which we want to avoid. The script approach is safer.



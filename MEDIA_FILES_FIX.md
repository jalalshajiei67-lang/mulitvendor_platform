# Media Files Serving Fix

## Problem
Media files return HTML error pages (179 bytes) instead of images when accessed via `/media/category_images/road-sign-361513_1280.webp`.

## Root Cause
1. Media subdirectories may not exist in `/app/media/`
2. Media files might not be uploaded to the server
3. CapRover needs persistent volume for media files (to survive deployments)

## Solutions Applied

### 1. Updated Dockerfile.backend
- Creates all required media subdirectories on container start
- Sets proper permissions (755) for media directory
- Ensures directories exist: `category_images`, `subcategory_images`, `product_images`, `department_images`, `blog_images`, `user_images`

### 2. CapRover Persistent Volume Setup (REQUIRED)

**Important:** Media files will be lost on redeployment unless you configure a persistent volume in CapRover.

#### Steps:
1. Go to CapRover dashboard: https://captain.indexo.ir/
2. Select your backend app (`multivendor-backend` or similar)
3. Go to **App Configs** → **Volumes**
4. Add a persistent volume:
   - **Container Path:** `/app/media`
   - **Volume Name:** `backend-media` (or any name)
   - Click **Save & Update**

This ensures media files persist across deployments.

### 3. Verify Media Files Exist

After deployment, check if files exist:

```bash
# Via CapRover terminal or SSH
docker exec -it <backend-container-name> ls -la /app/media/category_images/
```

If files don't exist, you need to:
1. Upload them through Django admin
2. Or restore from backup
3. Or sync from development environment

### 4. Check Django Admin

1. Go to https://multivendor-backend.indexo.ir/admin/
2. Check if categories/departments have images uploaded
3. If images show in admin but not on frontend, check URL configuration

## Testing

After applying fixes:

1. **Deploy updated Dockerfile.backend**
2. **Configure persistent volume in CapRover**
3. **Verify media directories exist:**
   ```bash
   docker exec <container> ls -la /app/media/
   ```
4. **Test image URL:**
   ```
   https://multivendor-backend.indexo.ir/media/category_images/road-sign-361513_1280.webp
   ```

## Expected Behavior

- Image URLs should return `Content-Type: image/webp` (or appropriate image type)
- File size should match actual image size (not 179 bytes)
- Images should display correctly on frontend

## Troubleshooting

If still not working:

1. **Check Django logs:**
   ```bash
   docker logs <backend-container-name>
   ```

2. **Verify MEDIA_ROOT setting:**
   - Should be `/app/media` in production

3. **Check file permissions:**
   ```bash
   docker exec <container> ls -la /app/media/
   ```
   - Should show `drwxr-xr-x` for directories

4. **Test direct file access:**
   ```bash
   docker exec <container> cat /app/media/category_images/road-sign-361513_1280.webp | head -c 100
   ```
   - Should output binary data, not HTML

## Next Steps

1. ✅ Updated Dockerfile.backend (creates directories)
2. ⚠️ **Configure CapRover persistent volume** (CRITICAL - prevents data loss)
3. ⚠️ **Verify/upload media files** (if missing)
4. ✅ Deploy and test


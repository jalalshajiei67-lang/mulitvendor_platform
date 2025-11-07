# CapRover Persistent Data Setup Guide

## ⚠️ Important Note
Persistent directories cannot be configured in `captain-definition-backend` file. 
They must be configured through the CapRover Dashboard UI.

## Quick Setup Steps

### 1. Access CapRover Dashboard
- Go to: https://captain.indexo.ir/
- Log in with your credentials

### 2. Configure Backend App
1. Find your backend app (e.g., `multivendor-backend`)
2. Click on the app name
3. Go to **App Configs** tab
4. Scroll to **Persistent Directories** section

### 3. Enable Persistent Data
1. Toggle **"Has Persistent Data"** to **ON**
2. Click **"Add Directory"** button
3. Enter: `/app/media`
4. Click **Save & Update**

### 4. Verify Configuration
After saving, CapRover will:
- Create a persistent volume for `/app/media`
- Redeploy your app with the volume mounted
- Preserve any existing files in that directory

## What Gets Persisted

The following directories will persist across deployments:
- `/app/media/category_images/` - Category images
- `/app/media/subcategory_images/` - Subcategory images  
- `/app/media/product_images/` - Product images
- `/app/media/department_images/` - Department images
- `/app/media/blog_images/` - Blog post images
- `/app/media/user_images/` - User profile images

## Verification

After configuration:

1. **Upload a test image** through Django admin
2. **Check it displays** correctly on the frontend
3. **Trigger a deployment** (push new code or manually redeploy)
4. **Verify the image still exists** after deployment

## Troubleshooting

### Images still disappear after deployment?
- Verify "Has Persistent Data" is enabled
- Check that `/app/media` is listed in Persistent Directories
- Ensure you clicked "Save & Update" after adding the directory
- Check CapRover logs for volume mount errors

### Can't find Persistent Directories option?
- Make sure you're in **App Configs** tab (not Build Settings)
- Scroll down to find the **Persistent Directories** section
- If still not visible, your CapRover version might need updating

### Permission errors?
- CapRover handles permissions automatically
- If issues persist, check Docker logs: `docker logs <container-name>`

## Important Notes

- ⚠️ **First-time setup**: After adding persistent directory, existing files in the container will be lost. You'll need to re-upload images.
- ⚠️ **Scaling limitation**: Apps with persistent data cannot be scaled to multiple instances (data corruption risk)
- ✅ **Backup recommended**: Regularly backup `/app/media` directory to prevent data loss

## Alternative: External Storage

For production, consider using external storage (S3, Azure Blob, etc.) with `django-storages` package. This allows:
- Multiple app instances
- Better scalability
- Automatic backups
- CDN integration

See Django Storages documentation for setup.






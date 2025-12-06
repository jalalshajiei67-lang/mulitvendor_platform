# Static Files Persistent Volume Setup for CapRover

## ⚠️ Problem Without Persistent Static Files

Currently, your static files are stored in `/app/staticfiles` inside the container. This causes:

1. **Slow Deployments**: `collectstatic` runs on every container restart (10-30+ seconds)
2. **Downtime**: Static files unavailable during deployment
3. **Resource Waste**: Unnecessary CPU/disk I/O on every restart
4. **Poor Performance**: Admin CSS/JS, TinyMCE, and other static assets must be regenerated

## ✅ Solution: Add Persistent Volume for Static Files

### Step 1: Configure Persistent Directory in CapRover

1. **Access CapRover Dashboard**
   - Go to: https://captain.indexo.ir/
   - Log in with your credentials

2. **Open Backend App**
   - Find your backend app: `multivendor-backend`
   - Click on the app name
   - Go to **App Configs** tab

3. **Add Persistent Directory for Static Files**
   - Scroll to **Persistent Directories** section
   - Toggle **"Has Persistent Data"** to **ON** (if not already enabled)
   - Click **"Add Directory"** button
   - Enter: `/app/staticfiles`
   - Click **"Set specific host path"** (optional but recommended)
   - Enter: `/captain/data/backend-static`
   - Label: `static-files` (optional)
   - Click **Save & Update**

### Step 2: Optimize Dockerfile (Optional but Recommended)

After setting up persistent volume, you can optimize the startup script to skip `collectstatic` if files already exist:

**Current behavior**: Always runs `collectstatic` (slow)
**Optimized behavior**: Only runs if static files are missing (fast)

However, for now, keeping `collectstatic` in the startup is safe and ensures files are always up-to-date.

### Step 3: Verify Configuration

After saving, CapRover will:
- Create a persistent volume for `/app/staticfiles`
- Redeploy your app with the volume mounted
- Preserve static files across deployments

**Test it:**
1. Deploy your app
2. Wait for `collectstatic` to complete (first time only)
3. Check static files are accessible: `https://multivendor-backend.indexo.ir/static/admin/css/base.css`
4. Trigger a new deployment
5. Verify static files are still accessible immediately (no waiting for `collectstatic`)

## 📊 Comparison: Before vs After

| Aspect | Without Persistent Volume | With Persistent Volume |
|--------|---------------------------|------------------------|
| **Deployment Time** | 30-60 seconds (collectstatic runs) | 5-10 seconds (skips if exists) |
| **Static Files Availability** | Unavailable during collectstatic | Always available |
| **Resource Usage** | High (every restart) | Low (only on first deploy) |
| **User Experience** | Admin may be broken during deploy | Smooth, no interruption |

## 🔧 Advanced: Optimize Startup Script

If you want to optimize further, you can modify the Dockerfile to check if static files exist before running `collectstatic`:

```dockerfile
# In Dockerfile.backend CMD section, replace collectstatic line with:
echo "[3/5] Checking static files..." && \
if [ -z "$(ls -A /app/staticfiles 2>/dev/null)" ]; then \
    echo "Static files directory is empty, collecting..." && \
    python manage.py collectstatic --noinput --clear || echo "⚠️  Collectstatic failed, but continuing..."; \
else \
    echo "Static files exist, skipping collectstatic (use --force to regenerate)"; \
fi && \
echo "✅ Static files ready"
```

**Note**: This optimization is optional. The current setup works fine, it just takes a bit longer on each deployment.

## ⚠️ Important Notes

1. **First Deployment**: After adding persistent directory, the first deployment will still run `collectstatic` (directory is empty)

2. **Scaling Limitation**: Apps with persistent data cannot be scaled to multiple instances. If you need scaling, consider:
   - Using external storage (S3, Azure Blob) with `django-storages`
   - Using a CDN for static files
   - Using a separate Nginx static server (see `NGINX_STATIC_SETUP.md`)

3. **Media Files**: Make sure `/app/media` also has a persistent volume (for user uploads)

4. **Backup**: Consider backing up `/captain/data/backend-static` periodically

## 🚀 Quick Setup Checklist

- [ ] Access CapRover Dashboard
- [ ] Open backend app → App Configs
- [ ] Enable "Has Persistent Data"
- [ ] Add persistent directory: `/app/staticfiles` → `/captain/data/backend-static`
- [ ] Save & Update
- [ ] Verify static files are accessible after deployment
- [ ] Test by triggering a new deployment

## 📝 Current Configuration

Your current static files configuration:
- **STATIC_ROOT**: `/app/staticfiles` (inside container)
- **STATIC_URL**: `/static/`
- **Persistent Volume**: Not configured ❌

**After setup:**
- **STATIC_ROOT**: `/app/staticfiles` (mounted to persistent volume)
- **STATIC_URL**: `/static/`
- **Persistent Volume**: `/captain/data/backend-static` ✅

## 🆘 Troubleshooting

### Static files still not persisting?
- Verify "Has Persistent Data" is enabled
- Check that `/app/staticfiles` is listed in Persistent Directories
- Ensure you clicked "Save & Update" after adding the directory
- Check CapRover logs for volume mount errors

### Permission errors?
- CapRover handles permissions automatically
- If issues persist, check Docker logs: `docker logs <container-name>`

### Still running collectstatic every time?
- This is normal if you want to ensure files are always up-to-date
- To optimize, use the advanced startup script modification above

---

**Last Updated**: 2025-01-27
**Status**: Ready to implement


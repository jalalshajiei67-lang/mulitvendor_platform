# Fix: 502 Bad Gateway After Adding Persistent Volumes

## Problem Summary
After adding persistent volumes for `/app/staticfiles` and `/app/media` in CapRover, the backend application returns 502 Bad Gateway errors, indicating the application is not starting.

## Root Causes
1. **Permission Issues**: Persistent volumes might be mounted with incorrect permissions
2. **Missing Directories**: Subdirectories within media might not exist
3. **Logging Failures**: The application tries to write logs but the directory might not be writable
4. **Collectstatic Issues**: Using `--clear` flag might cause issues with persistent volumes

## Solutions Applied

### 1. Updated Dockerfile.backend
- Removed `--clear` flag from collectstatic to preserve existing files
- Added directory permission checks at startup
- Ensured all required directories are created with proper permissions
- Added permission testing to diagnose issues

### 2. Updated settings_caprover.py
- Made logging configuration resilient (falls back to console-only if file logging fails)
- Prevents application crashes due to logging directory issues

## CapRover Persistent Volume Configuration

### Correct Volume Mounts
In CapRover, configure these persistent volumes for the `multivendor-backend` app:

1. **Static Files Volume**:
   - Container Path: `/app/staticfiles`
   - Volume Name: `multivendor-backend-staticfiles` (or any unique name)

2. **Media Files Volume**:
   - Container Path: `/app/media`
   - Volume Name: `multivendor-backend-media` (or any unique name)

3. **Optional - Logs Volume** (recommended):
   - Container Path: `/app/logs`
   - Volume Name: `multivendor-backend-logs` (or any unique name)

### Steps to Configure in CapRover

1. **Go to CapRover Dashboard**: https://captain.indexo.ir/
2. **Select the App**: Click on `multivendor-backend`
3. **Go to Volumes Tab**: Click on "Persistent Directories" or "Volumes"
4. **Add Volumes**:
   - Click "Add New Persistent Directory"
   - Container Path: `/app/staticfiles`
   - Click "Add"
   - Repeat for `/app/media`
   - Optionally add `/app/logs`

### Important Notes

⚠️ **After adding volumes, you MUST:**
1. **Redeploy the application** - The changes require a new deployment
2. **Check container logs** - Verify the application starts successfully
3. **Verify permissions** - The startup script will test and report permissions

### Verifying the Fix

After deploying, check the container logs:

```bash
# In CapRover, go to App Details > View Logs
# Or use CapRover CLI
caprover logs multivendor-backend
```

Look for these messages:
- ✅ `Directories ready`
- ✅ `Media directory is writable`
- ✅ `Logs directory is writable`
- ✅ `Starting Gunicorn server...`

If you see warnings about permissions, the volumes might need to be recreated or permissions adjusted.

## Troubleshooting

### If 502 Error Persists

1. **Check Container Status**:
   - In CapRover, verify the container is running
   - Check if it's restarting (crash loop)

2. **View Container Logs**:
   - Look for Python errors or permission denied messages
   - Check if migrations are failing

3. **Test Volume Permissions**:
   - The startup script now tests permissions
   - Look for permission warnings in logs

4. **Verify Volume Mounts**:
   - In CapRover, check if volumes are properly mounted
   - Ensure container paths match exactly: `/app/staticfiles` and `/app/media`

### If Images Still Disappear

1. **Check Media Directory Permissions**:
   - Files must be writable by the application user
   - The startup script sets permissions to 777 (readable by all)

2. **Verify Uploads Are Saving**:
   - Check if files are being saved to `/app/media/`
   - Files should persist after container restarts

3. **Check Static Files**:
   - Verify `collectstatic` runs successfully
   - Static files should be in `/app/staticfiles/`

## Next Steps

1. **Commit and Push Changes**:
   ```bash
   git add .
   git commit -m "Fix: Handle persistent volumes with proper permissions and resilient logging"
   git push
   ```

2. **Wait for CI/CD Deployment**:
   - GitHub Actions will automatically deploy
   - Or manually trigger deployment in CapRover

3. **Monitor Deployment**:
   - Watch the deployment logs in CapRover
   - Verify the application starts successfully
   - Test API endpoints

4. **Verify Image Persistence**:
   - Upload a test image
   - Restart the container
   - Verify the image still exists

## Prevention

To prevent similar issues in the future:
- Always test persistent volume configurations locally first
- Use the permission testing in the startup script
- Monitor container logs after deployment
- Consider using a separate volume for logs
- Regularly backup persistent volumes


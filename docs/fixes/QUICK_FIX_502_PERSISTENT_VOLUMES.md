# Quick Fix: 502 Error After Adding Persistent Volumes

## What Was Fixed

✅ **Dockerfile.backend**: 
- Removed `--clear` flag from collectstatic (was deleting files in persistent volumes)
- Added permission checks and directory creation at startup
- Added permission testing to diagnose issues

✅ **settings_caprover.py**:
- Made logging resilient (falls back to console if file logging fails)
- Prevents crashes due to unwritable log directory

## What You Need to Do

### 1. Commit and Push Changes
```bash
git add .
git commit -m "Fix: Handle persistent volumes with proper permissions"
git push
```

### 2. Verify CapRover Volume Configuration

In CapRover Dashboard (https://captain.indexo.ir/):

**For `multivendor-backend` app, ensure these volumes are configured:**

- Container Path: `/app/staticfiles` → Persistent Volume
- Container Path: `/app/media` → Persistent Volume  
- Container Path: `/app/logs` → Persistent Volume (optional but recommended)

### 3. Monitor Deployment

After pushing, watch the deployment:
1. Go to CapRover Dashboard
2. Click on `multivendor-backend` app
3. Go to "Deployment" tab
4. Watch the logs

### 4. Check Startup Logs

Look for these success messages:
- ✅ `Directories ready`
- ✅ `Media directory is writable`
- ✅ `Starting Gunicorn server...`

If you see permission warnings, the volumes may need to be recreated.

### 5. Test the Application

1. Check health endpoint: `https://multivendor-backend.indexo.ir/health/`
2. Test API: `https://multivendor-backend.indexo.ir/api/departments/`
3. Upload a test image and verify it persists

## If 502 Error Still Persists

1. **Check Container Status**: Is it running or restarting?
2. **View Logs**: Look for Python errors or permission issues
3. **Verify Volumes**: Check if volumes are properly mounted in CapRover
4. **Try Removing and Re-adding Volumes**: Sometimes volumes need to be recreated

## Expected Behavior After Fix

- ✅ Application starts successfully
- ✅ No 502 errors
- ✅ Images persist after container restarts
- ✅ Static files are served correctly
- ✅ CORS works properly (once app is running)

## Important Notes

- The persistent volumes must be configured in CapRover BEFORE or DURING deployment
- After adding volumes, you MUST redeploy the application
- The startup script will automatically create required subdirectories
- Permission issues will be reported in the startup logs


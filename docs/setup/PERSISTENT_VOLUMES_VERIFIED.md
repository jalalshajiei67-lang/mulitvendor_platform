# Persistent Volumes Configuration - VERIFIED ✅

## ✅ Current Configuration (CORRECT)

Your persistent directories are now correctly configured:

| Path in App | Host Path | Status |
|-------------|-----------|--------|
| `/app/staticfiles` | `/captain/data/backend-static` | ✅ Correct |
| `/app/media` | `/captain/data/backend-media` | ✅ Correct |

## 🎯 Next Steps

### Step 1: Save Configuration

1. **Scroll down** in CapRover Dashboard
2. Click **"Save & Update"** or **"Save & Restart"**
3. **Wait 2-3 minutes** for CapRover to:
   - Create the host directories
   - Mount the volumes
   - Redeploy the container

### Step 2: Verify Container Status

After deployment, check if backend is running:

**Via CapRover Dashboard:**
- Go to Apps → `multivendor-backend`
- Status should show **green** (Running)
- Should show `1/1` replicas

**Via SSH (if needed):**
```bash
ssh root@185.208.172.76
docker ps | grep multivendor-backend
```

**Expected output:**
```
srv-captain--multivendor-backend   replicated   1/1   ...   Up X minutes
```

**Not:**
```
srv-captain--multivendor-backend   replicated   0/1   ...   (crashed)
```

### Step 3: Check App Logs

1. Go to CapRover Dashboard → Backend App → **App Logs**
2. You should see:
   - ✅ Startup messages
   - ✅ "Starting Multivendor Backend Application"
   - ✅ "Static files collected"
   - ✅ "Gunicorn server started"

### Step 4: Test Persistent Volumes

**Test Static Files:**
1. Visit: `https://multivendor-backend.indexo.ir/static/admin/css/base.css`
2. Should return 200 OK (not 404)

**Test Media Files:**
1. Upload an image through Django admin
2. Trigger a deployment (push new code or restart)
3. Verify the image still exists after deployment

## ✅ What This Configuration Does

### Static Files (`/app/staticfiles` → `/captain/data/backend-static`)
- ✅ Static files persist across deployments
- ✅ No need to run `collectstatic` on every restart (faster deployments)
- ✅ Admin CSS/JS, TinyMCE, DRF static files are preserved

### Media Files (`/app/media` → `/captain/data/backend-media`)
- ✅ User uploads persist across deployments
- ✅ Product images, category images, user avatars are preserved
- ✅ No data loss on redeployment

## 🔍 Troubleshooting

### If Container Still Shows 0/1:

1. **Check Build Logs:**
   - CapRover Dashboard → Backend App → Build Logs
   - Look for volume mount errors

2. **Check App Logs:**
   - Look for Python errors
   - Look for permission errors
   - Look for import errors

3. **Verify Host Paths Exist:**
   ```bash
   ssh root@185.208.172.76
   ls -la /captain/data/backend-static
   ls -la /captain/data/backend-media
   ```
   - CapRover creates these automatically
   - Should show directories (may be empty initially)

4. **Check Disk Space:**
   ```bash
   df -h /captain/data
   ```
   - Ensure you have enough disk space

### If Logs Are Empty:

1. **Wait 1-2 minutes** after deployment
2. **Refresh** the logs page
3. **Check Build Logs** instead of App Logs
4. **Restart the app** manually if needed

## 📊 Expected Behavior

After successful setup:

1. ✅ Backend container runs (`1/1`)
2. ✅ App logs are visible
3. ✅ Static files accessible
4. ✅ Media files persist
5. ✅ Faster deployments (static files cached)
6. ✅ No data loss on redeployment

## 🎉 Success Indicators

You'll know it's working when:
- Container status: `1/1` (green)
- App logs show startup messages
- Static files load correctly
- Media files persist after deployment
- No volume mount errors in logs

---

**Status**: Configuration verified ✅
**Action**: Save & Update, then verify container starts


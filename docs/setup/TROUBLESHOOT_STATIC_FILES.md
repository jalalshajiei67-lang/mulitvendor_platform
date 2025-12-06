# Troubleshooting Static Files 404 - Step by Step Guide

## Current Issue
Status: `404 Not Found (from disk cache)`

⚠️ **This is a CACHED error!** Your browser is showing you the OLD 404 error from before WhiteNoise was deployed.

## Quick Fix - Try These Steps in Order

### Step 1: Clear Browser Cache Completely

#### Method A: Force Clear All Cache
```
1. Press: Ctrl + Shift + Delete
2. Time range: "All time" (not just "Last hour")
3. Check: ✅ Cached images and files
4. Check: ✅ Cookies and site data (optional but recommended)
5. Click: "Clear data"
6. Close ALL browser windows
7. Reopen browser
```

#### Method B: Use Incognito/Private Window
```
1. Press: Ctrl + Shift + N (Chrome) or Ctrl + Shift + P (Firefox)
2. Go to: https://multivendor-backend.indexo.ir/admin
3. This bypasses all cache
```

#### Method C: Hard Reload
```
1. Open: https://multivendor-backend.indexo.ir/admin
2. Press: Ctrl + F5 (Windows) or Cmd + Shift + R (Mac)
3. This forces fresh reload
```

### Step 2: Verify Deployment Completed

Check if the new code is actually deployed:

1. **GitHub Actions:**
   - Go to: https://github.com/jalalshajiei67-lang/mulitvendor_platform/actions
   - Last workflow should be: ✅ Green checkmark
   - Check timestamp: Should be recent (within last 15 mins)

2. **CapRover Dashboard:**
   - Go to: https://captain.indexo.ir/
   - Find your backend app
   - Check "Last Deployment": Should be recent
   - Status: Should be "Running" (green)

### Step 3: Check CapRover Logs for collectstatic

1. Go to CapRover → Your Backend App → Logs
2. Look for this line:
   ```
   X static files copied to '/app/static'
   ```
3. If you see "0 static files copied" → Problem with collectstatic
4. If you see a number > 0 → Static files were collected successfully

### Step 4: Test Static Files Directly

Try accessing static files directly in Incognito window:

```
https://multivendor-backend.indexo.ir/static/admin/css/base.css
https://multivendor-backend.indexo.ir/static/admin/js/jquery.init.js
```

**Expected Results:**
- ✅ Status 200 → WhiteNoise is working!
- ❌ Status 404 → Deployment issue (see solutions below)

## Common Issues & Solutions

### Issue 1: Browser Cache (Most Common)
**Symptom:** "404 Not Found (from disk cache)"
**Solution:**
```
1. Clear cache completely (all time, not just last hour)
2. Use Incognito mode
3. Try different browser
4. Restart browser completely
```

### Issue 2: Deployment Not Complete
**Symptom:** GitHub Actions still running or failed
**Solution:**
```
1. Wait for deployment to finish (~15 minutes)
2. Check GitHub Actions for errors
3. If failed, check error logs
4. May need to redeploy
```

### Issue 3: collectstatic Not Running
**Symptom:** CapRover logs show "0 static files copied"
**Solution:**
```
1. Check Dockerfile CMD includes collectstatic
2. Check requirements.txt has all packages
3. Manually trigger in CapRover:
   - App → App Configs → Deployment
   - Run command: python manage.py collectstatic --noinput
```

### Issue 4: nginx Interfering
**Symptom:** Static files work in browser but not through domain
**Solution:**
```
1. CapRover uses nginx as reverse proxy
2. WhiteNoise should handle static files
3. Check if custom nginx config exists
4. May need to disable nginx static file handling
```

## Diagnostic Commands

### Check WhiteNoise is Installed
Run in CapRover App Console:
```bash
pip list | grep whitenoise
# Should show: whitenoise 6.5.0
```

### Check Static Files Exist
Run in CapRover App Console:
```bash
ls -la /app/static/admin/css/
# Should list CSS files including custom_admin.css
```

### Force Collect Static Files
Run in CapRover App Console:
```bash
python manage.py collectstatic --noinput --clear
# This clears and recollects all static files
```

### Check Django Settings
Run in CapRover App Console:
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_ROOT)
>>> print(settings.STATIC_URL)
>>> print('whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE)
# Should print: True
```

## Step-by-Step Verification

### 1. Verify WhiteNoise Installation
```bash
# In CapRover console or SSH
pip show whitenoise
```
Expected output:
```
Name: whitenoise
Version: 6.5.0
Location: /usr/local/lib/python3.11/site-packages
```

### 2. Verify Middleware Configuration
Check settings.py has:
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Must be here!
    ...
]
```

### 3. Verify Storage Configuration
Check settings.py has:
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 4. Check Dockerfile
Dockerfile should have:
```dockerfile
CMD python manage.py migrate --noinput --fake-initial; \
    python manage.py collectstatic --noinput && \
    gunicorn ...
```

## Force Rebuild Solution

If nothing works, force a complete rebuild:

### Method 1: Empty Commit
```bash
git commit --allow-empty -m "Force rebuild"
git push
```

### Method 2: CapRover Manual Rebuild
```
1. Go to CapRover Dashboard
2. Select your backend app
3. Go to "Deployment" tab
4. Click "Force rebuild"
5. Wait for completion (~10 minutes)
```

### Method 3: Restart App
```
1. CapRover → Your App
2. Click "Stop" button
3. Wait 10 seconds
4. Click "Start" button
```

## Expected Behavior After Fix

### In Browser DevTools (F12 → Network):
```
Request: custom_admin.css
Status: 200 OK
Size: 2.5 KB (actual file size, not 0)
Time: < 100ms
Headers:
  ✅ Content-Encoding: gzip
  ✅ Content-Type: text/css
  ✅ Cache-Control: max-age=31536000
```

### In CapRover Logs:
```
✅ "X static files copied to '/app/static'"
✅ No 404 errors for static files
✅ Gunicorn worker started successfully
```

## Still Not Working?

### Get Detailed Logs

1. **CapRover Logs:**
   ```
   CapRover → App → Logs
   Look for errors during startup
   ```

2. **Django Debug:**
   Check if DEBUG=True in logs (should be False in production)

3. **Static Files List:**
   ```bash
   python manage.py collectstatic --noinput -v 2
   # Verbose mode shows which files are copied
   ```

### Check File Permissions
```bash
ls -la /app/static/
# Should show files owned by app user
# Permissions should be readable (r)
```

### Verify URL Configuration
In CapRover console:
```python
python manage.py shell
>>> from django.conf import settings
>>> print(f"STATIC_URL: {settings.STATIC_URL}")
>>> print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
```

Expected:
```
STATIC_URL: /static/
STATIC_ROOT: /app/static
```

## Emergency Fix: Manual Static File Upload

If all else fails, manually verify files exist:

1. CapRover → App → File Manager (if available)
2. Navigate to `/app/static/admin/css/`
3. Check if `custom_admin.css` exists
4. If missing, run collectstatic manually

## Contact Info

If issue persists after trying all steps:
1. Share CapRover logs (last 100 lines)
2. Share output of: `pip list | grep whitenoise`
3. Share output of: `python manage.py collectstatic --noinput -v 2`
4. Share browser DevTools Network tab screenshot

---

## Most Likely Solution

**90% chance:** Your browser cache is showing the old 404 error.

**Solution:**
1. Use Incognito window: Ctrl + Shift + N
2. Go to admin: https://multivendor-backend.indexo.ir/admin
3. Check if it works there

If it works in Incognito but not regular browser:
→ Clear cache completely (All time)
→ Close all browser windows
→ Reopen and try again


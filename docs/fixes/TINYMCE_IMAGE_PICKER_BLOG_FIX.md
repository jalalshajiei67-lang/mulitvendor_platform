# TinyMCE Image Picker - Blog Section Fix

## ✅ Status: Code is Correct - Deployment Issue

The TinyMCE image picker JavaScript file is correctly configured in the blog admin section. The 404 error in production indicates that the static file needs to be collected during deployment.

## 📋 Current Configuration

### File Location
- Source: `multivendor_platform/multivendor_platform/static/admin/js/tinymce_image_picker.js`
- Should be collected to: `staticfiles/admin/js/tinymce_image_picker.js`

### Blog Admin Configuration
The blog admin already includes the TinyMCE image picker JavaScript:

```python
# blog/admin.py
class Media:
    js = ('admin/js/fix_action_button.js', 'admin/js/tinymce_image_picker.js',)
```

This matches the products admin configuration exactly.

### Static Files Settings
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

## 🔧 Solution: Deploy or Run collectstatic

Since the code is already correct, you need to ensure the file is collected during deployment:

### Option 1: Redeploy (Recommended)
The `docker-entrypoint.sh` already runs `collectstatic --noinput --clear` during startup, so a fresh deployment should collect the file.

1. Commit and push any changes (if needed)
2. Trigger a new deployment in CapRover
3. Verify the file is collected in the deployment logs

### Option 2: Manual collectstatic (Quick Fix)
SSH into your CapRover server and run collectstatic manually:

```bash
# Connect to your backend container
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput --clear"

# Verify the file exists
caprover apps:exec multivendor-backend --command "ls -la /app/staticfiles/admin/js/tinymce_image_picker.js"
```

### Option 3: Force Rebuild
In CapRover dashboard:
1. Go to your backend app
2. Click "Deployment" tab
3. Click "Force Rebuild"
4. Wait for deployment to complete

## ✅ Verification

After deployment, verify the file is accessible:

1. **Check in browser DevTools:**
   - URL: `https://multivendor-backend.indexo.ir/static/admin/js/tinymce_image_picker.js`
   - Should return 200 OK (not 404)

2. **Check in CapRover logs:**
   ```
   [8/9] Collecting static files...
   ✅ Static files collected successfully!
   ```

3. **Test in blog admin:**
   - Go to: `https://multivendor-backend.indexo.ir/admin/blog/blogpost/add/`
   - Click the image button in TinyMCE editor
   - The file picker should open (not show error)

## 📝 Notes

- The file is already correctly configured in the code
- Both products and blog admin sections use the same configuration
- The backend image optimization (`tinymce_views.py`) is shared and works for both
- This is purely a static file collection/deployment issue, not a code issue


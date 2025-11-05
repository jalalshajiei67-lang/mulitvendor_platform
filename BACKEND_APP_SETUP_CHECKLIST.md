# Backend App Setup Checklist (After Recreating App)

Since you removed and recreated the backend app, verify these settings:

## ✅ Step 1: App Configuration

### Build Method
- [ ] Go to App Configs
- [ ] Build Method: **Dockerfile**
- [ ] Dockerfile Path: `./Dockerfile.backend`
- [ ] Repository: Your GitHub repo URL

### Port Configuration
- [ ] Go to **HTTP Settings**
- [ ] **Container HTTP Port:** `80` (must match EXPOSE in Dockerfile)
- [ ] **HTTPS:** Enabled
- [ ] **Domain:** `multivendor-backend.indexo.ir`

## ✅ Step 2: Environment Variables

Verify these are set in **App Configs → Environment Variables**:

```
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=your-actual-password
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
CSRF_TRUSTED_ORIGINS=https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir,https://multivendor-backend.indexo.ir
```

## ✅ Step 3: Persistent Directories

In **App Configs → Persistent Directories**:

- [ ] Add: `/app/staticfiles` → `/captain/data/backend-static` (Label: `static-files`)
- [ ] Add: `/app/media` → `/captain/data/backend-media` (Label: `media-files`)

## ✅ Step 4: Nginx Configuration

Your Nginx config looks correct. The default template is fine.

**IMPORTANT:** If you added custom Nginx config, make sure:
- [ ] No syntax errors
- [ ] Port matches (should use `$containerHttpPort` variable)
- [ ] No conflicting location blocks

## ✅ Step 5: Deploy

1. [ ] Push code to GitHub (if using CI/CD)
2. [ ] Or manually trigger deployment in CapRover
3. [ ] Wait for build to complete
4. [ ] Check app status turns **green "Running"**

## ✅ Step 6: Verify Logs

After deployment:

1. [ ] Go to **App Logs**
2. [ ] You should see:
   - "Starting Multivendor Backend Application"
   - "Creating media directories..."
   - "Running database migrations..."
   - "Collecting static files..."
   - "Starting Gunicorn server..."
   - Gunicorn startup messages

**If logs are still empty:**
- App might not be building correctly
- Check if Dockerfile path is correct
- Verify repository URL is correct
- Check build logs in CapRover

## ✅ Step 7: Test Endpoints

After app is running:

1. [ ] Test health: `https://multivendor-backend.indexo.ir/health/`
   - Should return: `OK`

2. [ ] Test API: `https://multivendor-backend.indexo.ir/api/departments/`
   - Should return JSON data

3. [ ] Test admin: `https://multivendor-backend.indexo.ir/admin/`
   - Should show login page

## 🔍 Troubleshooting Empty Logs

If logs are empty, the container might not be starting. Check:

1. **Build Logs:**
   - In CapRover, check build logs (not app logs)
   - Look for Docker build errors

2. **Container Status:**
   - App should show "Running" status
   - If "Stopped" or "Restarting", check build logs

3. **Verify Dockerfile:**
   - Ensure `Dockerfile.backend` exists in repo root
   - Check if `captain-definition-backend` points to correct Dockerfile

4. **Check Port:**
   - Container HTTP Port must be `80`
   - Must match `EXPOSE 80` in Dockerfile

## 🚨 Common Issues After Recreating App

### Issue 1: Wrong Dockerfile Path
**Symptom:** Build fails or app doesn't start

**Fix:** Verify Dockerfile path is `./Dockerfile.backend`

### Issue 2: Wrong Port
**Symptom:** 502 error even though app shows "Running"

**Fix:** Check Container HTTP Port is `80`

### Issue 3: Missing Environment Variables
**Symptom:** App crashes during startup

**Fix:** Add all required environment variables

### Issue 4: Database Connection Failed
**Symptom:** App starts but crashes, logs show DB error

**Fix:** Verify `DB_HOST=srv-captain--postgres-db` is correct

## 📝 Quick Verification Commands

After deployment, you can test from terminal:

```bash
# Test health endpoint
curl https://multivendor-backend.indexo.ir/health/

# Test API
curl https://multivendor-backend.indexo.ir/api/departments/

# Check if app is responding
curl -I https://multivendor-backend.indexo.ir/
```


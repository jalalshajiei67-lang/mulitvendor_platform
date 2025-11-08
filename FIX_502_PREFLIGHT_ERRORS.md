# Fix 502 Bad Gateway on Preflight OPTIONS Requests

## 🔍 Problem

You're getting **502 Bad Gateway** errors specifically on **preflight OPTIONS requests**:
- `OPTIONS /api/auth/me/` → 502 Bad Gateway
- `OPTIONS /api/departments/` → 502 Bad Gateway

But actual XHR requests work:
- `GET /api/auth/me/` → 200 OK
- `GET /api/departments/` → 200 OK

## 🔍 Root Cause

The 502 error means the backend server is **not responding** to OPTIONS requests. This could be:
1. **Backend crashed** on OPTIONS requests
2. **CORS middleware not working** correctly
3. **Changes not deployed** yet
4. **Backend needs restart** after configuration changes

## ✅ Fixes Applied

### 1. Enhanced CORS Configuration

Updated `settings_caprover.py` with:
- ✅ Better CORS headers (including preflight headers)
- ✅ Explicit OPTIONS method support
- ✅ CORS_URLS_REGEX to only apply to API endpoints
- ✅ Better error handling

### 2. Verified Middleware Order

CORS middleware is at the **top** of MIDDLEWARE list (required).

## 🚀 Deployment Steps

### Step 1: Commit and Push Changes

```bash
git add .
git commit -m "Fix 502 preflight errors - enhance CORS configuration"
git push origin main
```

### Step 2: Verify Deployment

1. **Check if changes are deployed:**
   - Go to CapRover Dashboard → Backend App → App Logs
   - Look for recent deployment logs
   - Verify the app restarted

2. **If not auto-deployed, manually trigger:**
   - Go to CapRover Dashboard → Backend App
   - Click **"Save & Restart"** or **"Save & Update"**

### Step 3: Check Backend Status

**Via CapRover Dashboard:**
- Check app status (should be green/running)
- Check App Logs for any errors
- Check Build Logs if deployment failed

**Via SSH (if needed):**
```bash
ssh root@185.208.172.76

# Check if container is running
docker ps | grep multivendor-backend

# Check logs
docker logs srv-captain--multivendor-backend.1.<container-id> --tail 100
```

### Step 4: Test OPTIONS Request

Test preflight request manually:

```bash
curl -X OPTIONS https://multivendor-backend.indexo.ir/api/departments/ \
  -H "Origin: https://indexo.ir" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: content-type" \
  -v
```

**Expected response:**
- Status: `200 OK` (not 502)
- Headers include:
  - `Access-Control-Allow-Origin: https://indexo.ir`
  - `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH`
  - `Access-Control-Allow-Headers: ...`
  - `Access-Control-Max-Age: 86400`

## 🔧 If 502 Errors Persist

### Option 1: Restart Backend App

1. Go to CapRover Dashboard → Backend App
2. Click **"Save & Restart"**
3. Wait 1-2 minutes for restart
4. Test again

### Option 2: Check Backend Logs for Errors

```bash
# Via CapRover Dashboard
Go to Backend App → App Logs

# Look for:
# - Python errors
# - Import errors
# - Middleware errors
# - CORS-related errors
```

### Option 3: Verify CORS Middleware is Installed

Check if `django-cors-headers` is in requirements:

```bash
# Should be in requirements.txt
django-cors-headers==4.4.0
```

### Option 4: Check Environment Variables

In CapRover Dashboard → Backend App → App Configs → Environment Variables:

```env
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
```

Or leave empty to use defaults from code.

### Option 5: Temporarily Enable CORS_ALLOW_ALL_ORIGINS

**For testing only** (not recommended for production):

In CapRover Dashboard → Backend App → Environment Variables:
```env
CORS_ALLOW_ALL_ORIGINS=True
```

This will allow all origins temporarily to test if CORS is the issue.

**⚠️ Remember to disable this after testing!**

## 📋 Current CORS Configuration

After fixes, your CORS settings:

```python
CORS_ALLOWED_ORIGINS = [
    'https://indexo.ir',
    'https://www.indexo.ir',
    'https://multivendor-backend.indexo.ir'
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-request-method',
    'access-control-request-headers',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_URLS_REGEX = r'^/api/.*$'  # Only apply to API endpoints
```

## ✅ Expected Behavior After Fix

1. **OPTIONS preflight requests** → Return `200 OK` (not 502)
2. **CORS headers** present in OPTIONS response
3. **Actual API requests** work normally
4. **No CORS errors** in browser console
5. **Frontend can make API calls** successfully

## 🆘 Still Not Working?

If 502 errors persist after deployment:

1. **Check backend is actually running:**
   - Status should be green in CapRover
   - Logs should show Gunicorn started

2. **Check for Python errors:**
   - Look for import errors
   - Look for syntax errors
   - Look for middleware errors

3. **Verify CORS middleware is loaded:**
   - Check logs for "CORS" related messages
   - Verify `corsheaders` is in INSTALLED_APPS

4. **Check if it's a proxy/nginx issue:**
   - 502 might be from nginx/proxy, not Django
   - Check CapRover nginx configuration

---

**Last Updated**: 2025-11-07
**Status**: Ready to deploy


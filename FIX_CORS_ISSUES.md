# Fix CORS Issues - Complete Guide

## 🔍 Issues Identified

1. **CORS Error**: "No 'Access-Control-Allow-Origin' header is present on the requested resource"
2. **502 Bad Gateway**: Backend might be crashing on OPTIONS requests
3. **403 Forbidden**: Likely a side effect of CORS failing

## ✅ Fixes Applied

### 1. Fixed CORS Configuration

Updated `settings_caprover.py` with proper CORS settings:

- ✅ Fixed `CORS_ALLOWED_ORIGINS` parsing (strips whitespace)
- ✅ Added `CORS_ALLOW_HEADERS` (includes all necessary headers)
- ✅ Added `CORS_ALLOW_METHODS` (includes OPTIONS for preflight)
- ✅ Added `CORS_EXPOSE_HEADERS`
- ✅ Added `CORS_PREFLIGHT_MAX_AGE` for caching

### 2. CORS Origins Configuration

Make sure your CapRover environment variables are set correctly:

**In CapRover Dashboard → Backend App → App Configs → Environment Variables:**

```env
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
```

Or leave it as default (already configured in code).

## 🚀 Deployment Steps

### Step 1: Commit and Push Changes

```bash
git add multivendor_platform/multivendor_platform/multivendor_platform/settings_caprover.py
git commit -m "Fix CORS configuration - add proper headers and methods"
git push origin main
```

### Step 2: Verify CapRover Environment Variables

1. Go to CapRover Dashboard → `multivendor-backend` → App Configs
2. Check Environment Variables section
3. Verify or add:
   ```
   CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
   ```
4. Click **Save & Update**

### Step 3: Wait for Deployment

- CapRover will automatically redeploy (if CI/CD is set up)
- Or manually trigger deployment
- Wait 1-2 minutes for deployment to complete

### Step 4: Test CORS

1. Open browser console on `https://indexo.ir`
2. Try making an API request
3. Check Network tab for:
   - ✅ OPTIONS request returns 200 (preflight)
   - ✅ GET/POST request returns 200 (actual request)
   - ✅ Response headers include `Access-Control-Allow-Origin`

## 🔍 Troubleshooting

### If CORS errors persist:

#### 1. Check Backend Logs

```bash
# Via CapRover Dashboard
Go to Backend App → App Logs

# Or via SSH
ssh root@185.208.172.76
docker logs srv-captain--multivendor-backend.1.<container-id> --tail 100
```

Look for:
- CORS middleware errors
- OPTIONS request handling
- Any 500 errors

#### 2. Verify CORS Middleware Order

The CORS middleware **must** be at the top of MIDDLEWARE list:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← Must be first
    'django.middleware.security.SecurityMiddleware',
    # ... rest of middleware
]
```

#### 3. Test OPTIONS Request Manually

```bash
curl -X OPTIONS https://multivendor-backend.indexo.ir/api/departments/ \
  -H "Origin: https://indexo.ir" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: content-type" \
  -v
```

Expected response headers:
```
Access-Control-Allow-Origin: https://indexo.ir
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
Access-Control-Allow-Headers: accept, content-type, authorization, ...
Access-Control-Allow-Credentials: true
```

#### 4. Check 502 Bad Gateway

If you're still getting 502 errors:

1. **Check if backend is running:**
   ```bash
   # In CapRover Dashboard
   Check app status (should be green/running)
   ```

2. **Check backend logs for crashes:**
   ```bash
   docker logs srv-captain--multivendor-backend.1.<container-id> --tail 200
   ```

3. **Restart backend app:**
   - In CapRover Dashboard → Backend App
   - Click "Save & Restart"

#### 5. Verify Environment Variables

Make sure environment variables are set correctly in CapRover:

```env
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
```

**Note**: Don't use `CORS_ALLOW_ALL_ORIGINS=True` in production (security risk).

## 📋 Current CORS Configuration

After the fix, your CORS settings are:

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
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

## ✅ Expected Behavior After Fix

1. **Preflight OPTIONS requests** → Return 200 with CORS headers
2. **Actual API requests** → Return 200/201/404 with CORS headers
3. **No CORS errors** in browser console
4. **Frontend can make API calls** successfully

## 🔒 Security Note

The current configuration:
- ✅ Only allows specific origins (not all origins)
- ✅ Allows credentials (cookies, auth headers)
- ✅ Restricts allowed methods and headers

This is secure for production use.

---

**Last Updated**: 2025-11-07
**Status**: Ready to deploy


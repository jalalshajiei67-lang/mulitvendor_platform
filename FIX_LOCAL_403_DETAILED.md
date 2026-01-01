# 🔧 Fix: Local Development 403 Forbidden Errors

## 🐛 Issue
Your Nuxt frontend (port 3000) is getting 403 Forbidden when calling Django backend (port 8000):

```
GET http://localhost:8000/api/categories/ 403 (Forbidden)
GET http://localhost:8000/api/label-groups/ 403 (Forbidden)
```

## 🎯 Root Cause

The Django backend is rejecting requests from your frontend due to **CSRF/CORS protection**. The backend doesn't recognize `localhost:3000` as an allowed origin.

---

## ✅ Solution (Choose One)

### **Option 1: Quick Script (Easiest)**

```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform"
./fix-local-403.sh
```

Then restart your Django server.

---

### **Option 2: Manual Configuration**

#### Step 1: Set Environment Variables

**For Linux/Mac:**
```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform"

export DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1
export CORS_ALLOW_ALL_ORIGINS=True
export CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

python manage.py runserver
```

**For Windows (PowerShell):**
```powershell
cd "C:\path\to\multivendor_platform\multivendor_platform\multivendor_platform"

$env:DEBUG="True"
$env:ALLOWED_HOSTS="localhost,127.0.0.1"
$env:CORS_ALLOW_ALL_ORIGINS="True"
$env:CSRF_TRUSTED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"

python manage.py runserver
```

---

### **Option 3: Create `.env` File in Django Directory**

```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform"

# Create .env file
cat > .env << 'EOF'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
SECRET_KEY=dev-secret-key-for-local-only
EOF

# Restart Django
python manage.py runserver
```

---

## 🔍 Verify the Fix

After restarting Django, check the console output. You should see:

```bash
System check identified no issues (0 silenced).
January 01, 2026 - 16:30:00
Django version 4.2.x, using settings 'multivendor_platform.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Then test in your browser console:**
- Refresh your Nuxt app
- Open Developer Tools → Console
- Should see **NO 403 errors**
- API calls should return 200 OK

---

## 📊 What Changed

| Setting | Before | After | Why |
|---------|--------|-------|-----|
| `CORS_ALLOW_ALL_ORIGINS` | False | **True** | Allow all origins in development |
| `CSRF_TRUSTED_ORIGINS` | Not set | **localhost:3000** | Trust frontend origin |
| `ALLOWED_HOSTS` | Limited | **localhost,127.0.0.1** | Accept local requests |
| `DEBUG` | False | **True** | Enable debugging |

---

## ⚠️ Important Notes

### **For Development Only**
These settings are **INSECURE for production**. Never use `CORS_ALLOW_ALL_ORIGINS=True` in production!

### **For Production (VPS)**
Keep these settings in your production `.env`:
```env
DEBUG=False
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
CSRF_TRUSTED_ORIGINS=https://multivendor-backend.indexo.ir,https://indexo.ir
ALLOWED_HOSTS=indexo.ir,www.indexo.ir,multivendor-backend.indexo.ir
```

---

## 🎯 Additional Issues in Your Console

### 1. **Sentry/Analytics Error** (Non-Critical)
```
POST http://127.0.0.1:7242/ingest/... net::ERR_CONNECTION_REFUSED
```
**This is NORMAL** - You don't have Sentry running locally. It won't affect functionality.

**To disable these errors:**
- Remove or comment out Sentry initialization in your Nuxt config
- Or ignore them (they're just warnings)

### 2. **E-namad SSL Error** (Non-Critical)
```
GET https://trustseal.enamad.ir/logo.aspx?... net::ERR_SSL_VERSION_OR_CIPHER_MISMATCH
```
**This is an external service issue** - Not your fault. The E-namad server has SSL configuration problems.

---

## 🚀 Quick Test

After applying the fix:

```bash
# Test from command line
curl -I http://localhost:8000/api/categories/

# Should return:
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Content-Type: application/json
```

---

## 📝 Troubleshooting

### Still getting 403?

1. **Check Django is using the environment variables:**
   ```bash
   python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.CORS_ALLOW_ALL_ORIGINS)
   True  # Should be True
   >>> print(settings.DEBUG)
   True  # Should be True
   ```

2. **Check for syntax errors in .env file:**
   - No spaces around `=`
   - No quotes around values (unless needed)
   - One setting per line

3. **Restart Django completely:**
   - Stop: Ctrl+C
   - Wait 2 seconds
   - Start: `python manage.py runserver`

4. **Clear browser cache:**
   - Open DevTools
   - Right-click refresh button
   - Select "Empty Cache and Hard Reload"

---

## ✅ Success Checklist

- [ ] Environment variables set
- [ ] Django server restarted
- [ ] No 403 errors in console
- [ ] API calls returning 200 OK
- [ ] Nuxt app loading data successfully

---

## 🎉 Summary

**Problem:** Backend rejecting frontend requests (403 Forbidden)  
**Cause:** CORS/CSRF protection blocking localhost:3000  
**Solution:** Enable CORS for all origins in development  
**Time to fix:** < 2 minutes  

Run `./fix-local-403.sh` and restart Django! 🚀

---

**Last Updated:** January 1, 2026  
**Status:** Ready to Apply  
**Environment:** Local Development Only  


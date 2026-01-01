# 🔧 Quick Fix: 403 Forbidden Errors on API Requests

## 🐛 Issue
Your API is returning **403 Forbidden** for GET requests:
```
[WARNING] HTTP GET /api/categories/ 403
[WARNING] HTTP GET /api/label-groups/ 403
[WARNING] HTTP GET /api/products/slug/9/ 403
```

While OPTIONS requests work fine:
```
[INFO] HTTP OPTIONS /api/products/slug/9/ 200
```

## 🔍 Root Cause

This is happening because:
1. CORS preflight (OPTIONS) is working ✅
2. But actual requests are being blocked by CSRF/authentication ❌

## ✅ Quick Solutions

### **Solution 1: Check ALLOWED_HOSTS (Most Common)**

Add your frontend origin to `ALLOWED_HOSTS` in `.env`:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,your-frontend-domain.com
```

Then restart:
```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform"
python manage.py runserver
```

### **Solution 2: Add CSRF Trusted Origins**

If running frontend on different port (e.g., 3000), add to `.env`:

```env
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### **Solution 3: Verify CORS Settings**

Check your `.env` has:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_ALL_ORIGINS=True  # For development only
```

## 🚀 Quick Test

After making changes, test with curl:

```bash
# Test from command line
curl -X GET http://127.0.0.1:8000/api/categories/ -H "Origin: http://localhost:3000"
```

Should return 200, not 403.

## 📝 For Production

Remember to set in production `.env`:
```env
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-production-domain.com
```

---

**Which solution do you need help with?** Let me know your frontend setup (port, domain) and I'll provide the exact configuration.


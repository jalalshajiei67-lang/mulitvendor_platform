# 🔍 Asset 404 Fix Guide

## Problem
HTML loads but shows blank page because:
- `/assets/index-wCylENLd.js` → 404 Not Found
- `/assets/index-CmgsvBAv.css` → 404 Not Found

## Check Inside Container

**In CapRover → Frontend App → Deployment → View Logs → Web Terminal:**

```bash
# Check what's actually there:
ls -la /usr/share/nginx/html/
ls -la /usr/share/nginx/html/assets/

# Check nginx config:
cat /etc/nginx/conf.d/default.conf
```

## Possible Causes & Fixes

### Cause 1: Assets folder is empty/missing
**Solution:** Rebuild with verbose logging to see if dist/ has files

### Cause 2: Nginx config is wrong
**Check:** nginx/frontend.conf should have correct root path

### Cause 3: Permissions issue
**Solution:** Check file permissions in container

### Cause 4: Base URL mismatch
**Check:** If using a subdirectory, Vite needs base config

## Quick Test
In browser console (F12), try accessing assets directly:
- https://indexo.ir/assets/index-wCylENLd.js
- Does it 404 or show JavaScript?

## Immediate Actions

1. **Fix environment variable in CapRover:**
   - Change: `VITE_API_BASE_URL=https://multivendor-backend.indexo.ir/api`
   - (Add /api suffix)
   - Save & Update

2. **Force Rebuild:**
   - After fixing env var
   - Click "Force Rebuild"
   - Wait 5 minutes

3. **Check container:**
   - Use Web Terminal
   - Run: `ls -la /usr/share/nginx/html/assets/`
   - Confirm files exist

4. **Hard refresh browser:**
   - Ctrl + F5 (Windows)
   - Cmd + Shift + R (Mac)


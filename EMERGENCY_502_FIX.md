# 🚨 EMERGENCY: 502 Bad Gateway Fix

## Problem
Your backend is returning 502 errors - the application isn't starting.

## Quick Fix Options

### Option 1: Deploy with Fixed Dockerfile (RECOMMENDED)

The main `Dockerfile.backend` has been updated to not fail if collectstatic has issues.

```bash
# Deploy immediately
git add Dockerfile.backend
git commit -m "Fix: Make startup resilient to collectstatic failures"
git push origin main
```

**What this does:**
- Even if collectstatic fails, Gunicorn will start
- Your APIs will work immediately
- Static files might not work yet, but we can fix that separately

---

### Option 2: Emergency Dockerfile (If Option 1 Fails)

If the first option doesn't work, use the emergency Dockerfile:

1. **Rename the emergency file:**
```bash
# Backup current Dockerfile
mv Dockerfile.backend Dockerfile.backend.backup

# Use emergency version
mv Dockerfile.backend.emergency Dockerfile.backend
```

2. **Deploy:**
```bash
git add Dockerfile.backend
git commit -m "Emergency: Use minimal Dockerfile to restore service"
git push origin main
```

3. **This will:**
   - Skip static file collection completely
   - Get your APIs working IMMEDIATELY
   - Admin might not have styling, but APIs work

---

### Option 3: Check CapRover Environment Variable

The issue might be that you didn't update the environment variable yet.

1. **Go to CapRover Dashboard**
   - Navigate to your backend app
   - Click "App Configs" tab
   - Find environment variables section

2. **Check/Update this variable:**
   ```
   STATIC_ROOT=/app/staticfiles
   ```
   
3. **If it says `/app/static`, change it to `/app/staticfiles`**

4. **Click "Save & Update"**

---

### Option 4: View Logs to Diagnose

Check what's actually failing:

**In CapRover Web Interface:**
1. Go to your backend app
2. Click "App Logs" tab
3. Look for errors (usually at the bottom)

**Via SSH:**
```bash
# SSH into your server
ssh root@your-server-ip

# View recent logs
docker logs srv-captain--multivendor-backend --tail 100

# Follow logs in real-time
docker logs srv-captain--multivendor-backend -f
```

**Look for these errors:**
- `ImproperlyConfigured: STATIC_ROOT`
- `CommandError: collectstatic`
- `ModuleNotFoundError`
- `DatabaseError`

---

## Quick Rollback (Nuclear Option)

If you need to restore service immediately, revert all changes:

```bash
# See recent commits
git log --oneline -5

# Revert to before the changes
git revert HEAD

# Or reset to a specific commit
git reset --hard <commit-hash-before-changes>

# Force push (CAREFUL!)
git push origin main --force
```

⚠️ **Warning:** This removes the static files fix, so you'll be back to the original problem.

---

## What's Different in the Fixed Dockerfile

**OLD (Breaks on error):**
```dockerfile
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput --clear && \
    gunicorn ...
```

**NEW (Continues even with errors):**
```dockerfile
CMD python manage.py migrate --noinput && \
    (python manage.py collectstatic --noinput --clear && echo "✓ Static files collected" || echo "⚠ collectstatic failed, but continuing...") && \
    gunicorn ...
```

The `(command || fallback)` syntax means:
- If collectstatic succeeds → print success message
- If collectstatic fails → print warning but **continue anyway**
- Gunicorn starts regardless

---

## After Getting App Running

Once your APIs are working again:

1. **Check if static files work:**
   - Visit: `https://multivendor-backend.indexo.ir/static/admin/css/base.css`
   - If 200 OK → static files are working!
   - If 404 → we need to debug collectstatic

2. **If static files still don't work, we'll debug separately**

3. **Your APIs and business logic will work fine** regardless of static file issues

---

## Prevention for Future

To avoid this in future deployments:

1. **Always test locally first:**
   ```bash
   # Build Docker image locally
   docker build -f Dockerfile.backend -t test-backend .
   
   # Run it
   docker run -p 8000:80 test-backend
   
   # Test if it starts
   curl http://localhost:8000/api/products/
   ```

2. **Use staging environment** before production

3. **Monitor CapRover logs** during deployment

4. **Keep emergency Dockerfile** handy

---

## Contact Points

If none of this works:

1. Share the CapRover logs (last 50 lines)
2. Share any error messages from the deployment
3. Confirm which environment variables are set in CapRover

---

Remember: **Getting your APIs working is priority #1**. We can fix static files after your service is restored! 🚀


# Quick Fix for 502 Bad Gateway

## Immediate Actions (Do These First)

### Step 1: Check CapRover Dashboard

1. Go to **https://captain.indexo.ir**
2. Navigate to **Apps** → **multivendor-backend**
3. Check the app status:
   - ✅ **Green "Running"** = App is up, but there's a configuration issue
   - ❌ **Red "Stopped"** or **"Restarting"** = App is crashing

### Step 2: Check App Logs

1. In your backend app, click **"App Logs"**
2. Look at the **most recent logs** (scroll to bottom)
3. Common errors to look for:

**Database Connection Error:**
```
django.db.utils.OperationalError: could not connect to server
```
**Solution:** Check database credentials in App Config → Environment Variables

**Migration Error:**
```
django.db.utils.ProgrammingError: relation already exists
```
**Solution:** This is usually OK, but check if migrations are running

**Import Error:**
```
ModuleNotFoundError: No module named 'xxx'
```
**Solution:** Check requirements.txt, redeploy

**Port Error:**
```
Address already in use
```
**Solution:** Check port mapping in CapRover

### Step 3: Quick Fixes

#### Fix 1: Restart the App
1. In CapRover Dashboard → Backend App
2. Click **"Save & Restart"**
3. Wait 30-60 seconds
4. Test the endpoint again

#### Fix 2: Check Environment Variables
Verify these are set correctly:
- `DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover`
- `DB_HOST=srv-captain--postgres-db`
- `DB_NAME=multivendor_db`
- `DB_USER=postgres`
- `DB_PASSWORD=your-actual-password`

#### Fix 3: Verify Database is Running
1. CapRover → **One-Click Apps/Databases**
2. Check if PostgreSQL is running
3. If not, restart it

#### Fix 4: Check HTTP Settings
1. Backend App → **HTTP Settings**
2. Ensure:
   - HTTPS is enabled
   - Domain is set: `multivendor-backend.indexo.ir`
   - No custom port conflicts

### Step 4: Test Health Endpoint

After deploying the updated code, test:
```bash
curl https://multivendor-backend.indexo.ir/health/
```

Should return: `OK`

## Common Scenarios

### Scenario 1: App Shows "Running" but 502 Error

**Cause:** App is running but Gunicorn isn't listening on port 80

**Fix:**
1. Check logs for Gunicorn startup messages
2. Verify `EXPOSE 80` in Dockerfile
3. Check if gunicorn is binding to `0.0.0.0:80`

### Scenario 2: App Keeps Restarting

**Cause:** App crashes during startup

**Fix:**
1. Check logs for the error causing the crash
2. Common causes:
   - Database connection failed
   - Migration failed
   - Missing environment variable
   - Import error

### Scenario 3: Database Connection Failed

**Symptoms:** Logs show database connection errors

**Fix:**
1. Verify database service name: `srv-captain--postgres-db`
2. Check database credentials
3. Ensure database is running
4. Test connection manually:
   ```bash
   # In CapRover, use one-click terminal or SSH to VPS
   docker exec -it srv-captain--postgres-db psql -U postgres -d multivendor_db
   ```

### Scenario 4: Migration Failed

**Symptoms:** Logs show migration errors

**Fix:**
1. Check if database exists
2. Try running migrations manually
3. If database is fresh, ensure initial migrations can run

## Emergency: Use Simplified Dockerfile

If the main Dockerfile keeps failing, temporarily switch to the emergency version:

1. In CapRover → Backend App → App Configs
2. Change Dockerfile path to: `./Dockerfile.backend.emergency`
3. Save & Restart

This version skips collectstatic and has minimal startup steps.

## After Fixing

1. ✅ Test: `https://multivendor-backend.indexo.ir/health/` → Should return "OK"
2. ✅ Test: `https://multivendor-backend.indexo.ir/api/departments/` → Should return JSON
3. ✅ Check logs for successful startup message
4. ✅ Verify no errors in logs

## Still Not Working?

1. Check **TROUBLESHOOT_502.md** for detailed diagnosis
2. Check CapRover logs for specific error messages
3. Verify all environment variables are correct
4. Ensure database is accessible
5. Check if there are any recent code changes that broke startup



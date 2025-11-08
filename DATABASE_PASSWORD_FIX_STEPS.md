# Quick Fix: Database Password Authentication Error

## The Problem
```
FATAL: password authentication failed for user "postgres"
```

Your app is running, but can't connect to the database because the password is wrong.

## Quick Fix Steps

### Step 1: Find Your PostgreSQL Password

**Method 1: Check CapRover PostgreSQL App**
1. Go to CapRover Dashboard → **One-Click Apps/Databases**
2. Click on your PostgreSQL app (usually named `postgres-db`)
3. Go to **App Configs** → **Environment Variables**
4. Look for `POSTGRES_PASSWORD` or `POSTGRES_ROOT_PASSWORD`
5. Copy that password value

**Method 2: If You Don't See the Password**
- The password might be hidden for security
- You may need to reset it (see below)

### Step 2: Update Backend App Password

1. Go to CapRover Dashboard → **Apps** → **multivendor-backend**
2. Click **App Configs** → **Environment Variables**
3. Find `DB_PASSWORD` in the list
4. Click to edit it
5. Paste the PostgreSQL password you found in Step 1
6. Click **Save** (or outside the field to save)
7. Click **"Save & Restart"** button at the bottom

### Step 3: Wait for Restart

- Wait 30-60 seconds for the app to restart
- Check **App Logs** again
- You should now see: `✅ Migrations completed` instead of the error

## If You Don't Know the Password

### Option A: Reset PostgreSQL Password

1. Go to PostgreSQL app → **App Configs** → **Environment Variables**
2. Add or update: `POSTGRES_PASSWORD=your-new-secure-password`
3. **Save & Restart** PostgreSQL app
4. Update backend app's `DB_PASSWORD` to match
5. Restart backend app

### Option B: Create New Database User

If you can't reset the password, you might need to create a new database user with proper permissions.

## Verify All Database Settings

After fixing, make sure these are set correctly in backend app:

```
DB_HOST=srv-captain--postgres-db
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=<the-correct-password>
DB_PORT=5432
```

## Test After Fix

1. **Check Logs:**
   - Should see: `✅ Migrations completed`
   - No more password errors

2. **Test API:**
   ```bash
   curl https://multivendor-backend.indexo.ir/api/departments/
   ```
   - Should return JSON data, not 500 error

3. **Test Health:**
   ```bash
   curl https://multivendor-backend.indexo.ir/health/
   ```
   - Should return: `OK`

## Common Mistakes

❌ **Wrong password** - Make sure it matches exactly (case-sensitive)
❌ **Extra spaces** - No spaces before/after password
❌ **Special characters** - If password has special chars, they might need escaping
❌ **Wrong database name** - Verify `DB_NAME` matches actual database

## Still Not Working?

1. Double-check PostgreSQL app is running
2. Verify database exists: `DB_NAME` should match an existing database
3. Check network connectivity between apps (usually automatic in CapRover)
4. Try resetting the password completely (Option A above)






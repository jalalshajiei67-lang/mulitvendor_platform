# Fix Database Password Authentication Error

## Current Error
```
FATAL: password authentication failed for user "postgres"
```

## Solution: Update DB_PASSWORD Environment Variable

### Step 1: Find PostgreSQL Password

**Option A: Check CapRover PostgreSQL App**
1. CapRover Dashboard → **One-Click Apps/Databases**
2. Find your PostgreSQL app (usually `postgres-db`)
3. Click on it
4. Check **Environment Variables** or **App Configs** for the password
5. Look for `POSTGRES_PASSWORD` or `POSTGRES_ROOT_PASSWORD`

**Option B: Check When You Created the Database**
- If you set a password when creating PostgreSQL, use that
- If you didn't set one, CapRover might have generated one

**Option C: Reset PostgreSQL Password (if needed)**
1. In PostgreSQL app → **App Configs**
2. Add/Update environment variable: `POSTGRES_PASSWORD=your-new-password`
3. Save & Restart PostgreSQL app
4. Use this new password in your backend app

### Step 2: Update Backend App Environment Variable

1. CapRover Dashboard → **Apps** → **multivendor-backend**
2. Go to **App Configs** → **Environment Variables**
3. Find `DB_PASSWORD`
4. **Update it** to match the PostgreSQL password
5. Click **"Save & Restart"**

### Step 3: Verify All Database Variables

Make sure these are set correctly:

```
DB_HOST=srv-captain--postgres-db
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=<your-actual-postgres-password>
DB_PORT=5432
```

### Step 4: Test Connection

After restart, check logs again. You should see:
```
[2/5] Running database migrations...
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying ... OK
✅ Migrations completed
```

Instead of the password authentication error.

## Quick Test

After fixing, test the API:
```bash
curl https://multivendor-backend.indexo.ir/api/departments/
```

Should return JSON data instead of 500 error.

## Common Issues

### Issue 1: Password Has Special Characters
- If password contains special characters, make sure they're properly escaped
- Try wrapping in quotes if needed

### Issue 2: Database Doesn't Exist
- If `DB_NAME` doesn't exist, create it:
  ```sql
  CREATE DATABASE multivendor_db;
  ```

### Issue 3: User Doesn't Have Permission
- Ensure `postgres` user has access to the database
- Or use a different user that has proper permissions






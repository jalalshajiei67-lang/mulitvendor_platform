# Quick Fix: Database Connection Error

## Problem
```
FATAL: password authentication failed for user "postgres"
```

## Immediate Fix Steps

### Step 1: Verify PostgreSQL App Environment Variables

Go to CapRover Dashboard → `multivendor_db` app → Environment Variables

**Set these EXACT values:**
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=thisIsAsimplePassword09
POSTGRES_DB=multivendor-db
POSTGRES_INITDB_ARGS=
```

**Important**: Change `POSTGRES_DB` from `postgres` to `multivendor-db`

### Step 2: Verify Backend App Environment Variables

Go to CapRover Dashboard → `multivendor-backend` app → Environment Variables

**Verify these match:**
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor-db
DB_USER=postgres
DB_PASSWORD=thisIsAsimplePassword09
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
```

### Step 3: If Database Already Exists with Wrong Name

If you've already created the database with name `postgres`:

**Option A**: Create the new database manually
```bash
# SSH to your server
ssh root@185.208.172.76

# Connect to PostgreSQL
docker exec -it srv-captain--postgres-db psql -U postgres

# Create the database
CREATE DATABASE "multivendor-db";

# Grant permissions
GRANT ALL PRIVILEGES ON DATABASE "multivendor-db" TO postgres;

# Exit
\q
```

**Option B**: Update backend to use existing database
- Change `DB_NAME=postgres` in backend app (only if you want to use existing database)

### Step 4: Restart Apps

1. Restart `multivendor_db` app in CapRover
2. Restart `multivendor-backend` app in CapRover

### Step 5: Verify Fix

Check backend logs:
```bash
caprover logs multivendor-backend --lines 20
```

Should see successful migration or no database errors.

## Common Issues

### Issue 1: Database doesn't exist
**Error**: `database "multivendor-db" does not exist`
**Fix**: Create database (Step 3 above)

### Issue 2: Password mismatch
**Error**: `password authentication failed`
**Fix**: 
- Double-check both apps have EXACT same password
- No extra spaces or typos
- If still failing, reset PostgreSQL password:
  1. Delete `multivendor_db` app
  2. Recreate with correct `POSTGRES_PASSWORD`
  3. Restart backend

### Issue 3: User doesn't exist
**Error**: `role "postgres" does not exist`
**Fix**: Ensure `POSTGRES_USER=postgres` in PostgreSQL app

## After Fix

Run migrations:
```bash
# This should run automatically on container start
# If not, execute manually:
docker exec -it srv-captain--multivendor-backend python manage.py migrate
```










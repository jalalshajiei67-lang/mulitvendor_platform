# Fix Database Connection Issue

## Problem
The backend is failing to connect to PostgreSQL with error: `password authentication failed for user "postgres"`

## Root Cause Analysis

### Current Configuration:

**multivendor-backend app:**
- DB_PASSWORD=thisIsAsimplePassword09
- DB_NAME=multivendor-db
- DB_USER=postgres

**multivendor_db app:**
- POSTGRES_PASSWORD=thisIsAsimplePassword09
- POSTGRES_DB=postgres

### Issues Identified:

1. **Database Name Mismatch**: Backend tries to connect to `multivendor-db`, but PostgreSQL is initialized with default database `postgres`
2. **Password Authentication**: The error suggests password mismatch or user doesn't exist

## Solution Steps

### Option 1: Fix Database Name (Recommended)

Update the PostgreSQL app environment variables to create the correct database:

1. Go to CapRover Dashboard → `multivendor_db` app
2. Add/Update environment variable:
   ```
   POSTGRES_DB=multivendor-db
   ```
3. **Important**: If this is an existing database, you may need to:
   - Create the database manually inside PostgreSQL, OR
   - Delete and recreate the database container (⚠️ **WARNING**: This will delete all data!)

### Option 2: Update Backend to Use Existing Database

Update the backend app environment variables:

1. Go to CapRover Dashboard → `multivendor-backend` app
2. Update environment variable:
   ```
   DB_NAME=postgres
   ```

### Option 3: Reset PostgreSQL Password (If password is actually wrong)

If the passwords don't match, you need to reset PostgreSQL:

1. **Backup your data first!** (if you have any)
2. Delete the `multivendor_db` app in CapRover
3. Create a new PostgreSQL app with these exact variables:
   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=thisIsAsimplePassword09
   POSTGRES_DB=multivendor-db
   POSTGRES_INITDB_ARGS=
   ```
4. Make sure backend app has matching credentials:
   ```
   DB_NAME=multivendor-db
   DB_USER=postgres
   DB_PASSWORD=thisIsAsimplePassword09
   ```

## Quick Fix (Recommended)

**Step 1**: Update PostgreSQL app environment variables:
```
POSTGRES_DB=multivendor-db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=thisIsAsimplePassword09
POSTGRES_INITDB_ARGS=
```

**Step 2**: If database already exists with data:
- SSH into your server
- Connect to PostgreSQL container
- Create the database manually:
  ```bash
  # Connect to PostgreSQL
  docker exec -it srv-captain--postgres-db psql -U postgres
  
  # Create database
  CREATE DATABASE "multivendor-db";
  
  # Exit
  \q
  ```

**Step 3**: Verify backend environment variables match:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor-db
DB_USER=postgres
DB_PASSWORD=thisIsAsimplePassword09
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
```

**Step 4**: Restart both apps in CapRover

## Verification

After making changes, check logs:
```bash
# Check backend logs
caprover logs multivendor-backend --lines 50

# Check if migration runs successfully
```

Expected success: No more "password authentication failed" errors.










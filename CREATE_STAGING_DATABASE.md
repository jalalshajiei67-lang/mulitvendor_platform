# Create Staging Database - Quick Fix

## Problem
```
database "multivendor-db-staging" does not exist
```

The backend is trying to connect to a database that doesn't exist yet.

## ✅ Solution: Create the Database

### Option 1: Via CapRover (Easiest)

1. Go to CapRover Dashboard: `https://captain.indexo.ir`
2. Navigate to **Apps** → **postgres-db-staging**
3. Click **App Configs** → **Environment Variables**
4. Make sure it has:
   ```
   POSTGRES_DB=multivendor-db-staging
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=thisIsAsimplePassword09-staging
   ```
5. If `POSTGRES_DB` is missing or different, **add/set it** to `multivendor-db-staging`
6. Click **Save & Update**
7. **Important:** If the database was already initialized, you may need to delete the persistent volume and recreate the app (see Option 2)

### Option 2: Create Database Manually (If PostgreSQL Already Exists)

If PostgreSQL staging app already exists but the database doesn't:

1. **SSH into your server:**
   ```bash
   ssh root@185.208.172.76
   ```

2. **Connect to PostgreSQL:**
   ```bash
   docker exec -it srv-captain--postgres-db-staging psql -U postgres
   ```

3. **Create the database:**
   ```sql
   CREATE DATABASE "multivendor-db-staging";
   \q
   ```

4. **Verify it was created:**
   ```bash
   docker exec -it srv-captain--postgres-db-staging psql -U postgres -l
   ```
   You should see `multivendor-db-staging` in the list.

### Option 3: Force Recreate PostgreSQL App (Nuclear Option)

If you don't have important data in staging database:

1. **Delete the PostgreSQL staging app in CapRover**
2. **Recreate it:**
   - App Name: `postgres-db-staging`
   - Has Persistent Data: **Yes**
   - Environment Variables:
     ```
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=thisIsAsimplePassword09-staging
     POSTGRES_DB=multivendor-db-staging
     ```
3. Wait for it to fully start
4. Restart backend staging app

## ✅ After Creating Database

1. **Restart backend staging app:**
   - CapRover → Apps → `multivendor-backend-staging`
   - Click **Save & Update** (or restart button)
   - Wait 30-60 seconds

2. **Check logs** - should see:
   - ✅ `Database connection successful!`
   - ✅ `Migrations completed successfully!`

3. **Frontend should then work** once backend is running!






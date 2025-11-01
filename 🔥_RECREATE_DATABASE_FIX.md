# 🔥 Force Recreate PostgreSQL Database

## Why This Is Needed

PostgreSQL initializes its database on **first startup only**. Changing `POSTGRES_DB` environment variable after the container already exists doesn't recreate the database.

## ✅ Solution: Force Database Recreation

### Step 1: Remove the Persistent Data Volume

In CapRover for `multivendor_db` app:

1. **Go to App Configs tab**
2. **Scroll to "Persistent Directories"**
3. **Delete any persistent directories** (this will erase all data but force a fresh start)
4. **Or note the path** (likely `/var/lib/postgresql/data`)

### Step 2: Method A - Delete and Recreate App (Cleanest)

**In CapRover:**

1. Go to `Apps` → `multivendor_db`
2. Click **"Delete App"** (yes, delete the entire app)
3. Wait for deletion to complete
4. Click **"One-Click Apps/Databases"**
5. Search for **"PostgreSQL"**
6. Create new PostgreSQL app with these settings:
   - App Name: `multivendor-db` or `postgres-db` (your choice, but remember for DB_HOST)
   - **IMPORTANT:** Use environment variables:
     ```
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=thisIsAsimplePassword09
     POSTGRES_DB=multivendor-db
     ```

7. Wait for it to fully start

8. **Update your backend app** `DB_HOST` if you changed the app name:
   - If you named it `multivendor-db`: `DB_HOST=srv-captain--multivendor-db`
   - If you named it `postgres-db`: `DB_HOST=srv-captain--postgres-db`

### Step 2: Method B - Manually Create Database (Keep Container)

If you don't want to delete the app, manually create the database:

**1. SSH into your CapRover server:**
```bash
ssh root@185.208.172.76
```

**2. Find the PostgreSQL container:**
```bash
docker ps | grep postgres
```

**3. Enter the PostgreSQL container:**
```bash
# Replace with actual container name/ID from step 2
docker exec -it srv-captain--multivendor-db bash
```

**4. Connect to PostgreSQL as postgres user:**
```bash
psql -U postgres
```

**5. Create the database:**
```sql
CREATE DATABASE "multivendor-db";
```

**6. Verify it was created:**
```sql
\l
```
You should see `multivendor-db` in the list.

**7. Exit:**
```sql
\q
exit
```

**8. Restart your backend app** in CapRover

## Verification After Fix

Check your backend logs. You should see:

```
✅ Running migrations...
✅ Operations to perform:
   Apply all migrations: admin, auth, contenttypes, sessions, users, products, orders, blog
✅ Running migrations:
   Applying contenttypes.0001_initial... OK
   Applying auth.0001_initial... OK
   [more migrations...]
```

## Updated Environment Variables

### For New PostgreSQL App (multivendor-db or postgres-db):
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=thisIsAsimplePassword09
POSTGRES_DB=multivendor-db
POSTGRES_INITDB_ARGS=
```

### For Backend App (multivendor-backend):
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor-db
DB_USER=postgres
DB_PASSWORD=thisIsAsimplePassword09
DB_HOST=srv-captain--multivendor-db  # ← Or srv-captain--postgres-db
DB_PORT=5432
SECRET_KEY=tfu9y@exp6tdda$%f_+u&o80jd!%ld5@y=iua)$176x5bf(aut
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
CORS_ALLOWED_ORIGINS=https://multivendor-frontend.indexo.ir,https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
```

## After Database Is Working

Once the connection works, you'll need to:

1. **Run migrations** (should happen automatically on backend startup)
2. **Create superuser:**
   ```bash
   # SSH to server
   ssh root@185.208.172.76
   
   # Enter backend container
   docker exec -it srv-captain--multivendor-backend bash
   
   # Create superuser
   python manage.py createsuperuser
   ```

## Common Issues

### Issue: Still getting authentication errors
**Solution:** Double-check password has no special characters that need escaping

### Issue: "database does not exist"
**Solution:** The manual database creation (Method B) worked, but backend hasn't restarted yet

### Issue: Container keeps restarting
**Solution:** Check if port 5432 is already in use by another container

---

**Recommended:** Use **Method A** (delete and recreate) for a clean start. This is a fresh installation anyway, so you're not losing any valuable data.

**Time Estimate:** 5-10 minutes
**Risk:** None (fresh database)





# 🔧 Fix Authentication Token and Restore Data

## Problem 1: Invalid Authentication Token (403 on Detail Endpoints)

### Root Cause
Your Nuxt frontend is sending an old, invalid token:
```
Token 7670d04d8faf85dd2a5c47127626213fa906f5f2
```

This token doesn't exist in the database because migrations created fresh tables.

### Solution Options

#### Option A: Clear Frontend Token (Quickest)

**Clear browser localStorage:**

1. Open browser console (F12)
2. Run:
```javascript
localStorage.clear()
sessionStorage.clear()
location.reload()
```

**OR manually:**
- Go to Application tab → Local Storage
- Find and delete the auth token
- Refresh the page

#### Option B: Create New Admin User and Token

SSH into CapRover backend and create a new superuser:

```bash
# Find the backend container
docker ps | grep multivendor-backend

# Create superuser
docker exec -it <container_id> python manage.py createsuperuser

# Or create via shell
docker exec -it <container_id> python manage.py shell

# In Python shell:
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create superuser
user = User.objects.create_superuser(
    username='admin',
    email='admin@indexo.ir',
    password='your-secure-password'
)

# Create token
token = Token.objects.create(user=user)
print(f"Token: {token.key}")
```

Then update your frontend with the new token.

#### Option C: Fix Authentication Handling (Recommended for Public APIs)

Update the backend to handle invalid tokens gracefully for public endpoints.

## Problem 2: Lost Data (Products, Categories, etc.)

### Root Cause
Migrations ran on an empty database, creating fresh tables with no data.

### Solution: Restore Data from Backup OR Re-populate

#### Option 1: If You Have a Backup

**From database dump:**
```bash
# SSH into CapRover host
ssh root@185.208.172.76

# Find postgres container
docker ps | grep postgres-db

# Restore from backup
docker exec -i <postgres_container_id> psql -U postgres postgres < backup.sql
```

#### Option 2: Re-populate with Management Commands

**SSH into backend container:**
```bash
docker exec -it <backend_container_id> bash

# Run population commands
python manage.py populate_categories
python manage.py populate_departments  # if exists
python manage.py populate_products     # if exists
python manage.py populate_blog         # if exists
```

#### Option 3: Manual Data Entry

1. Login to admin: https://multivendor-backend.indexo.ir/admin/
2. Create departments, categories, products manually
3. Or import via Django admin actions

## Immediate Action Plan

### Step 1: Fix Auth Token Issue (Do This First)

**Quick fix - Clear token from frontend:**

1. Open https://indexo.ir/
2. Press F12 (Developer Console)
3. Run:
```javascript
localStorage.clear()
sessionStorage.clear()
location.reload()
```

This will remove the invalid token and allow public API access to work.

### Step 2: Verify API Works

After clearing localStorage, test:
```bash
curl https://multivendor-backend.indexo.ir/api/departments/general/
```

Should return 200 OK with data.

### Step 3: Restore or Re-create Data

**Check what data you have:**
```bash
# SSH into backend
docker exec -it <backend_container_id> python manage.py shell

# Check counts
from products.models import Product, Category, Department
print(f"Departments: {Department.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Products: {Product.objects.count()}")
```

**If you have old database backup:**
- Restore from backup (Option 1 above)

**If no backup:**
- Run management commands to populate sample data
- Or manually add your products via admin panel

## Preventing This in the Future

### 1. Regular Database Backups

Create a backup script:

```bash
#!/bin/bash
# backup-db.sh
docker exec <postgres_container_id> pg_dump -U postgres postgres > backup_$(date +%Y%m%d_%H%M%S).sql
```

Run daily via cron.

### 2. Test Migrations on Staging First

Before deploying to production:
1. Test migrations on a copy of production data
2. Verify data integrity
3. Then deploy to production

### 3. Separate Migration and Data Scripts

- Keep schema migrations separate from data population
- Use fixtures or data migration files for critical data

## Quick Commands Reference

### Check Backend Container Status
```bash
docker ps | grep multivendor-backend
docker logs <container_id> --tail 50
```

### Access Backend Shell
```bash
docker exec -it <container_id> bash
python manage.py shell
```

### Check Database
```bash
docker exec -it <backend_container_id> python manage.py dbshell
\dt  # List tables
SELECT COUNT(*) FROM products_product;
SELECT COUNT(*) FROM products_category;
\q   # Quit
```

### Create Superuser
```bash
docker exec -it <backend_container_id> python manage.py createsuperuser
```

## What Happened Timeline

1. ✅ Old system working with Vue frontend + data in database
2. 🔧 Migrated from Vue to Nuxt
3. 🚀 Deployed to CapRover
4. ⚠️  Migrations ran on empty database (fresh tables created)
5. ❌ Old auth tokens invalid
6. ❌ All data lost (tables empty except migration records)

## Expected Result After Fix

- ✅ `/api/departments/` returns 200 OK
- ✅ `/api/departments/general/` returns 200 OK (not 403)
- ✅ No auth errors in console
- ✅ Data visible on frontend (after restoration)











# 🚀 Run Project with Downloaded Database

This guide shows you how to restore the downloaded database and run your project locally.

## Quick Start (3 Steps)

### Step 1: Restore the Database

**Option A: Using the PowerShell Script (Recommended)**
```powershell
.\restore-local-database.ps1
```

**Option B: Manual Restore**
```powershell
# 1. Start database container
docker-compose -f docker-compose.local.yml up -d db

# 2. Wait for database to be ready (about 10 seconds)
Start-Sleep -Seconds 10

# 3. Decompress backup (if compressed)
$backup = ".\database_backups\multivendor_db_backup.sql.gz"
$uncompressed = ".\database_backups\multivendor_db_backup.sql"
[System.IO.Compression.GZipStream]::new([System.IO.File]::OpenRead($backup), [System.IO.Compression.CompressionMode]::Decompress).CopyTo([System.IO.File]::Create($uncompressed))

# 4. Restore database
Get-Content $uncompressed | docker exec -i multivendor_db_local psql -U postgres -d multivendor_db
```

### Step 2: Start Your Project

**Option A: Using Batch File (Easiest)**
```powershell
.\test-local.bat
```

**Option B: Using Docker Compose**
```powershell
docker-compose -f docker-compose.local.yml up --build
```

**Option C: Background Mode (Recommended)**
```powershell
docker-compose -f docker-compose.local.yml up -d --build
```

### Step 3: Access Your Application

Once services are running (wait for "healthy" status):

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Database**: localhost:5432 (for DB clients)

---

## Detailed Instructions

### Prerequisites

1. ✅ **Docker Desktop** must be running
2. ✅ **Database backup** downloaded (should be in `.\database_backups\`)

### Step-by-Step Guide

#### 1. Check Backup File

Verify your backup exists:
```powershell
Get-ChildItem .\database_backups\
```

You should see: `multivendor_db_backup.sql.gz` (or `.sql`)

#### 2. Restore Database

Run the restore script:
```powershell
.\restore-local-database.ps1
```

**What the script does:**
- ✅ Checks Docker is running
- ✅ Starts database container if needed
- ✅ Decompresses backup (if compressed)
- ✅ Adjusts database name (multivendor-db → multivendor_db)
- ✅ Drops existing local database
- ✅ Creates new database
- ✅ Restores all data from backup

#### 3. Start Project Services

**Full Start (with logs):**
```powershell
docker-compose -f docker-compose.local.yml up --build
```

**Background Start (detached):**
```powershell
docker-compose -f docker-compose.local.yml up -d --build
```

**Or use the batch file:**
```powershell
.\test-local.bat
```

#### 4. Verify Everything Works

**Check container status:**
```powershell
docker ps
```

All containers should show "healthy" status.

**Check backend logs:**
```powershell
docker-compose -f docker-compose.local.yml logs backend
```

**Check frontend logs:**
```powershell
docker-compose -f docker-compose.local.yml logs frontend
```

**Test API:**
```powershell
curl http://localhost:8000/api/
```

**Test Frontend:**
Open browser: http://localhost:8080

---

## Troubleshooting

### Database Container Not Found

**Error:** `No such container: multivendor_db_local`

**Solution:**
```powershell
docker-compose -f docker-compose.local.yml up -d db
```

### Database Already Exists

**Error:** `database "multivendor_db" already exists`

**Solution:** The restore script automatically drops and recreates the database. If you see this error manually, run:
```powershell
docker exec multivendor_db_local psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;"
docker exec multivendor_db_local psql -U postgres -c "CREATE DATABASE multivendor_db;"
```

### Database Name Mismatch

**Issue:** Production database is `multivendor-db` (hyphen), local uses `multivendor_db` (underscore)

**Solution:** The restore script automatically handles this conversion. If restoring manually, replace all occurrences in the SQL file:
```powershell
(Get-Content backup.sql) -replace 'multivendor-db', 'multivendor_db' | Set-Content backup.sql
```

### Port Already in Use

**Error:** `Port 8000/8080 is already in use`

**Solution:**
```powershell
# Find what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8080

# Stop other services or change ports in docker-compose.local.yml
```

### Docker Not Running

**Error:** `Cannot connect to Docker daemon`

**Solution:**
1. Open Docker Desktop
2. Wait for it to fully start (whale icon should be steady)
3. Try again

### Backend Can't Connect to Database

**Error:** `could not connect to server`

**Solution:**
```powershell
# 1. Check database is running
docker ps | findstr multivendor_db_local

# 2. Check database logs
docker-compose -f docker-compose.local.yml logs db

# 3. Restart database
docker-compose -f docker-compose.local.yml restart db

# 4. Wait a few seconds, then restart backend
docker-compose -f docker-compose.local.yml restart backend
```

---

## Common Commands

### Start Services
```powershell
# Start all services
docker-compose -f docker-compose.local.yml up -d

# Start specific service
docker-compose -f docker-compose.local.yml up -d db
docker-compose -f docker-compose.local.yml up -d backend
docker-compose -f docker-compose.local.yml up -d frontend
```

### Stop Services
```powershell
# Stop all services
docker-compose -f docker-compose.local.yml down

# Stop but keep volumes (preserves database)
docker-compose -f docker-compose.local.yml stop
```

### View Logs
```powershell
# All services
docker-compose -f docker-compose.local.yml logs -f

# Specific service
docker-compose -f docker-compose.local.yml logs -f backend
docker-compose -f docker-compose.local.yml logs -f frontend
docker-compose -f docker-compose.local.yml logs -f db
```

### Access Database
```powershell
# PostgreSQL shell
docker exec -it multivendor_db_local psql -U postgres -d multivendor_db

# Run SQL command
docker exec multivendor_db_local psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM products;"
```

### Rebuild After Code Changes
```powershell
# Rebuild specific service
docker-compose -f docker-compose.local.yml up --build backend

# Rebuild all services
docker-compose -f docker-compose.local.yml up --build
```

### Clean Everything (Reset)
```powershell
# Stop and remove containers, networks, and volumes
docker-compose -f docker-compose.local.yml down -v

# Then restore database again
.\restore-local-database.ps1
```

---

## Database Migration Notes

After restoring the database, Django migrations should be compatible. However, if you see migration errors:

```powershell
# Run migrations (inside backend container)
docker exec multivendor_backend_local python manage.py migrate

# Create superuser (if needed)
docker exec -it multivendor_backend_local python manage.py createsuperuser
```

---

## What's Different from Production?

| Aspect | Production (CapRover) | Local (Docker) |
|--------|----------------------|----------------|
| Database Name | `multivendor-db` | `multivendor_db` |
| Database Container | `srv-captain--postgres-db` | `multivendor_db_local` |
| Backend Container | `multivendor-backend` | `multivendor_backend_local` |
| Frontend Container | `multivendor-frontend` | `multivendor_frontend_local` |
| URLs | https://indexo.ir | http://localhost:8080 |
| Debug Mode | False | True |

---

## Next Steps

1. ✅ Database restored
2. ✅ Project running locally
3. 🎯 Test your application
4. 🎯 Make changes locally
5. 🎯 Deploy when ready

---

## Quick Reference

**Restore Database:**
```powershell
.\restore-local-database.ps1
```

**Start Project:**
```powershell
.\test-local.bat
```

**Stop Project:**
```powershell
docker-compose -f docker-compose.local.yml down
```

**View Logs:**
```powershell
docker-compose -f docker-compose.local.yml logs -f
```

---

## Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Check Docker Desktop is running
3. Check container logs: `docker-compose -f docker-compose.local.yml logs`
4. Verify backup file exists and is not corrupted


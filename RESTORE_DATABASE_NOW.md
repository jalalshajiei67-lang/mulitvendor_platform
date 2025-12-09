# 🚨 Emergency Database Restore Guide

Your backend lost connection with the database after deployment. Follow these steps to restore it.

## Step 1: Diagnose the Issue

First, let's check what's wrong:

```bash
# SSH into your VPS
ssh root@185.208.172.76

# Navigate to deployment directory
cd /home/deploy/docker-deploy

# Run diagnostic script
chmod +x diagnose-db-connection.sh
./diagnose-db-connection.sh
```

This will show you:
- If the database container is running
- If the database exists
- If the backend can connect
- What environment variables are set

## Step 2: Restore Database

### Option A: If you have a backup on the server

```bash
# Make sure you're in the deployment directory
cd /home/deploy/docker-deploy

# Make script executable
chmod +x restore-production-db.sh

# Run restore script
./restore-production-db.sh
```

The script will:
1. Find available backups
2. Ask you to select one
3. Backup current database (just in case)
4. Restore from backup
5. Restart backend

### Option B: Upload backup from your local machine

If you have a backup on your local machine (like `database_backups/multivendor_db_backup.sql.gz`):

```bash
# From your LOCAL machine (Windows PowerShell)
# Upload the backup to the server
scp database_backups/multivendor_db_backup.sql.gz root@185.208.172.76:/home/deploy/docker-deploy/

# Then SSH into server
ssh root@185.208.172.76
cd /home/deploy/docker-deploy

# Run restore script
chmod +x restore-production-db.sh
./restore-production-db.sh
# When asked for backup file, enter: multivendor_db_backup.sql.gz
```

### Option C: Manual restore (if scripts don't work)

```bash
# SSH into server
ssh root@185.208.172.76
cd /home/deploy/docker-deploy

# 1. Check database container
docker ps | grep multivendor_db

# 2. Drop and recreate database
docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;"
docker exec multivendor_db psql -U postgres -c "CREATE DATABASE multivendor_db;"

# 3. Restore from backup (replace path with your backup file)
gunzip -c /path/to/backup.sql.gz | docker exec -i multivendor_db psql -U postgres -d multivendor_db

# 4. Restart backend
docker compose restart backend
```

## Step 3: Verify Restoration

```bash
# Check backend logs
docker logs multivendor_backend --tail 50

# Test database connection
docker exec multivendor_backend python manage.py check --database default

# Check if tables exist
docker exec multivendor_db psql -U postgres -d multivendor_db -c "\dt"
```

## Step 4: Run Migrations (if needed)

```bash
docker exec multivendor_backend python manage.py migrate --noinput
```

## Common Issues

### Issue: "Database does not exist"
**Solution:** The database was recreated during deployment. Restore from backup.

### Issue: "Connection refused"
**Solution:** Check if database container is running:
```bash
docker ps | grep multivendor_db
docker compose up -d db
```

### Issue: "Password authentication failed"
**Solution:** Check environment variables match:
```bash
docker exec multivendor_backend printenv | grep DB_
docker exec multivendor_db printenv | grep POSTGRES
```

### Issue: "No backup found"
**Solution:** Upload your local backup:
```bash
# From local machine
scp database_backups/multivendor_db_backup.sql.gz root@185.208.172.76:/home/deploy/docker-deploy/
```

## Quick Commands Reference

```bash
# Check database status
docker ps | grep multivendor_db

# Check backend logs
docker logs multivendor_backend --tail 100

# Check database connection
docker exec multivendor_db psql -U postgres -c "\l"

# List tables in database
docker exec multivendor_db psql -U postgres -d multivendor_db -c "\dt"

# Restart all services
docker compose restart

# View backend environment variables
docker exec multivendor_backend printenv | grep DB_
```



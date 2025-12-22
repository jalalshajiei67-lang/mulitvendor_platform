# 🚨 Production Recovery Guide

## Quick Recovery Steps

Your production server crashed after deployment. Follow these steps to restore from backup.

### Prerequisites
- SSH access to VPS: `91.107.172.234`
- Backup files available (check `/root/crisis-backups-*` directories)
- Deployment directory: `/home/deploy/docker-deploy`

### Step 1: Transfer Recovery Script to VPS

**From your local machine:**

```bash
# Make transfer script executable
chmod +x transfer-recovery-script.sh

# Transfer recovery script
./transfer-recovery-script.sh
```

**Or manually:**

```bash
scp recover-production.sh root@91.107.172.234:/home/deploy/docker-deploy/
```

### Step 2: SSH to VPS and Run Recovery

```bash
# SSH to VPS
ssh root@91.107.172.234

# Navigate to deployment directory
cd /home/deploy/docker-deploy

# Make script executable
chmod +x recover-production.sh

# Run recovery script
./recover-production.sh
```

### Step 3: Follow the Interactive Prompts

The script will:

1. ✅ **Check prerequisites** - Verify Docker, containers, and files
2. 🔍 **Find backups** - Search for available backup files in:
   - `/root/crisis-backups-*`
   - `/home/deploy/docker-deploy/database_backups`
   - `/opt/multivendor_platform/backups`
   - Other common locations
3. 📋 **List backups** - Show all available backups with dates and sizes
4. ✅ **Select backup** - Choose which backup to restore from
5. 💾 **Create safety backup** - Backup current database before restore
6. 🔄 **Restore database** - Restore from selected backup
7. 🔙 **Optional Git rollback** - Rollback to previous working commit (if needed)
8. 🔄 **Restart services** - Restart backend and other services
9. ✅ **Verify recovery** - Check database connection and service health

### Step 4: Verify Everything Works

After recovery, verify:

```bash
# Check backend logs
docker logs multivendor_backend --tail 50

# Check database connection
docker exec multivendor_backend python manage.py check --database default

# Check container status
docker ps --filter "name=multivendor"

# Test API
curl https://api.indexo.ir/api/

# Test frontend
curl -I https://indexo.ir
```

### Manual Recovery (If Script Fails)

If the automated script doesn't work, you can restore manually:

#### 1. Find Your Backup

```bash
# List crisis backups
ls -lh /root/crisis-backups-*/

# Or check other locations
find /root -name "*.sql" -o -name "*.sql.gz" 2>/dev/null
find /home/deploy -name "*.sql" -o -name "*.sql.gz" 2>/dev/null
```

#### 2. Restore Database Manually

```bash
cd /home/deploy/docker-deploy

# Create safety backup first
docker exec multivendor_db pg_dump -U postgres multivendor_db > /tmp/safety_backup_$(date +%Y%m%d_%H%M%S).sql

# Prepare restore file (decompress if needed)
BACKUP_FILE="/root/crisis-backups-20251221-234333/database.sql"
RESTORE_FILE="/tmp/restore.sql"

if [[ "$BACKUP_FILE" == *.gz ]]; then
    gunzip -c "$BACKUP_FILE" > "$RESTORE_FILE"
else
    cp "$BACKUP_FILE" "$RESTORE_FILE"
fi

# Drop and recreate database
docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;"
docker exec multivendor_db psql -U postgres -c "CREATE DATABASE multivendor_db;"

# Restore database
cat "$RESTORE_FILE" | docker exec -i multivendor_db psql -U postgres -d multivendor_db

# Restart backend
docker compose -f docker-compose.production.yml restart backend
```

#### 3. Rollback Git Commit (Optional)

If you need to rollback to a previous working commit:

```bash
cd /home/deploy/docker-deploy

# View recent commits
git log --oneline -15

# Rollback to specific commit (replace COMMIT_HASH)
git fetch --all
git reset --hard COMMIT_HASH

# Rebuild and restart
docker compose -f docker-compose.production.yml build backend
docker compose -f docker-compose.production.yml up -d backend
```

### Troubleshooting

#### Database Container Not Running

```bash
# Start database container
docker compose -f docker-compose.production.yml up -d db

# Wait for it to be ready
sleep 10
docker exec multivendor_db pg_isready -U postgres
```

#### Backend Cannot Connect to Database

```bash
# Check database exists
docker exec multivendor_db psql -U postgres -l

# Check environment variables
docker exec multivendor_backend env | grep DB_

# Restart backend
docker compose -f docker-compose.production.yml restart backend
```

#### Frontend Still Shows Errors

After database restore, you may need to:

1. **Rebuild frontend** (if code was rolled back):
   ```bash
   docker compose -f docker-compose.production.yml build frontend
   docker compose -f docker-compose.production.yml up -d frontend
   ```

2. **Clear browser cache** - Frontend may be cached

3. **Check frontend logs**:
   ```bash
   docker logs multivendor_frontend --tail 50
   ```

### Backup Locations

The recovery script searches for backups in:

- `/root/crisis-backups-*` (crisis recovery backups)
- `/home/deploy/docker-deploy/database_backups`
- `/opt/multivendor_platform/backups`
- `/root/database_backups`
- `/root/backup-*`
- Current directory

### Safety Backups

The script automatically creates a safety backup before restoring:
- Location: `/root/safety-backup-before-restore-YYYYMMDD-HHMMSS/`
- Contains: Current database dump, Git commit info

### Important Notes

⚠️ **WARNING**: This will overwrite your current database!

✅ **Always**: The script creates a safety backup before restoring

🔄 **After restore**: You may need to run migrations if the backup is from an older version

📝 **Git rollback**: Only rollback Git if you're sure the code changes caused the issue

### Need Help?

If recovery fails:

1. Check the safety backup was created
2. Review container logs: `docker logs multivendor_backend`
3. Check database logs: `docker logs multivendor_db`
4. Verify network: `docker network ls | grep multivendor`
5. Check volumes: `docker volume ls | grep multivendor`

### Quick Reference

```bash
# Transfer script
./transfer-recovery-script.sh

# SSH and run
ssh root@185.208.172.76
cd /home/deploy/docker-deploy
./recover-production.sh

# Manual restore (if needed)
docker exec multivendor_db pg_dump -U postgres multivendor_db > /tmp/backup.sql
cat /path/to/backup.sql | docker exec -i multivendor_db psql -U postgres -d multivendor_db
docker compose -f docker-compose.production.yml restart backend
```

---

**Last Updated**: 2024-12-21
**VPS IP**: 91.107.172.234
**Deployment Path**: /home/deploy/docker-deploy


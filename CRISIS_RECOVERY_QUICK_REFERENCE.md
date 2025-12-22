# 🚨 Crisis Recovery Quick Reference - Production

## VPS Information
- **VPS IP**: `91.107.172.234`
- **SSH Command**: `ssh root@91.107.172.234`
- **Environment**: Production

## Quick Copy-Paste Commands

### 1. Upload Recovery Script to VPS

```bash
# From your local machine
scp crisis-recovery-production.sh root@91.107.172.234:/root/
ssh root@91.107.172.234 "chmod +x /root/crisis-recovery-production.sh"
```

### 2. Run Recovery Script

```bash
# SSH to VPS
ssh root@91.107.172.234

# Navigate to project directory
cd /path/to/mulitvendor_platform

# Run recovery script
bash /root/crisis-recovery-production.sh
# OR if script is in project directory:
bash crisis-recovery-production.sh
```

## Manual Recovery Steps (If Script Fails)

### Step 1: Check Current Status

```bash
# Check containers
docker ps -a | grep multivendor

# Check volumes
docker volume ls | grep -E "(postgres|static|media|redis)"

# Check network
docker network ls | grep multivendor
```

### Step 2: Backup Database

```bash
# Create backup directory
mkdir -p /root/backup-$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="/root/backup-$(date +%Y%m%d-%H%M%S)"

# Backup database
docker exec multivendor_db pg_dump -U postgres multivendor_db > $BACKUP_DIR/database.sql

# Backup volume info
docker volume ls > $BACKUP_DIR/volumes.txt
docker inspect multivendor_db > $BACKUP_DIR/db-info.json
docker inspect multivendor_backend > $BACKUP_DIR/backend-info.json
```

### Step 3: Verify Volumes

```bash
# Check if volumes exist
docker volume ls

# If missing, create them:
docker volume create postgres_data
docker volume create static_files
docker volume create media_files
docker volume create redis_data
```

### Step 4: Verify Network

```bash
# Check if network exists
docker network ls | grep multivendor_network

# If missing, create it:
docker network create multivendor_network
```

### Step 5: Check Volume Mounts

```bash
# Check backend mounts
docker inspect multivendor_backend --format '{{range .Mounts}}{{.Name}} -> {{.Destination}}{{"\n"}}{{end}}'

# Check nginx mounts
docker inspect multivendor_nginx --format '{{range .Mounts}}{{.Name}} -> {{.Destination}}{{"\n"}}{{end}}'

# Verify they share the same volumes
docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/static"}}{{.Name}}{{end}}{{end}}'
docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/static"}}{{.Name}}{{end}}{{end}}'
```

### Step 6: Restart Services (Safe Order)

```bash
# Navigate to project directory
cd /path/to/mulitvendor_platform

# Stop all services
docker-compose -f docker-compose.production.yml down

# Start database first
docker-compose -f docker-compose.production.yml up -d db

# Wait for database (check every 2 seconds, max 30 attempts)
for i in {1..30}; do
  if docker exec multivendor_db pg_isready -U postgres > /dev/null 2>&1; then
    echo "Database is ready!"
    break
  fi
  echo "Waiting for database... ($i/30)"
  sleep 2
done

# Start Redis
docker-compose -f docker-compose.production.yml up -d redis
sleep 3

# Start backend
docker-compose -f docker-compose.production.yml up -d backend
sleep 10

# Start nginx
docker-compose -f docker-compose.production.yml up -d nginx
sleep 3

# Start frontend
docker-compose -f docker-compose.production.yml up -d frontend
sleep 3

# Start traefik
docker-compose -f docker-compose.production.yml up -d traefik
```

### Step 7: Verify Connections

```bash
# Test database connection from backend
docker exec multivendor_backend python manage.py check --database default

# Check static files
docker exec multivendor_backend ls -1 /app/static | wc -l
docker exec multivendor_nginx ls -1 /usr/share/nginx/html/static | wc -l

# Check media files
docker exec multivendor_backend ls -1 /app/media | wc -l
docker exec multivendor_nginx ls -1 /usr/share/nginx/html/media | wc -l

# Test network connectivity
docker exec multivendor_backend ping -c 1 db
docker exec multivendor_backend ping -c 1 redis
```

### Step 8: Recollect Static Files

```bash
# Collect static files
docker exec multivendor_backend python manage.py collectstatic --noinput --clear

# Verify files were collected
docker exec multivendor_backend ls -1 /app/static | wc -l
docker exec multivendor_nginx ls -1 /usr/share/nginx/html/static | wc -l
```

## Common Issues & Solutions

### Issue 1: Database Connection Lost

**Symptoms:**
- Backend logs show: `could not connect to server`
- `docker exec multivendor_backend python manage.py check --database default` fails

**Solution:**
```bash
# 1. Check database is running
docker ps | grep multivendor_db

# 2. Test database connection
docker exec multivendor_db pg_isready -U postgres

# 3. Check network connectivity
docker exec multivendor_backend ping -c 1 db

# 4. Verify environment variables
docker exec multivendor_backend env | grep DB_

# 5. Restart backend
docker restart multivendor_backend
```

### Issue 2: Static Files Not Accessible

**Symptoms:**
- 404 errors on `/static/` URLs
- Admin panel has no CSS/JS
- Nginx cannot find static files

**Solution:**
```bash
# 1. Check if backend has static files
docker exec multivendor_backend ls -la /app/static

# 2. Check if nginx has static files
docker exec multivendor_nginx ls -la /usr/share/nginx/html/static

# 3. Verify volumes are shared
BACKEND_VOL=$(docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/static"}}{{.Name}}{{end}}{{end}}')
NGINX_VOL=$(docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/static"}}{{.Name}}{{end}}{{end}}')
echo "Backend volume: $BACKEND_VOL"
echo "Nginx volume: $NGINX_VOL"

# 4. Recollect static files
docker exec multivendor_backend python manage.py collectstatic --noinput --clear

# 5. Restart nginx
docker restart multivendor_nginx
```

### Issue 3: Media Files Not Accessible

**Symptoms:**
- Images return 404
- User uploads not visible

**Solution:**
```bash
# 1. Check if backend has media files
docker exec multivendor_backend ls -la /app/media

# 2. Check if nginx has media files
docker exec multivendor_nginx ls -la /usr/share/nginx/html/media

# 3. Verify volumes are shared
BACKEND_VOL=$(docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/media"}}{{.Name}}{{end}}{{end}}')
NGINX_VOL=$(docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/media"}}{{.Name}}{{end}}{{end}}')
echo "Backend volume: $BACKEND_VOL"
echo "Nginx volume: $NGINX_VOL"

# 4. Check permissions
docker exec multivendor_backend ls -ld /app/media

# 5. Restart nginx
docker restart multivendor_nginx
```

### Issue 4: Volume Mismatch

**Symptoms:**
- Backend and Nginx see different files
- Changes in backend don't appear in nginx

**Solution:**
```bash
# 1. Stop all services
docker-compose -f docker-compose.production.yml down

# 2. Verify volume names in docker-compose.production.yml
grep -A 2 "volumes:" docker-compose.production.yml

# 3. Check existing volumes
docker volume ls

# 4. If volumes don't match, update docker-compose.production.yml to use explicit volume names:
# volumes:
#   static_files:
#     name: static_files
#   media_files:
#     name: media_files

# 5. Restart services
docker-compose -f docker-compose.production.yml up -d
```

## Quick Health Check

```bash
# One-liner to check everything
echo "=== Containers ===" && \
docker ps --filter "name=multivendor" --format "table {{.Names}}\t{{.Status}}" && \
echo -e "\n=== Database ===" && \
docker exec multivendor_db pg_isready -U postgres && \
echo -e "\n=== Backend DB Connection ===" && \
docker exec multivendor_backend python manage.py check --database default && \
echo -e "\n=== Static Files ===" && \
echo "Backend: $(docker exec multivendor_backend ls -1 /app/static 2>/dev/null | wc -l) files" && \
echo "Nginx: $(docker exec multivendor_nginx ls -1 /usr/share/nginx/html/static 2>/dev/null | wc -l) files" && \
echo -e "\n=== Media Files ===" && \
echo "Backend: $(docker exec multivendor_backend ls -1 /app/media 2>/dev/null | wc -l) items" && \
echo "Nginx: $(docker exec multivendor_nginx ls -1 /usr/share/nginx/html/media 2>/dev/null | wc -l) items"
```

## Emergency Rollback

If something goes wrong, you can rollback:

```bash
# 1. Stop all services
docker-compose -f docker-compose.production.yml down

# 2. Restore from backup (if you have one)
# Find your backup directory
ls -la /root/backup-*

# 3. Restore database (if needed)
# docker exec -i multivendor_db psql -U postgres multivendor_db < /root/backup-YYYYMMDD-HHMMSS/database.sql

# 4. Restart services
docker-compose -f docker-compose.production.yml up -d
```

## Contact & Support

- **VPS**: 91.107.172.234
- **Project**: Multivendor Platform
- **Environment**: Production

## Notes

- Always backup before making changes
- Test in staging first if possible
- Monitor logs: `docker logs -f multivendor_backend`
- Check container health: `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"`


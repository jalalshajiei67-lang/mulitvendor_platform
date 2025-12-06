# 🆘 Quick Troubleshooting Guide

## Common Issues & Fast Fixes

### ❌ Issue: Can't SSH to VPS

**Quick Fix:**
```bash
# Test connection
ping 158.255.74.123

# Try SSH
ssh root@158.255.74.123
# Password: e<c6w:1EDupHjf4*
```

**If still fails:**
- Check VPS is running
- Verify IP address is correct
- Check firewall allows port 22

---

### ❌ Issue: Deployment script fails

**Quick Fix:**
```bash
# Windows
CHECK_BEFORE_DEPLOY.bat

# Ensure .env exists
copy env.production .env

# Try again
deploy-windows.bat
```

---

### ❌ Issue: Containers won't start

**Quick Fix:**
```bash
# SSH to VPS
ssh root@158.255.74.123
cd /opt/multivendor_platform

# Check status
docker-compose ps

# View logs
docker-compose logs

# Restart everything
docker-compose down
docker-compose up -d --build --force-recreate
```

---

### ❌ Issue: Application not accessible

**Quick Fix:**
```bash
# Check if containers are running
docker-compose ps

# Check firewall
ufw status

# Restart nginx
docker-compose restart nginx

# Check logs
docker-compose logs nginx
docker-compose logs backend
```

---

### ❌ Issue: 502 Bad Gateway

**Quick Fix:**
```bash
# Backend likely not responding
docker-compose logs backend

# Restart backend
docker-compose restart backend
docker-compose restart nginx

# If still failing
docker-compose down
docker-compose up -d --build
```

---

### ❌ Issue: Database connection error

**Quick Fix:**
```bash
# Check database
docker-compose logs db

# Restart database
docker-compose restart db

# Wait 10 seconds, then restart backend
sleep 10
docker-compose restart backend
```

---

### ❌ Issue: Static files not loading

**Quick Fix:**
```bash
# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Restart nginx
docker-compose restart nginx
```

---

### ❌ Issue: Media/image uploads not working

**Quick Fix:**
```bash
# Check permissions
docker-compose exec backend ls -la /app/media

# Recreate media directory
docker-compose exec backend mkdir -p /app/media
docker-compose exec backend chmod 755 /app/media

# Restart backend
docker-compose restart backend
```

---

### ❌ Issue: Admin panel not accessible

**Quick Fix:**
```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Restart services
docker-compose restart backend nginx
```

---

### ❌ Issue: Out of disk space

**Quick Fix:**
```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a -f

# Remove old images
docker image prune -a -f

# Check again
df -h
```

---

### ❌ Issue: High memory usage

**Quick Fix:**
```bash
# Check usage
docker stats

# Restart services
docker-compose restart

# If critical, restart everything
docker-compose down
docker-compose up -d
```

---

### ❌ Issue: Can't create superuser

**Quick Fix:**
```bash
# Ensure backend is running
docker-compose ps backend

# Try again
docker-compose exec backend python manage.py createsuperuser

# If still fails, check migrations
docker-compose exec backend python manage.py migrate
```

---

### ❌ Issue: Changes not appearing

**Quick Fix:**
```bash
# Frontend changes
docker-compose down frontend
docker-compose up -d --build frontend

# Backend changes
docker-compose exec backend python manage.py collectstatic --noinput
docker-compose restart backend

# Both
docker-compose down
docker-compose up -d --build
```

---

## 🔍 Diagnostic Commands

### Check Everything
```bash
./health-check.sh
./monitor.sh
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100
```

### Check Resources
```bash
# Container stats
docker stats

# Disk space
df -h

# Memory
free -h

# Processes
top
```

### Network
```bash
# Check nginx is listening
netstat -tulpn | grep :80

# Check DNS
nslookup yourdomain.com

# Test endpoint
curl http://localhost:80
curl http://localhost:80/api/
```

---

## 🚨 Emergency Recovery

### Nuclear Option (Complete Reset)
```bash
# BACKUP FIRST!
./backup-database.sh

# Stop and remove everything
docker-compose down -v

# Remove old images
docker system prune -a -f

# Rebuild from scratch
docker-compose up -d --build --force-recreate

# Restore database if needed
./restore-database.sh
```

### Restore from Backup
```bash
# List backups
ls -lh backups/

# Restore latest
./restore-database.sh
# Then type: latest
```

---

## 📞 Get More Help

### Full Troubleshooting
See: **DEPLOYMENT_GUIDE.md** (Troubleshooting section)

### Check Logs
```bash
# Application logs
docker-compose logs

# System logs
journalctl -xe

# Nginx error log
docker-compose exec nginx cat /var/log/nginx/error.log
```

### Interactive Help
```bash
./manage-deployment.sh
# Use menu option 4, 5, or 6 to view logs
```

---

## ✅ After Fixing

Always verify:
```bash
# Check containers
docker-compose ps

# Quick health check
./health-check.sh

# Test application
curl http://158.255.74.123
```

---

**Still stuck?** Check the comprehensive **DEPLOYMENT_GUIDE.md** for detailed solutions.




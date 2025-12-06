# 🚀 Docker Deployment Quick Checklist

## ⚠️ BEFORE FIRST RUN

### 1. Create .env File (REQUIRED!)
```bash
# Copy template
copy env.template .env

# Then edit .env and change:
- DB_PASSWORD=YOUR_SECURE_PASSWORD
- SECRET_KEY=GENERATE_NEW_KEY  # See below
- ALLOWED_HOSTS=your-domain.com
- CORS_ALLOWED_ORIGINS=https://your-domain.com
- DOMAIN=your-domain.com
- EMAIL=your-email@example.com
```

### 2. Generate Django Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy output to `.env` as `SECRET_KEY`

---

## 🏗️ BUILD & RUN

### First Time Setup
```bash
# Build all services
docker-compose build

# Start services in background
docker-compose up -d

# Check health status (wait ~1 minute)
docker-compose ps

# View logs
docker-compose logs -f
```

### Access Your Application
- **Website:** http://localhost
- **Admin:** http://localhost/admin/
- **API:** http://localhost/api/

---

## 🔄 COMMON COMMANDS

```bash
# View all services status
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
docker-compose logs -f db

# Restart a service
docker-compose restart backend

# Rebuild specific service
docker-compose build --no-cache backend
docker-compose up -d backend

# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ DELETES DATABASE!)
docker-compose down -v
```

---

## 🧪 VERIFY DEPLOYMENT

### Check Health (All should be "healthy")
```bash
docker-compose ps
```

Expected output:
```
NAME                      STATUS
multivendor_backend       Up (healthy)
multivendor_frontend      Up (healthy)
multivendor_db            Up (healthy)
multivendor_nginx         Up
multivendor_certbot       Up
```

### Test Endpoints
```bash
# Test frontend
curl http://localhost/

# Test API
curl http://localhost/api/

# Test admin (should redirect to login)
curl -I http://localhost/admin/
```

---

## 🐛 QUICK TROUBLESHOOTING

### Service Unhealthy?
```bash
# Check logs
docker-compose logs -f [service-name]

# Restart
docker-compose restart [service-name]

# Full rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Issues?
```bash
# Access database directly
docker-compose exec db psql -U postgres -d multivendor_db

# View database logs
docker-compose logs -f db

# Reset database (⚠️ DELETES ALL DATA!)
docker-compose down -v
docker-compose up -d
```

### Static Files Not Loading?
```bash
# Collect static files manually
docker-compose exec backend python manage.py collectstatic --noinput

# Restart backend
docker-compose restart backend
```

---

## 🔒 PRODUCTION DEPLOYMENT

### Before Going Live:
- [ ] .env file created with strong passwords
- [ ] SECRET_KEY is random and unique
- [ ] DEBUG=False in .env
- [ ] ALLOWED_HOSTS updated with your domain
- [ ] CORS_ALLOWED_ORIGINS updated with your domain
- [ ] Database password is strong (20+ characters)
- [ ] Firewall configured (allow 80, 443, block others)
- [ ] SSH key-based authentication enabled
- [ ] Regular backups configured

### Setup SSL (HTTPS):
```bash
# Edit .env with your domain
DOMAIN=yourdomain.com
EMAIL=your-email@example.com

# Run SSL setup script
./setup-ssl.sh
```

---

## 📊 MONITORING

### Check Resource Usage
```bash
# View container stats
docker stats

# View disk usage
docker system df
```

### Database Backup
```bash
# Manual backup
./backup-database.sh

# Setup automated backups (Linux/Mac)
./setup-cron-backup.sh
```

---

## 🔥 EMERGENCY PROCEDURES

### Rollback to Previous Version
```bash
# Stop current containers
docker-compose down

# Restore database from backup
./restore-database.sh

# Start with previous code version
git checkout [previous-commit]
docker-compose up -d
```

### Complete Reset (⚠️ Nuclear Option)
```bash
# Stop everything
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Remove orphaned volumes
docker volume prune

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

---

## ✅ CHANGES MADE TO YOUR PROJECT

### Files Modified:
1. **Dockerfile** - Added health check and curl dependency
2. **docker-compose.yml** - Added health checks for all services
3. **settings.py** - Removed hardcoded password, fixed MEDIA_ROOT duplication

### Files You Need to Create:
1. **.env** - Copy from `env.template` and customize

### No Breaking Changes:
- All existing functionality preserved
- Only improvements and security fixes applied

---

## 📚 DOCUMENTATION

- **Full Review:** `DOCKER_CONFIGURATION_REVIEW.md`
- **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
- **Troubleshooting:** `TROUBLESHOOTING_DEPLOYMENT.md`

---

## ⚡ QUICK START (Copy & Paste)

```bash
# 1. Create .env file
copy env.template .env
# Then edit .env with your values!

# 2. Build and run
docker-compose build
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f

# 5. Access app
# Open browser: http://localhost
```

**That's it! 🎉**


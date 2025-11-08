# Multivendor Platform - VPS Deployment Guide

Complete guide for deploying your Django + Vue.js application to a VPS using Docker.

## 📋 Prerequisites

- VPS with Ubuntu 20.04+ (Your IP: 158.255.74.123)
- Domain name pointed to your VPS IP (optional, for SSL)
- SSH access to VPS
- Local machine with Git and SSH client

## 🚀 Quick Start Deployment

### Step 1: Configure Environment Variables

1. Create `.env` file from template:
```bash
cp env.template .env
```

2. Edit `.env` with your settings:
```bash
# Required changes:
DB_PASSWORD=YourSecurePassword123!
SECRET_KEY=YourRandomSecretKey456!
ALLOWED_HOSTS=158.255.74.123,yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=http://158.255.74.123,http://yourdomain.com,https://yourdomain.com
```

3. Generate a secure SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Deploy to VPS

#### Option A: Automated Deployment (Recommended)

From your local machine:

```bash
chmod +x deploy.sh
./deploy.sh
```

This will:
- Create deployment package
- Upload to VPS
- Set up directory structure

Then SSH into your VPS and run:

```bash
ssh root@158.255.74.123
cd /opt/multivendor_platform
chmod +x server-deploy.sh
./server-deploy.sh
```

#### Option B: Manual Deployment

1. **Upload files to VPS:**
```bash
# Create deployment package
tar -czf deploy.tar.gz \
    --exclude='node_modules' \
    --exclude='venv' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git' \
    docker-compose.yml nginx/ Dockerfile requirements.txt multivendor_platform/

# Upload to VPS
scp deploy.tar.gz root@158.255.74.123:/tmp/
scp .env root@158.255.74.123:/tmp/deploy.env
```

2. **SSH into VPS:**
```bash
ssh root@158.255.74.123
```

3. **Set up project:**
```bash
# Create project directory
mkdir -p /opt/multivendor_platform
cd /opt/multivendor_platform

# Extract files
tar -xzf /tmp/deploy.tar.gz
mv /tmp/deploy.env .env

# Install Docker and Docker Compose
apt-get update
apt-get install -y docker.io docker-compose

# Start services
docker-compose up -d --build
```

### Step 3: Initial Setup

After deployment, run these commands on the VPS:

```bash
cd /opt/multivendor_platform

# Wait for services to start
sleep 15

# Run migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

### Step 4: Verify Deployment

1. **Check container status:**
```bash
docker-compose ps
```

All services should be "Up"

2. **Check logs:**
```bash
docker-compose logs -f
```

3. **Access your application:**
- Frontend: http://158.255.74.123
- Admin Panel: http://158.255.74.123/admin
- API: http://158.255.74.123/api

## 🔒 Enable HTTPS (Optional)

### Prerequisites
- Domain name pointed to your VPS
- DNS propagation completed (verify with `nslookup yourdomain.com`)

### Steps

1. **Update `.env` file:**
```bash
DOMAIN=yourdomain.com
EMAIL=your-email@example.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,158.255.74.123
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

2. **Run SSL setup:**
```bash
chmod +x setup-ssl.sh
./setup-ssl.sh yourdomain.com
```

3. **Restart services:**
```bash
docker-compose restart
```

Your site will now be available at `https://yourdomain.com`

## 📊 Management Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
docker-compose logs -f db
```

### Restart Services
```bash
# All services
docker-compose restart

# Specific service
docker-compose restart backend
```

### Stop Services
```bash
docker-compose down
```

### Start Services
```bash
docker-compose up -d
```

### Rebuild Services
```bash
docker-compose up -d --build
```

### Database Operations
```bash
# Access PostgreSQL
docker-compose exec db psql -U postgres -d multivendor_db

# Backup database
docker-compose exec db pg_dump -U postgres multivendor_db > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T db psql -U postgres multivendor_db
```

### Django Management
```bash
# Django shell
docker-compose exec backend python manage.py shell

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Run migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

## 🔧 Troubleshooting

### Issue: Containers won't start

**Solution:**
```bash
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up -d --build --force-recreate
```

### Issue: Database connection errors

**Solution:**
```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Issue: Frontend not loading

**Solution:**
```bash
# Check nginx logs
docker-compose logs nginx

# Check frontend logs
docker-compose logs frontend

# Verify frontend is running
docker-compose ps frontend
```

### Issue: 502 Bad Gateway

**Solution:**
```bash
# Check if backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Restart nginx
docker-compose restart nginx
```

### Issue: Static files not loading

**Solution:**
```bash
# Recollect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Restart nginx
docker-compose restart nginx
```

## 🔄 Updating Your Application

### Update Code

1. **Pull latest changes:**
```bash
cd /opt/multivendor_platform
# Upload new files using deploy.sh or manually
```

2. **Rebuild and restart:**
```bash
docker-compose down
docker-compose up -d --build
```

3. **Run migrations if needed:**
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```

## 📈 Performance Optimization

### Enable Gzip Compression
Already enabled in nginx configuration

### Database Optimization
```bash
# Access PostgreSQL
docker-compose exec db psql -U postgres -d multivendor_db

# Run VACUUM
VACUUM ANALYZE;
```

### Monitor Resources
```bash
# Check Docker stats
docker stats

# Check disk usage
df -h

# Check memory usage
free -h
```

## 🔐 Security Best Practices

1. **Change default passwords:**
   - Database password in `.env`
   - Django SECRET_KEY
   - Create strong superuser password

2. **Enable firewall:**
```bash
ufw enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
```

3. **Regular updates:**
```bash
apt-get update
apt-get upgrade
```

4. **Enable HTTPS** (see HTTPS section above)

5. **Backup regularly:**
```bash
# Backup script
docker-compose exec db pg_dump -U postgres multivendor_db > backup-$(date +%Y%m%d).sql
```

## 📞 Support

### Useful Links
- Docker Documentation: https://docs.docker.com
- Django Documentation: https://docs.djangoproject.com
- Vue.js Documentation: https://vuejs.org

### Check System Status
```bash
# Container status
docker-compose ps

# Resource usage
docker stats

# Disk space
df -h

# System logs
journalctl -xe
```

## 📝 Architecture Overview

```
┌─────────────────────────────────────────┐
│          Client Browser                  │
└────────────┬────────────────────────────┘
             │ HTTP/HTTPS
             ▼
┌─────────────────────────────────────────┐
│       Nginx Reverse Proxy               │
│  - Routes requests                      │
│  - Serves static files                  │
│  - SSL termination                      │
└──┬────────────┬─────────────────────────┘
   │            │
   │ /api/*     │ /*
   │ /admin/*   │
   ▼            ▼
┌──────────┐  ┌──────────┐
│ Django   │  │ Vue.js   │
│ Backend  │  │ Frontend │
│ (Gunicorn)│ │ (Nginx)  │
└────┬─────┘  └──────────┘
     │
     │ Database
     ▼
┌──────────┐
│PostgreSQL│
└──────────┘
```

## 🎯 Next Steps

1. ✅ Deploy application
2. ✅ Create superuser
3. ✅ Test all functionality
4. ⬜ Set up SSL certificate
5. ⬜ Configure domain
6. ⬜ Set up automated backups
7. ⬜ Configure monitoring
8. ⬜ Set up CI/CD pipeline

---

**Your VPS Information:**
- IP: 158.255.74.123
- SSH: `ssh root@158.255.74.123`
- Project Directory: `/opt/multivendor_platform`

**Quick Access:**
- Frontend: http://158.255.74.123
- Admin: http://158.255.74.123/admin
- API: http://158.255.74.123/api




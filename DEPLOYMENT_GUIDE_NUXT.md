# 🚀 Nuxt Deployment Guide

## Overview
This guide covers deploying the migrated Nuxt.js frontend to various environments.

---

## 📋 Pre-Deployment Checklist

- [ ] All API composables tested locally
- [ ] Nuxt app builds successfully (`npm run build`)
- [ ] Environment variables configured
- [ ] Docker Compose updated (✅ Done)
- [ ] Nginx config updated (✅ Done)
- [ ] CapRover apps created (if using CapRover)

---

## 🐳 Option 1: Docker Compose (Local/VPS)

### Step 1: Update Environment Variables

Create or update `.env` file:

```bash
# Backend
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com,185.208.172.76
CORS_ALLOWED_ORIGINS=https://your-domain.com
DB_PASSWORD=your-secure-db-password

# Frontend
NUXT_PUBLIC_API_BASE=http://backend:8000/api
```

### Step 2: Build and Deploy

```bash
# Stop existing containers
docker-compose down

# Build with new Nuxt configuration
docker-compose build --no-cache frontend

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f frontend
```

### Step 3: Verify Deployment

```bash
# Check frontend is running
curl http://localhost:3000

# Check backend API
curl http://localhost:8000/api/

# Check Nginx proxy
curl http://localhost
```

---

## 🎯 Option 2: CapRover Deployment (Recommended)

### Step 1: Create Apps in CapRover

1. **Login to CapRover**: https://captain.indexo.ir
2. **Create Backend App** (if not exists):
   - App Name: `multivendor-backend`
   - Enable HTTPS
   - Connect domain: `multivendor-backend.indexo.ir`

3. **Create Frontend App**:
   - App Name: `multivendor-frontend`
   - Enable HTTPS
   - Connect domain: `multivendor-frontend.indexo.ir` or `indexo.ir`

### Step 2: Configure Backend App

In CapRover backend app settings, add environment variables:

```
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://multivendor-frontend.indexo.ir
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=srv-captain--postgres
DB_PORT=5432
```

### Step 3: Configure Frontend App

In CapRover frontend app settings, add environment variable:

```
NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
```

**⚠️ IMPORTANT**: This must be set BEFORE deployment as it's embedded during build.

### Step 4: Deploy Using GitHub Actions

#### A. Setup GitHub Secrets

Go to your GitHub repo → Settings → Secrets and variables → Actions

Add these secrets:
- `CAPROVER_SERVER`: `https://captain.indexo.ir`
- `CAPROVER_APP_TOKEN`: Your CapRover app token
- `CAPROVER_BACKEND_APP`: `multivendor-backend`
- `CAPROVER_FRONTEND_APP`: `multivendor-frontend`

#### B. Push to Trigger Deployment

```bash
git add .
git commit -m "Deploy Nuxt frontend"
git push origin main
```

GitHub Actions will automatically:
1. Deploy backend first
2. Then deploy frontend
3. Show logs in Actions tab

### Step 5: Manual Deployment (Alternative)

If not using GitHub Actions:

```bash
# Install CapRover CLI
npm install -g caprover

# Login to CapRover
caprover login

# Deploy backend
cd /path/to/project
caprover deploy -a multivendor-backend

# Deploy frontend (with correct captain-definition)
caprover deploy -a multivendor-frontend
```

---

## 🔧 Option 3: Direct VPS Deployment

### Step 1: Setup VPS (185.208.172.76)

```bash
# SSH into VPS
ssh root@185.208.172.76

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt-get install docker-compose-plugin

# Clone repository
git clone https://github.com/your-username/mulitvendor_platform.git
cd mulitvendor_platform
```

### Step 2: Configure Environment

```bash
# Create .env file
nano .env

# Add production variables
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=185.208.172.76,your-domain.com
NUXT_PUBLIC_API_BASE=http://backend:8000/api
# ... other variables
```

### Step 3: Deploy with Docker Compose

```bash
# Build and start
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 4: Setup Nginx (if not using Docker Compose nginx)

```bash
# Install Nginx
apt-get install nginx

# Copy config
cp nginx/conf.d/default.conf /etc/nginx/sites-available/multivendor
ln -s /etc/nginx/sites-available/multivendor /etc/nginx/sites-enabled/

# Test and reload
nginx -t
systemctl reload nginx
```

---

## 🔍 Troubleshooting

### Frontend Not Loading

```bash
# Check frontend container
docker logs multivendor_frontend

# Check if Nuxt is running
docker exec multivendor_frontend ps aux | grep node

# Check port 3000
docker exec multivendor_frontend netstat -tlnp | grep 3000
```

### API Calls Failing

1. **Check NUXT_PUBLIC_API_BASE**:
   ```bash
   # In frontend container
   docker exec multivendor_frontend env | grep NUXT
   ```

2. **Check CORS settings** in backend:
   ```python
   # multivendor_platform/settings.py
   CORS_ALLOWED_ORIGINS = [
       'https://your-frontend-domain.com',
   ]
   ```

3. **Check Nginx proxy**:
   ```bash
   # Test backend through Nginx
   curl http://localhost/api/
   ```

### Build Failures

```bash
# Check build logs
docker-compose logs frontend

# Common issues:
# 1. Missing NUXT_PUBLIC_API_BASE - set in docker-compose.yml
# 2. Node version mismatch - check Dockerfile uses Node 20
# 3. Dependency issues - try npm ci --legacy-peer-deps
```

### Port Conflicts

```bash
# Check if port 3000 is in use
netstat -tlnp | grep 3000

# If using different port, update:
# 1. docker-compose.yml (expose and environment)
# 2. nginx/conf.d/default.conf (upstream frontend)
```

---

## 📊 Deployment Verification

### 1. Health Checks

```bash
# Frontend health
curl http://your-domain.com

# Backend health
curl http://your-domain.com/api/

# Admin panel
curl http://your-domain.com/admin/
```

### 2. Browser Tests

1. Open https://your-domain.com
2. Check browser console for errors
3. Test login/register
4. Test product listing
5. Test admin dashboard

### 3. Performance Checks

```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://your-domain.com

# Check container resources
docker stats
```

---

## 🔄 Update/Redeploy Process

### For CapRover:

```bash
# Just push to GitHub
git add .
git commit -m "Update frontend"
git push origin main
# GitHub Actions handles deployment
```

### For Docker Compose:

```bash
# Pull latest changes
git pull origin main

# Rebuild frontend
docker-compose build --no-cache frontend

# Restart
docker-compose up -d frontend

# Check logs
docker-compose logs -f frontend
```

---

## 🎯 Production Optimization

### 1. Enable Gzip Compression

Already configured in `nginx/nginx.conf` ✅

### 2. Setup CDN (Optional)

- Use Cloudflare for static assets
- Point DNS to your VPS/CapRover
- Enable caching rules

### 3. Database Optimization

```bash
# Regular backups
docker exec multivendor_db pg_dump -U postgres multivendor_db > backup.sql

# Optimize database
docker exec multivendor_backend python manage.py dbshell
# Run VACUUM ANALYZE;
```

### 4. Monitoring

- Setup Sentry for error tracking
- Use CapRover's built-in monitoring
- Setup uptime monitoring (UptimeRobot, etc.)

---

## 📝 Environment-Specific Configurations

### Development
```bash
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api
DEBUG=True
```

### Staging
```bash
NUXT_PUBLIC_API_BASE=https://staging-backend.indexo.ir/api
DEBUG=False
```

### Production
```bash
NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
DEBUG=False
SECURE_SSL_REDIRECT=True
```

---

## ✅ Post-Deployment Checklist

- [ ] Frontend loads correctly
- [ ] API calls work
- [ ] Authentication works (login/register)
- [ ] Admin dashboard accessible
- [ ] Static files loading (CSS, JS, images)
- [ ] Media files uploading
- [ ] SEO meta tags present
- [ ] SSL certificate active
- [ ] Monitoring setup
- [ ] Backup system configured

---

## 🆘 Support

If you encounter issues:

1. Check logs: `docker-compose logs -f frontend`
2. Verify environment variables
3. Test API endpoint directly
4. Check Nginx configuration
5. Review this guide's troubleshooting section

---

## 🎉 Success!

Your Nuxt frontend should now be deployed and running. The migration from Vue to Nuxt is complete!

**Next Steps:**
- Monitor performance
- Setup analytics
- Configure backups
- Plan for scaling












# CapRover Deployment Guide for Multivendor Platform

Complete guide for deploying your Django + Vue.js multivendor platform to CapRover.

## 📋 Prerequisites

- ✅ CapRover installed and running on your VPS
- ✅ Domain `indexo.ir` pointed to your VPS IP
- ✅ CapRover CLI installed locally
- ✅ SSH access to your VPS

## 🚀 Quick Deployment Steps

### Step 1: Install CapRover CLI (if not already installed)

```bash
npm install -g caprover
```

### Step 2: Login to CapRover

```bash
caprover login
```

Enter your CapRover dashboard URL (e.g., `https://captain.indexo.ir`) and your password.

### Step 3: Run the Deployment Script

```bash
chmod +x deploy-caprover.sh
./deploy-caprover.sh
```

This script will:
- Create the necessary CapRover apps
- Deploy PostgreSQL database
- Deploy Django backend
- Deploy Vue.js frontend
- Guide you through manual configuration steps

## 📝 Manual Configuration Steps

After running the deployment script, complete these steps in the CapRover dashboard:

### 1. Set Up PostgreSQL Database

1. Go to `https://captain.indexo.ir`
2. Click "One-Click Apps/Databases"
3. Install PostgreSQL
4. Configure:
   - **App Name**: `postgres-db`
   - **Database Name**: `multivendor_db`
   - **Username**: `postgres`
   - **Password**: `1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^`

### 2. Configure Backend Environment Variables

1. Go to `multivendor-backend` app
2. Click "App Configs" tab
3. Add these environment variables:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
SECRET_KEY=tfu9y@exp6tdda$%f_+u&o80jd!%ld5@y=iua)$176x5bf(aut
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
CORS_ALLOWED_ORIGINS=https://multivendor-frontend.indexo.ir,https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
STATIC_URL=/static/
STATIC_ROOT=/app/static
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
```

### 3. Configure Frontend Environment Variables

1. Go to `multivendor-frontend` app
2. Click "App Configs" tab
3. Add these environment variables:

```
VITE_API_BASE_URL=https://multivendor-backend.indexo.ir
VITE_DJANGO_ADMIN_URL=https://multivendor-backend.indexo.ir/admin/
VUE_APP_TITLE=Multivendor Platform
VUE_APP_DESCRIPTION=Your Multivendor E-commerce Platform
```

### 4. Configure Domains and SSL

#### Backend App (`multivendor-backend`):
1. Go to "HTTP Settings" tab
2. Enable "HTTPS" and "Force HTTPS"
3. Add custom domain: `multivendor-backend.indexo.ir`
4. Enable "Let's Encrypt SSL"

#### Frontend App (`multivendor-frontend`):
1. Go to "HTTP Settings" tab
2. Enable "HTTPS" and "Force HTTPS"
3. Add custom domain: `indexo.ir`
4. Enable "Let's Encrypt SSL"

### 5. Configure Persistent Directories

For the backend app (`multivendor-backend`):
1. Go to "App Configs" tab
2. Add persistent directory: `/app/media`
3. Add persistent directory: `/app/static`

## 🔧 Post-Deployment Setup

### 1. Run Django Migrations

```bash
caprover apps:logs multivendor-backend
```

Wait for the app to start, then run:

```bash
caprover apps:exec multivendor-backend --command "python manage.py migrate"
```

### 2. Create Superuser

```bash
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"
```

### 3. Collect Static Files

```bash
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
```

## 🌐 Access Your Application

After deployment and configuration:

- **Frontend**: https://multivendor-frontend.indexo.ir (or https://indexo.ir)
- **Backend API**: https://multivendor-backend.indexo.ir/api
- **Admin Panel**: https://multivendor-backend.indexo.ir/admin
- **CapRover Dashboard**: https://captain.indexo.ir

## 📊 Management Commands

### View Logs
```bash
# Backend logs
caprover apps:logs multivendor-backend

# Frontend logs
caprover apps:logs multivendor-frontend

# Database logs
caprover apps:logs postgres-db
```

### Restart Apps
```bash
caprover apps:restart multivendor-backend
caprover apps:restart multivendor-frontend
```

### Execute Commands
```bash
# Django shell
caprover apps:exec multivendor-backend --command "python manage.py shell"

# Run migrations
caprover apps:exec multivendor-backend --command "python manage.py migrate"

# Collect static files
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
```

### Database Operations
```bash
# Access PostgreSQL
caprover apps:exec postgres-db --command "psql -U postgres -d multivendor_db"

# Backup database
caprover apps:exec postgres-db --command "pg_dump -U postgres multivendor_db" > backup.sql
```

## 🔄 Updating Your Application

### 1. Update Code
```bash
# Make your changes locally
# Then run the deployment script again
./deploy-caprover.sh
```

### 2. Update Environment Variables
1. Go to CapRover dashboard
2. Update environment variables in "App Configs"
3. Restart the app

### 3. Run Migrations (if needed)
```bash
caprover apps:exec multivendor-backend --command "python manage.py migrate"
```

## 🔧 Troubleshooting

### Issue: App won't start
**Solution:**
1. Check logs: `caprover apps:logs multivendor-backend`
2. Verify environment variables are set correctly
3. Check if PostgreSQL is running: `caprover apps:logs postgres-db`

### Issue: Database connection errors
**Solution:**
1. Verify PostgreSQL app is running
2. Check database environment variables
3. Ensure database name, user, and password are correct

### Issue: Frontend not loading
**Solution:**
1. Check frontend logs: `caprover apps:logs multivendor-frontend`
2. Verify API URL in frontend environment variables
3. Check if backend is accessible

### Issue: SSL certificate not working
**Solution:**
1. Wait 5-10 minutes for Let's Encrypt to issue certificate
2. Check domain DNS is pointing to your VPS
3. Verify domain is added correctly in HTTP Settings

### Issue: Static files not loading
**Solution:**
1. Check if persistent directory is configured
2. Run: `caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"`
3. Restart the backend app

## 📈 Performance Optimization

### Enable Gzip Compression
Already configured in nginx frontend configuration.

### Database Optimization
```bash
caprover apps:exec postgres-db --command "psql -U postgres -d multivendor_db -c 'VACUUM ANALYZE;'"
```

### Monitor Resources
Use CapRover dashboard to monitor:
- CPU usage
- Memory usage
- Disk usage
- Network traffic

## 🔐 Security Best Practices

1. **Change default passwords**:
   - Database password
   - Django SECRET_KEY
   - CapRover root password

2. **Enable firewall** on your VPS:
   ```bash
   ufw enable
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   ```

3. **Regular updates**:
   - Update CapRover regularly
   - Update your VPS system packages

4. **Backup regularly**:
   ```bash
   # Backup database
   caprover apps:exec postgres-db --command "pg_dump -U postgres multivendor_db" > backup-$(date +%Y%m%d).sql
   ```

## 📝 Architecture Overview

```
┌─────────────────────────────────────────┐
│          Client Browser                  │
└────────────┬────────────────────────────┘
             │ HTTPS
             ▼
┌─────────────────────────────────────────┐
│       CapRover Load Balancer            │
│  - SSL termination                      │
│  - Request routing                      │
└──┬────────────┬─────────────────────────┘
   │            │
   │ indexo.ir  │ multivendor-backend.indexo.ir
   ▼            ▼
┌──────────┐  ┌──────────┐
│ Vue.js   │  │ Django   │
│ Frontend │  │ Backend  │
│ (Nginx)  │  │ (Gunicorn)│
└──────────┘  └────┬─────┘
                   │
                   │ Database
                   ▼
┌──────────┐
│PostgreSQL│
│ (CapRover)│
└──────────┘
```

## 🎯 Next Steps

1. ✅ Deploy application to CapRover
2. ✅ Configure environment variables
3. ✅ Set up SSL certificates
4. ✅ Create superuser account
5. ⬜ Test all functionality
6. ⬜ Set up automated backups
7. ⬜ Configure monitoring
8. ⬜ Set up CI/CD pipeline

---

**Your CapRover Information:**
- Dashboard: https://captain.indexo.ir
- Frontend: https://multivendor-frontend.indexo.ir (or https://indexo.ir)
- Backend: https://multivendor-backend.indexo.ir
- Admin: https://multivendor-backend.indexo.ir/admin

**Useful Commands:**
- View logs: `caprover apps:logs [app-name]`
- Restart app: `caprover apps:restart [app-name]`
- Execute command: `caprover apps:exec [app-name] --command "[command]"`

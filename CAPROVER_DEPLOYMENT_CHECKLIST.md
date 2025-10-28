# CapRover Deployment Checklist

Use this checklist to ensure a successful deployment of your Multivendor Platform to CapRover.

## ✅ Pre-Deployment Checklist

- [ ] CapRover is installed and running on your VPS
- [ ] Domain `indexo.ir` is pointed to your VPS IP
- [ ] CapRover CLI is installed locally (`npm install -g caprover`)
- [ ] You have access to CapRover dashboard at `https://captain.indexo.ir`
- [ ] All project files are ready for deployment

## 🚀 Deployment Steps

### Step 1: Login to CapRover
- [ ] Run `caprover login`
- [ ] Enter CapRover dashboard URL: `https://captain.indexo.ir`
- [ ] Enter your CapRover password
- [ ] Verify successful login

### Step 2: Run Deployment Script
- [ ] Make deployment script executable: `chmod +x deploy-caprover.sh`
- [ ] Run deployment script: `./deploy-caprover.sh`
- [ ] Follow the script prompts and complete manual steps

### Step 3: PostgreSQL Database Setup
- [ ] Go to CapRover dashboard → "One-Click Apps/Databases"
- [ ] Install PostgreSQL
- [ ] Configure PostgreSQL:
  - [ ] App Name: `postgres-db`
  - [ ] Database Name: `multivendor_db`
  - [ ] Username: `postgres`
  - [ ] Password: `1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^`
- [ ] Wait for PostgreSQL to start successfully

### Step 4: Backend App Configuration
- [ ] Go to `multivendor-backend` app in CapRover dashboard
- [ ] Navigate to "App Configs" tab
- [ ] Add all environment variables from `caprover-env-backend.txt`
- [ ] Set `DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover`
- [ ] Go to "App Configs" → "Persistent Directories"
- [ ] Add persistent directory: `/app/media`
- [ ] Add persistent directory: `/app/static`
- [ ] Go to "HTTP Settings" tab
- [ ] Enable "HTTPS" and "Force HTTPS"
- [ ] Add custom domain: `multivendor-backend.indexo.ir`
- [ ] Enable "Let's Encrypt SSL"
- [ ] Save all changes

### Step 5: Frontend App Configuration
- [ ] Go to `multivendor-frontend` app in CapRover dashboard
- [ ] Navigate to "App Configs" tab
- [ ] Add all environment variables from `caprover-env-frontend.txt`
- [ ] Go to "HTTP Settings" tab
- [ ] Enable "HTTPS" and "Force HTTPS"
- [ ] Add custom domain: `multivendor-frontend.indexo.ir` (or `indexo.ir` if you prefer)
- [ ] Enable "Let's Encrypt SSL"
- [ ] Save all changes

## 🔧 Post-Deployment Setup

### Step 6: Django Setup
- [ ] Wait for backend app to start (check logs: `caprover apps:logs multivendor-backend`)
- [ ] Run migrations: `caprover apps:exec multivendor-backend --command "python manage.py migrate"`
- [ ] Create superuser: `caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"`
- [ ] Collect static files: `caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"`

### Step 7: SSL Certificate Setup
- [ ] Wait 5-10 minutes for Let's Encrypt certificates to be issued
- [ ] Verify SSL is working for `https://multivendor-frontend.indexo.ir` (or `https://indexo.ir`)
- [ ] Verify SSL is working for `https://multivendor-backend.indexo.ir`

## ✅ Verification Checklist

### Application Access
- [ ] Frontend loads at `https://multivendor-frontend.indexo.ir` (or `https://indexo.ir`)
- [ ] Backend API accessible at `https://multivendor-backend.indexo.ir/api`
- [ ] Admin panel accessible at `https://multivendor-backend.indexo.ir/admin`
- [ ] Can login to admin panel with superuser account

### Functionality Tests
- [ ] Frontend can communicate with backend API
- [ ] Static files (CSS, JS, images) load correctly
- [ ] Media files (user uploads) work correctly
- [ ] Database operations work (create, read, update, delete)
- [ ] All major features of the application work

### Performance & Security
- [ ] HTTPS is enforced (HTTP redirects to HTTPS)
- [ ] SSL certificates are valid and not expired
- [ ] Application loads quickly
- [ ] No console errors in browser
- [ ] No server errors in logs

## 🔍 Troubleshooting Checklist

If something doesn't work, check:

### Backend Issues
- [ ] Check backend logs: `caprover apps:logs multivendor-backend`
- [ ] Verify environment variables are set correctly
- [ ] Check if PostgreSQL is running: `caprover apps:logs postgres-db`
- [ ] Verify database connection settings
- [ ] Check if migrations ran successfully

### Frontend Issues
- [ ] Check frontend logs: `caprover apps:logs multivendor-frontend`
- [ ] Verify API URL in frontend environment variables
- [ ] Check if backend is accessible from frontend
- [ ] Verify CORS settings in backend

### SSL Issues
- [ ] Check if domain DNS is pointing to your VPS
- [ ] Verify domain is added correctly in HTTP Settings
- [ ] Wait longer for Let's Encrypt certificate issuance
- [ ] Check CapRover logs for SSL errors

### Database Issues
- [ ] Check PostgreSQL logs: `caprover apps:logs postgres-db`
- [ ] Verify database credentials
- [ ] Check if database is accessible from backend
- [ ] Verify database name and user permissions

## 📊 Monitoring Checklist

### Regular Monitoring
- [ ] Set up monitoring for application uptime
- [ ] Monitor disk space usage
- [ ] Monitor memory and CPU usage
- [ ] Set up log monitoring and alerts
- [ ] Regular database backups

### Maintenance Tasks
- [ ] Update CapRover regularly
- [ ] Update system packages on VPS
- [ ] Monitor SSL certificate expiration
- [ ] Regular security updates
- [ ] Performance optimization reviews

## 🎯 Success Criteria

Your deployment is successful when:

- [ ] All applications are running without errors
- [ ] SSL certificates are working
- [ ] Frontend and backend communicate properly
- [ ] Database operations work correctly
- [ ] Admin panel is accessible
- [ ] All major features are functional
- [ ] Performance is acceptable
- [ ] Security measures are in place

## 📞 Support Resources

If you encounter issues:

1. **Check CapRover Documentation**: https://caprover.com/docs/
2. **Check Application Logs**: Use `caprover apps:logs [app-name]`
3. **CapRover Community**: https://github.com/caprover/caprover
4. **Django Documentation**: https://docs.djangoproject.com/
5. **Vue.js Documentation**: https://vuejs.org/guide/

---

**Quick Commands Reference:**
```bash
# View logs
caprover apps:logs multivendor-backend
caprover apps:logs multivendor-frontend
caprover apps:logs postgres-db

# Restart apps
caprover apps:restart multivendor-backend
caprover apps:restart multivendor-frontend

# Execute commands
caprover apps:exec multivendor-backend --command "python manage.py migrate"
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
```

**Your URLs:**
- Frontend: https://multivendor-frontend.indexo.ir (or https://indexo.ir)
- Backend: https://multivendor-backend.indexo.ir
- Admin: https://multivendor-backend.indexo.ir/admin
- CapRover Dashboard: https://captain.indexo.ir

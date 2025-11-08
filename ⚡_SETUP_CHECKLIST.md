# ⚡ CapRover Setup Checklist

Use this checklist to track your setup progress!

## 📋 Prerequisites
- [x] CapRover installed and running
- [x] Apps created: `multivendor-backend`, `multivendor-frontend`, `postgres-db`
- [ ] CapRover CLI installed on your computer
- [ ] Logged into CapRover CLI

---

## 🗄️ Step 1: Database Setup
- [ ] Configure `postgres-db` environment variables
  - [ ] `POSTGRES_DB=multivendor_db`
  - [ ] `POSTGRES_USER=postgres`
  - [ ] `POSTGRES_PASSWORD=1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^`
- [ ] Save and restart postgres-db
- [ ] Verify database is running (check logs)

---

## 🔧 Step 2: Backend Configuration

### Environment Variables
- [ ] Open `multivendor-backend` app
- [ ] Go to "App Configs" → "Environmental Variables"
- [ ] Add all backend environment variables (see guide)
  - [ ] Database settings (DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
  - [ ] Django settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
  - [ ] CORS settings (CORS_ALLOWED_ORIGINS, CORS_ALLOW_ALL_ORIGINS)
  - [ ] Static/Media settings (STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT)
  - [ ] Django settings module (DJANGO_SETTINGS_MODULE)
- [ ] Save and update

### Persistent Storage
- [ ] Add persistent directory: `/app/staticfiles`
- [ ] Add persistent directory: `/app/media`
- [ ] Save and update

### HTTP Settings
- [ ] Go to "HTTP Settings" tab
- [ ] Enable HTTPS
- [ ] Enable Force HTTPS
- [ ] Add custom domain: `multivendor-backend.indexo.ir`
- [ ] Enable SSL certificate
- [ ] Save

---

## 🎨 Step 3: Frontend Configuration

### Environment Variables
- [ ] Open `multivendor-frontend` app
- [ ] Go to "App Configs" → "Environmental Variables"
- [ ] Add all frontend environment variables:
  - [ ] `VITE_API_BASE_URL=https://multivendor-backend.indexo.ir`
  - [ ] `VITE_DJANGO_ADMIN_URL=https://multivendor-backend.indexo.ir/admin/`
  - [ ] `VUE_APP_TITLE=Multivendor Platform`
  - [ ] `VUE_APP_DESCRIPTION=Your Multivendor E-commerce Platform`
- [ ] Save and update

### HTTP Settings
- [ ] Go to "HTTP Settings" tab
- [ ] Enable HTTPS
- [ ] Enable Force HTTPS
- [ ] Add custom domain: `indexo.ir`
- [ ] (Optional) Add custom domain: `www.indexo.ir`
- [ ] Enable SSL certificate
- [ ] Save

---

## 🚀 Step 4: Deploy Code

- [ ] Open PowerShell in project directory
- [ ] Deploy backend: `caprover deploy -a multivendor-backend`
- [ ] Wait for deployment to complete
- [ ] Deploy frontend: `caprover deploy -a multivendor-frontend`
- [ ] Wait for deployment to complete

---

## 🔨 Step 5: Django Setup

- [ ] Run migrations: `caprover apps:exec multivendor-backend --command "python manage.py migrate"`
- [ ] Create superuser: `caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"`
- [ ] Collect static files: `caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"`

---

## ✅ Step 6: Verification

### Check Logs
- [ ] Backend logs: `caprover apps:logs multivendor-backend`
- [ ] Frontend logs: `caprover apps:logs multivendor-frontend`
- [ ] Database logs: `caprover apps:logs postgres-db`
- [ ] No errors in any logs

### Access Apps
- [ ] Frontend accessible at: https://indexo.ir
- [ ] Backend API accessible at: https://multivendor-backend.indexo.ir/api
- [ ] Admin panel accessible at: https://multivendor-backend.indexo.ir/admin
- [ ] Can login to admin panel
- [ ] SSL certificates valid (green padlock)

### Test Functionality
- [ ] Browse frontend pages
- [ ] No console errors in browser
- [ ] Backend API responds correctly
- [ ] Static files (CSS/JS) loading properly
- [ ] Images and media files work

---

## 🎯 Quick Commands Reference

### Deploy
```powershell
# Deploy both apps
.\DEPLOY_TO_CAPROVER.bat

# Or manually:
caprover deploy -a multivendor-backend
caprover deploy -a multivendor-frontend
```

### View Logs
```powershell
caprover apps:logs multivendor-backend
caprover apps:logs multivendor-frontend
caprover apps:logs postgres-db
```

### Django Commands
```powershell
# Migrations
caprover apps:exec multivendor-backend --command "python manage.py migrate"

# Superuser
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"

# Static files
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
```

### Restart Apps
```powershell
caprover apps:restart multivendor-backend
caprover apps:restart multivendor-frontend
```

---

## 📱 Your URLs

- **CapRover Dashboard**: https://captain.indexo.ir
- **Frontend**: https://indexo.ir
- **Backend API**: https://multivendor-backend.indexo.ir/api
- **Admin Panel**: https://multivendor-backend.indexo.ir/admin

---

## 🔧 Troubleshooting

### If backend won't start:
1. Check logs: `caprover apps:logs multivendor-backend`
2. Verify environment variables in dashboard
3. Check database is running
4. Restart: `caprover apps:restart multivendor-backend`

### If SSL not working:
1. Wait 5-10 minutes
2. Check DNS records point to VPS IP
3. Verify domain is added correctly

### If static files not loading:
1. Run: `caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput --clear"`
2. Check persistent directories are configured
3. Restart backend app

---

## 📚 Documentation

For detailed instructions, see:
- **Main Guide**: `🚀_CAPROVER_FRESH_SETUP_GUIDE.md`
- **Deployment Guide**: `CAPROVER_DEPLOYMENT_GUIDE.md`
- **Troubleshooting**: Check logs and review error messages

---

## ✨ Success Criteria

Your setup is complete when:
- ✅ All apps running without errors
- ✅ Frontend loads at https://indexo.ir
- ✅ Backend API responds
- ✅ Admin panel works
- ✅ SSL certificates valid
- ✅ No console errors
- ✅ Can login and use the platform

---

**Current Status**: 🟡 In Progress

Update this as you complete steps!

**Started**: _________  
**Completed**: _________



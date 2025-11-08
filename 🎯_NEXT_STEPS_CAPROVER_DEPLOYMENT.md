# 🎯 Next Steps: Deploy to CapRover

## ✅ What Was Completed

All configuration files have been updated with:
- ✅ Secure Django SECRET_KEY generated
- ✅ Secure Database PASSWORD generated  
- ✅ All URLs updated to use `multivendor-backend.indexo.ir` and `multivendor-frontend.indexo.ir`
- ✅ CORS settings configured correctly
- ✅ Environment files updated
- ✅ Docker configurations updated
- ✅ Documentation updated

## 🔐 Your Credentials

**SAVE THESE SECURELY!**

```
Django SECRET_KEY: tfu9y@exp6tdda$%f_+u&o80jd!%ld5@y=iua)$176x5bf(aut
Database PASSWORD: 1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^
```

## 🚀 Deployment Steps

### Step 1: Add Environment Variables to CapRover

#### For Backend App (`multivendor-backend`):

1. Go to https://captain.indexo.ir
2. Click on **Apps** → **multivendor-backend**
3. Click **App Configs** tab
4. Scroll to **Environment Variables** section
5. Click **Bulk Edit**
6. Copy and paste this:

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
CORS_ALLOWED_ORIGINS=https://multivendor-frontend.indexo.ir,https://indexo.ir,https://www.indexo.ir,http://multivendor-frontend.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
STATIC_URL=/static/
STATIC_ROOT=/app/static
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
```

7. Click **Save & Update**

#### For Frontend App (`multivendor-frontend`):

1. Click on **Apps** → **multivendor-frontend**
2. Click **App Configs** tab
3. Scroll to **Environment Variables** section
4. Click **Bulk Edit**
5. Copy and paste this:

```
VITE_API_BASE_URL=https://multivendor-backend.indexo.ir
VITE_DJANGO_ADMIN_URL=https://multivendor-backend.indexo.ir/admin/
VUE_APP_TITLE=Multivendor Platform
VUE_APP_DESCRIPTION=Your Multivendor E-commerce Platform
```

6. Click **Save & Update**

### Step 2: Configure Custom Domains & SSL

#### Backend Domain:
1. Go to **multivendor-backend** app
2. Click **HTTP Settings** tab
3. Enable ☑️ **HTTPS**
4. Enable ☑️ **Force HTTPS**
5. In **Custom Domain** section, add: `multivendor-backend.indexo.ir`
6. Enable ☑️ **Let's Encrypt SSL**
7. Click **Save & Update**

#### Frontend Domain:
1. Go to **multivendor-frontend** app
2. Click **HTTP Settings** tab
3. Enable ☑️ **HTTPS**
4. Enable ☑️ **Force HTTPS**
5. In **Custom Domain** section, add: `multivendor-frontend.indexo.ir`
6. Enable ☑️ **Let's Encrypt SSL**
7. Click **Save & Update**

### Step 3: Set Up PostgreSQL Database

1. In CapRover Dashboard, click **Apps**
2. Click **One-Click Apps/Databases**
3. Search for **PostgreSQL**
4. Click **PostgreSQL**
5. Fill in:
   - **App Name**: `postgres-db`
   - **PostgreSQL Version**: 15 (or latest)
   - **Database Name**: `multivendor_db`
   - **Username**: `postgres`
   - **Password**: `1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^`
6. Click **Deploy**
7. Wait for deployment to complete (check logs)

### Step 4: Deploy Your Code

You need to push your code to CapRover. Choose one method:

#### Method A: Using Git (Recommended)
```powershell
# Add all changes
git add .

# Commit changes
git commit -m "Update configuration for CapRover deployment"

# If you have CapRover git remote configured:
git push caprover main
```

#### Method B: Using CapRover CLI
```powershell
# For backend
cd multivendor_platform
caprover deploy

# For frontend  
cd multivendor_platform/front_end
caprover deploy
```

#### Method C: Manual in Dashboard
1. Create a `.tar.gz` of your code
2. Upload via CapRover Dashboard → Apps → [app-name] → Deployment tab

### Step 5: Run Django Migrations

After backend deployment completes:

```powershell
# Run migrations
caprover apps:exec multivendor-backend --command "python manage.py migrate"

# Create superuser (follow prompts)
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"

# Collect static files
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
```

### Step 6: Verify Everything Works

Visit these URLs and verify:

✅ **Frontend**: https://multivendor-frontend.indexo.ir
✅ **Backend API**: https://multivendor-backend.indexo.ir/api/
✅ **Admin Panel**: https://multivendor-backend.indexo.ir/admin/

## 📊 View Logs

If something doesn't work, check logs:

```powershell
# Backend logs
caprover apps:logs multivendor-backend

# Frontend logs
caprover apps:logs multivendor-frontend

# Database logs
caprover apps:logs postgres-db
```

## 🔍 Common Issues & Solutions

### Issue: Frontend can't connect to backend
**Solution:**
- Check backend logs for CORS errors
- Verify `CORS_ALLOWED_ORIGINS` includes frontend URL
- Verify `VITE_API_BASE_URL` in frontend env vars

### Issue: SSL not working
**Solution:**
- Wait 5-10 minutes for Let's Encrypt to issue certificates
- Verify your domain DNS points to VPS IP
- Check "Enable HTTPS" and "Force HTTPS" are checked

### Issue: Database connection error
**Solution:**
- Verify PostgreSQL is running: `caprover apps:logs postgres-db`
- Check `DB_PASSWORD` matches in both places
- Verify `DB_HOST=srv-captain--postgres-db`

### Issue: Static files not loading
**Solution:**
- Make sure you ran: `python manage.py collectstatic --noinput`
- Check persistent directories are configured in backend app

## 📁 Files Modified

Here's what was changed in your project:

### Configuration Files:
- ✅ `caprover-env-backend.txt` - Backend environment variables
- ✅ `caprover-env-frontend.txt` - Frontend environment variables
- ✅ `env.template` - Environment template
- ✅ `env.production` - Production environment
- ✅ `.env` - Created from env.production

### Code Files:
- ✅ `multivendor_platform/multivendor_platform/multivendor_platform/settings_caprover.py`
- ✅ `multivendor_platform/front_end/Dockerfile`
- ✅ `docker-compose.yml`

### Documentation:
- ✅ `CAPROVER_DEPLOYMENT_GUIDE.md`
- ✅ `CAPROVER_DEPLOYMENT_CHECKLIST.md`
- ✅ `AXIOS_TO_DJANGO_CONNECTION_GUIDE.md`
- ✅ `CONFIGURATION_UPDATE_SUMMARY.md` (NEW)

## 🎉 Success Checklist

Your deployment is successful when:
- [ ] Backend accessible at https://multivendor-backend.indexo.ir/api/
- [ ] Frontend accessible at https://multivendor-frontend.indexo.ir
- [ ] Admin panel accessible at https://multivendor-backend.indexo.ir/admin
- [ ] SSL certificates working (green padlock in browser)
- [ ] Can login to admin panel
- [ ] Frontend can fetch data from backend API
- [ ] No CORS errors in browser console

## 📞 Need Help?

- Check detailed guide: `CONFIGURATION_UPDATE_SUMMARY.md`
- Check deployment guide: `CAPROVER_DEPLOYMENT_GUIDE.md`
- Check deployment checklist: `CAPROVER_DEPLOYMENT_CHECKLIST.md`
- CapRover Docs: https://caprover.com/docs/
- View logs with: `caprover apps:logs [app-name]`

---

**🎯 Your URLs:**
- Frontend: https://multivendor-frontend.indexo.ir
- Backend: https://multivendor-backend.indexo.ir
- Admin: https://multivendor-backend.indexo.ir/admin
- Dashboard: https://captain.indexo.ir

**Good luck with your deployment! 🚀**


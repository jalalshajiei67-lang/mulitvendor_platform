# 🚀 CapRover Fresh Setup Guide

## Current Status
✅ CapRover installed  
✅ Apps created:
- `multivendor-backend`
- `multivendor-frontend`
- `postgres-db`

Now let's configure everything step by step!

---

## 📝 STEP 1: Set Up PostgreSQL Database

### Option A: Using One-Click Apps (Recommended)
1. Go to CapRover dashboard: `https://captain.indexo.ir`
2. Click **"Apps"** in the left sidebar
3. Find **`postgres-db`** in your apps list
4. Click on it
5. Go to **"App Configs"** tab
6. Set these environment variables:

```
POSTGRES_DB=multivendor_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^
```

7. Click **"Save & Update"**
8. Wait for the app to restart

### Option B: If using One-Click App Install
1. Go to **"One-Click Apps/Databases"**
2. Search for **PostgreSQL**
3. Click **"PostgreSQL"**
4. Configure:
   - **App Name**: `postgres-db`
   - **PostgreSQL Version**: 16 (or latest)
   - **Database Name**: `multivendor_db`
   - **Username**: `postgres`
   - **Password**: `1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^`
5. Click **"Deploy"**

---

## 📝 STEP 2: Configure Backend Environment Variables

1. Go to **`multivendor-backend`** app
2. Click **"App Configs"** tab
3. Scroll to **"Environmental Variables"** section
4. Add these environment variables (click "Bulk Edit" for easier input):

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
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
```

5. Click **"Save & Update"**

### Configure Persistent Storage for Backend
1. Still in **`multivendor-backend`** app
2. Scroll to **"Persistent Directories"** section
3. Add these paths:
   - Path in App: `/app/staticfiles` → Label: `staticfiles`
   - Path in App: `/app/media` → Label: `media`
4. Click **"Save & Update"**

---

## 📝 STEP 3: Configure Frontend Environment Variables

1. Go to **`multivendor-frontend`** app
2. Click **"App Configs"** tab
3. Add these environment variables (use "Bulk Edit"):

```
VITE_API_BASE_URL=https://multivendor-backend.indexo.ir
VITE_DJANGO_ADMIN_URL=https://multivendor-backend.indexo.ir/admin/
VUE_APP_TITLE=Multivendor Platform
VUE_APP_DESCRIPTION=Your Multivendor E-commerce Platform
```

4. Click **"Save & Update"**

---

## 📝 STEP 4: Configure Domains and Enable SSL

### For Backend App (`multivendor-backend`)
1. Go to **`multivendor-backend`** app
2. Click **"HTTP Settings"** tab
3. Check these boxes:
   - ✅ **"HTTPS"**
   - ✅ **"Force HTTPS"**
   - ✅ **"Websocket Support"** (optional but recommended)
4. In **"Custom Domains"** section:
   - Add domain: `multivendor-backend.indexo.ir`
   - Click **"Connect New Domain"**
5. After domain is added, click **"Enable HTTPS"**
6. Check **"Force HTTPS"**
7. Click **"Save & Update"**

### For Frontend App (`multivendor-frontend`)
1. Go to **`multivendor-frontend`** app
2. Click **"HTTP Settings"** tab
3. Check these boxes:
   - ✅ **"HTTPS"**
   - ✅ **"Force HTTPS"**
4. In **"Custom Domains"** section:
   - Add domain: `indexo.ir`
   - Click **"Connect New Domain"**
   - Optionally add: `www.indexo.ir`
5. After domain is added, click **"Enable HTTPS"**
6. Check **"Force HTTPS"**
7. Click **"Save & Update"**

**⏰ Note:** SSL certificates may take 5-10 minutes to be issued by Let's Encrypt.

---

## 📝 STEP 5: Deploy Your Code

### Deploy Backend

Open PowerShell in your project directory and run:

```powershell
# Navigate to project directory
cd C:\Users\F003\Desktop\damirco

# Deploy backend
caprover deploy -a multivendor-backend
```

Wait for deployment to complete. You should see:
```
✔ Deployed successfully!
```

### Deploy Frontend

```powershell
# Deploy frontend (in the same directory)
caprover deploy -a multivendor-frontend
```

Wait for deployment to complete.

---

## 📝 STEP 6: Run Django Migrations and Setup

After backend deployment is complete, run these commands:

### 1. Run Migrations
```powershell
caprover apps:exec multivendor-backend --command "python manage.py migrate"
```

### 2. Create Superuser (Interactive)
```powershell
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"
```

Follow the prompts to create your admin account:
- Username: (your choice)
- Email: (your choice)
- Password: (your choice)

### 3. Collect Static Files (if not done automatically)
```powershell
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
```

---

## 📝 STEP 7: Verify Everything Works

### Check Logs
```powershell
# Check backend logs
caprover apps:logs multivendor-backend

# Check frontend logs
caprover apps:logs multivendor-frontend

# Check database logs
caprover apps:logs postgres-db
```

### Access Your Apps

1. **Frontend**: https://indexo.ir
2. **Backend API**: https://multivendor-backend.indexo.ir/api
3. **Admin Panel**: https://multivendor-backend.indexo.ir/admin
4. **CapRover Dashboard**: https://captain.indexo.ir

---

## 🔧 Troubleshooting

### Issue: Backend won't start

**Check logs:**
```powershell
caprover apps:logs multivendor-backend
```

**Common fixes:**
1. Verify all environment variables are set
2. Check database connection:
   ```powershell
   caprover apps:exec postgres-db --command "psql -U postgres -l"
   ```
3. Restart backend:
   ```powershell
   caprover apps:restart multivendor-backend
   ```

### Issue: Database connection refused

**Solution:**
1. Make sure `postgres-db` is running:
   ```powershell
   caprover apps:logs postgres-db
   ```
2. Verify `DB_HOST=srv-captain--postgres-db` (note the double dash `--`)
3. Check database credentials match between postgres-db and backend

### Issue: Frontend shows "Cannot connect to backend"

**Solution:**
1. Check if backend is running and accessible
2. Verify `VITE_API_BASE_URL` in frontend environment variables
3. Check CORS settings in backend
4. Check browser console for errors

### Issue: SSL certificate not working

**Solution:**
1. Wait 5-10 minutes for Let's Encrypt
2. Verify DNS records:
   - `indexo.ir` → Your VPS IP
   - `multivendor-backend.indexo.ir` → Your VPS IP
3. Check if ports 80 and 443 are open on your VPS

### Issue: Static files (CSS/JS) not loading

**Solution:**
1. Run collectstatic:
   ```powershell
   caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput --clear"
   ```
2. Verify persistent directories are configured
3. Restart backend:
   ```powershell
   caprover apps:restart multivendor-backend
   ```

---

## 📊 Useful Management Commands

### View Real-time Logs
```powershell
caprover apps:logs multivendor-backend -f
```

### Restart Apps
```powershell
caprover apps:restart multivendor-backend
caprover apps:restart multivendor-frontend
```

### Execute Django Commands
```powershell
# Django shell
caprover apps:exec multivendor-backend --command "python manage.py shell"

# Create superuser
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"

# Run migrations
caprover apps:exec multivendor-backend --command "python manage.py migrate"

# List all users
caprover apps:exec multivendor-backend --command "python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.all())\""
```

### Database Commands
```powershell
# Access PostgreSQL shell
caprover apps:exec postgres-db --command "psql -U postgres -d multivendor_db"

# List databases
caprover apps:exec postgres-db --command "psql -U postgres -c '\l'"

# Backup database
caprover apps:exec postgres-db --command "pg_dump -U postgres multivendor_db" > backup-$(Get-Date -Format "yyyyMMdd-HHmmss").sql
```

---

## 🔄 Updating Your Application

### Update Backend Code
```powershell
cd C:\Users\F003\Desktop\damirco
git pull  # if using git
caprover deploy -a multivendor-backend
```

### Update Frontend Code
```powershell
caprover deploy -a multivendor-frontend
```

### After Code Updates
```powershell
# Run new migrations (if any)
caprover apps:exec multivendor-backend --command "python manage.py migrate"

# Collect static files (if CSS/JS changed)
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"

# Restart apps
caprover apps:restart multivendor-backend
caprover apps:restart multivendor-frontend
```

---

## 🎯 Quick Deployment Checklist

Use this checklist to verify your setup:

- [ ] PostgreSQL database created and running
- [ ] Backend environment variables configured
- [ ] Frontend environment variables configured
- [ ] Backend persistent directories set up
- [ ] Custom domains added for backend
- [ ] Custom domains added for frontend
- [ ] SSL certificates enabled
- [ ] Backend code deployed
- [ ] Frontend code deployed
- [ ] Django migrations run
- [ ] Superuser created
- [ ] Static files collected
- [ ] Frontend accessible at https://indexo.ir
- [ ] Backend API accessible at https://multivendor-backend.indexo.ir/api
- [ ] Admin panel accessible and working

---

## 📞 Need Help?

If you encounter issues:

1. **Check logs first:**
   ```powershell
   caprover apps:logs multivendor-backend
   caprover apps:logs multivendor-frontend
   caprover apps:logs postgres-db
   ```

2. **Verify environment variables** are set correctly in CapRover dashboard

3. **Check DNS records** point to your VPS IP

4. **Restart apps** if needed

5. **Check CapRover logs** in the dashboard under each app's "Logs" tab

---

## 🎉 Success Indicators

Your setup is successful when:

✅ Frontend loads at https://indexo.ir  
✅ No console errors in browser  
✅ Backend API responds at https://multivendor-backend.indexo.ir/api  
✅ Admin panel loads at https://multivendor-backend.indexo.ir/admin  
✅ You can login to admin panel  
✅ SSL certificates show as valid (green padlock)  
✅ All logs show no errors  

---

## 🔐 Security Reminders

After setup, consider:

1. **Change default passwords** (especially database password and SECRET_KEY)
2. **Enable firewall** on your VPS
3. **Set up automated backups** for database
4. **Keep CapRover updated**
5. **Monitor logs regularly**

---

**Your Configuration Summary:**

- **CapRover Dashboard**: https://captain.indexo.ir
- **Frontend**: https://indexo.ir
- **Backend API**: https://multivendor-backend.indexo.ir/api
- **Admin Panel**: https://multivendor-backend.indexo.ir/admin
- **Database Host**: srv-captain--postgres-db:5432
- **Database Name**: multivendor_db

**Ready to deploy? Follow the steps above in order!** 🚀



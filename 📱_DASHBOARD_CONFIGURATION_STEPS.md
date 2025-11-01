# 📱 CapRover Dashboard Configuration Guide

This guide shows you exactly what to click and configure in the CapRover dashboard.

---

## 🗄️ PART 1: Configure PostgreSQL Database

### Step 1: Access the postgres-db app
1. Open browser: `https://captain.indexo.ir`
2. Click **"Apps"** in the left sidebar
3. Find and click **"postgres-db"** in the apps list

### Step 2: Set Environment Variables
1. Click the **"App Configs"** tab at the top
2. Scroll down to **"Environmental Variables"** section
3. Click **"Bulk Edit"** button (easier than adding one by one)
4. Paste these lines:
```
POSTGRES_DB=multivendor_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^
```
5. Click **"Save & Update"** button at the bottom
6. Wait 30-60 seconds for the app to restart
7. Check if it's running: Click **"Logs"** tab, look for "database system is ready to accept connections"

✅ **postgres-db is now configured!**

---

## 🔧 PART 2: Configure Backend App

### Step 1: Access the multivendor-backend app
1. Click **"Apps"** in the left sidebar
2. Find and click **"multivendor-backend"**

### Step 2: Set Environment Variables
1. Click the **"App Configs"** tab
2. Scroll to **"Environmental Variables"** section
3. Click **"Bulk Edit"** button
4. Paste ALL these lines:
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
5. Click **"Save & Update"** button

### Step 3: Add Persistent Directories
1. Still in **"App Configs"** tab
2. Scroll to **"Persistent Directories"** section
3. For the first directory:
   - **Path in App**: `/app/staticfiles`
   - **Label** (optional): `staticfiles`
   - Click **"Add Persistent Directory"**
4. For the second directory:
   - **Path in App**: `/app/media`
   - **Label** (optional): `media`
   - Click **"Add Persistent Directory"**
5. Click **"Save & Update"**

### Step 4: Configure Domain and SSL
1. Click the **"HTTP Settings"** tab at the top
2. In the **"HTTP Settings"** section:
   - Check ✅ **"HTTPS"**
   - Check ✅ **"Force HTTPS"**
   - Check ✅ **"Websocket Support"** (optional)
3. Scroll to **"Custom Domains"** section
4. In the text box, type: `multivendor-backend.indexo.ir`
5. Click **"Connect New Domain"** button
6. After domain appears in the list, click **"Enable HTTPS"** next to it
7. Wait 5-10 minutes for SSL certificate (Let's Encrypt)
8. Refresh the page - you should see a green padlock next to the domain

✅ **multivendor-backend is now configured!**

---

## 🎨 PART 3: Configure Frontend App

### Step 1: Access the multivendor-frontend app
1. Click **"Apps"** in the left sidebar
2. Find and click **"multivendor-frontend"**

### Step 2: Set Environment Variables
1. Click the **"App Configs"** tab
2. Scroll to **"Environmental Variables"** section
3. Click **"Bulk Edit"** button
4. Paste these lines:
```
VITE_API_BASE_URL=https://multivendor-backend.indexo.ir
VITE_DJANGO_ADMIN_URL=https://multivendor-backend.indexo.ir/admin/
VUE_APP_TITLE=Multivendor Platform
VUE_APP_DESCRIPTION=Your Multivendor E-commerce Platform
```
5. Click **"Save & Update"** button

### Step 3: Configure Domain and SSL
1. Click the **"HTTP Settings"** tab at the top
2. In the **"HTTP Settings"** section:
   - Check ✅ **"HTTPS"**
   - Check ✅ **"Force HTTPS"**
3. Scroll to **"Custom Domains"** section
4. In the text box, type: `indexo.ir`
5. Click **"Connect New Domain"** button
6. (Optional) Add another domain: `www.indexo.ir` and click **"Connect New Domain"**
7. After domain appears, click **"Enable HTTPS"** next to it
8. Wait 5-10 minutes for SSL certificate
9. Refresh the page - you should see a green padlock

✅ **multivendor-frontend is now configured!**

---

## 🚀 PART 4: Deploy Your Code

### From Your Computer (PowerShell)

1. Open PowerShell
2. Navigate to your project:
```powershell
cd C:\Users\F003\Desktop\damirco
```

3. Login to CapRover (if not already):
```powershell
caprover login
```
Enter:
- **CapRover Machine**: `https://captain.indexo.ir`
- **Password**: [your password]

4. Deploy backend:
```powershell
caprover deploy -a multivendor-backend
```
Wait for: `✔ Deployed successfully!`

5. Deploy frontend:
```powershell
caprover deploy -a multivendor-frontend
```
Wait for: `✔ Deployed successfully!`

✅ **Code deployed!**

---

## 🔨 PART 5: Run Django Setup

### In PowerShell, run these commands:

1. **Run Migrations:**
```powershell
caprover apps:exec multivendor-backend --command "python manage.py migrate"
```
Wait for: `Applying migrations...` → `OK`

2. **Create Superuser:**
```powershell
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"
```
Follow prompts:
- Username: [your choice, e.g., admin]
- Email: [your email]
- Password: [your password]

3. **Collect Static Files:**
```powershell
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
```
Wait for: `X static files copied`

✅ **Django setup complete!**

---

## ✅ PART 6: Verify Everything Works

### Check Logs in Dashboard

1. **Backend Logs:**
   - Go to **Apps** → **multivendor-backend**
   - Click **"Logs"** tab
   - Look for:
     - ✅ `Database connection successful`
     - ✅ `Booting worker with pid`
     - ✅ No red errors

2. **Frontend Logs:**
   - Go to **Apps** → **multivendor-frontend**
   - Click **"Logs"** tab
   - Look for:
     - ✅ `start worker process`
     - ✅ No errors

3. **Database Logs:**
   - Go to **Apps** → **postgres-db**
   - Click **"Logs"** tab
   - Look for:
     - ✅ `database system is ready to accept connections`

### Test Your Apps

1. **Test Frontend:**
   - Open: `https://indexo.ir`
   - Should load your site
   - Check browser console (F12) - no errors

2. **Test Backend API:**
   - Open: `https://multivendor-backend.indexo.ir/api`
   - Should show API response

3. **Test Admin Panel:**
   - Open: `https://multivendor-backend.indexo.ir/admin`
   - Should show login page
   - Login with superuser credentials
   - Should see admin dashboard

✅ **Everything works!**

---

## 🎯 Visual Checklist

Use this to track your progress:

### Database Configuration
- [ ] postgres-db environment variables set
- [ ] postgres-db logs show "ready to accept connections"

### Backend Configuration
- [ ] multivendor-backend environment variables set (all 15 variables)
- [ ] Persistent directories added (/app/staticfiles, /app/media)
- [ ] Domain added: multivendor-backend.indexo.ir
- [ ] SSL enabled (green padlock)
- [ ] Backend code deployed
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Static files collected
- [ ] Backend logs show no errors

### Frontend Configuration
- [ ] multivendor-frontend environment variables set (all 4 variables)
- [ ] Domain added: indexo.ir
- [ ] SSL enabled (green padlock)
- [ ] Frontend code deployed
- [ ] Frontend logs show no errors

### Verification
- [ ] Frontend loads at https://indexo.ir
- [ ] Backend API responds at https://multivendor-backend.indexo.ir/api
- [ ] Admin panel accessible and working
- [ ] Can login to admin
- [ ] No console errors
- [ ] SSL certificates valid

---

## 🔧 Common Dashboard Issues

### Issue: Can't find environment variables section
**Solution:** Make sure you're in the **"App Configs"** tab, not "Deployment" or "HTTP Settings"

### Issue: "Bulk Edit" button not working
**Solution:** Try adding variables one by one using the "Key" and "Value" inputs instead

### Issue: Domain won't connect
**Solution:**
1. Make sure DNS records point to your VPS IP
2. Wait a few minutes and try again
3. Check if domain is typed correctly (no http://, no trailing slash)

### Issue: SSL certificate pending
**Solution:**
1. This is normal - wait 5-10 minutes
2. Refresh the page to check status
3. Make sure ports 80 and 443 are open on your VPS

### Issue: Can't deploy code
**Solution:**
1. Make sure you're in the project directory
2. Check if logged in: `caprover login`
3. Verify app names match exactly

---

## 📞 Need Help?

### View Logs in Real-Time
```powershell
caprover apps:logs multivendor-backend -f
```

### Restart an App
1. Go to the app in dashboard
2. Click **"App Configs"** tab
3. Scroll to bottom
4. Click **"Save & Update"** (this restarts the app)

Or use PowerShell:
```powershell
caprover apps:restart multivendor-backend
```

---

## 🎉 Success!

When everything is done, you should have:

✅ Three running apps in CapRover dashboard (all with green status)  
✅ SSL certificates enabled (green padlock on all domains)  
✅ Frontend loading at https://indexo.ir  
✅ Backend API responding at https://multivendor-backend.indexo.ir/api  
✅ Admin panel working at https://multivendor-backend.indexo.ir/admin  
✅ No errors in any logs  

**Your multivendor platform is now live!** 🚀

---

## 📚 Related Documents

- **Command Reference**: `⚡_QUICK_START_COMMANDS.txt`
- **Detailed Guide**: `🚀_CAPROVER_FRESH_SETUP_GUIDE.md`
- **Checklist**: `⚡_SETUP_CHECKLIST.md`
- **Environment Variables**: `caprover-env-backend.txt`, `caprover-env-frontend.txt`



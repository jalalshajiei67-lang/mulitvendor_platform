# 🔧 Troubleshooting "Nothing here yet :/" - CapRover Deployment

## Current Setup:
- ✅ `db` - PostgreSQL Database
- ✅ `back` - Django Backend  
- ✅ `front` - Vue.js Frontend
- ❌ Seeing "Nothing here yet :/" on domain

---

## Step 1: Check App Status

### For Each App (back, front):
1. Go to CapRover Dashboard
2. Click on the app name
3. Check the status at the top:
   - ✅ **Running** (Green) - Good!
   - ⚠️ **Building** (Yellow) - Wait for it to finish
   - ❌ **Error** (Red) - Need to check logs

**Action:** Note which apps are running vs. errored

---

## Step 2: Check Backend (Django) Logs

### View Logs:
1. Go to CapRover → Apps → **`back`**
2. Click **Deployment** tab → **View Logs**
3. Look for errors (usually in red)

### Common Issues & Solutions:

#### ❌ Issue: "no environment variable named DB_PASSWORD"
**Solution:** Environment variables not set!

Go to `back` app → **App Configs** → **Environment Variables**, add:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=captain-back--yourdomain.com,back.yourdomain.com,yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=srv-captain--db
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://captain-front--yourdomain.com
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True
```

**Important Notes:**
- Replace `your-secret-key-here` with a new secret (see below)
- Replace `your-database-password` with the password you set for the `db` app
- Replace `yourdomain.com` with your actual domain
- DB_HOST should be `srv-captain--db` (srv-captain--[your-db-app-name])

**Generate SECRET_KEY:**
```python
# Run in Python or online Python interpreter
import secrets
print(secrets.token_urlsafe(50))
```

#### ❌ Issue: "relation does not exist" or "no such table"
**Solution:** Migrations haven't run

The Dockerfile should run migrations automatically, but check logs. If needed, run manually:
1. Go to `back` app → **Deployment** → **View Logs** → **Web Terminal** tab
2. Run:
```bash
python manage.py migrate
```

#### ❌ Issue: "connection to server at 'srv-captain--db' failed"
**Solution:** Database app name is wrong

- Check your database app name (you said it's `db`)
- DB_HOST should be: `srv-captain--db`
- If your DB app has a different name, use: `srv-captain--[actual-name]`

---

## Step 3: Check Frontend (Vue.js) Logs

### View Logs:
1. Go to CapRover → Apps → **`front`**
2. Click **Deployment** tab → **View Logs**
3. Check build logs and runtime logs

### Common Issues & Solutions:

#### ❌ Issue: Build fails with "npm ERR!"
**Solution:** Check if package-lock.json is present in deploy-vue branch
- Should be present (we added it earlier)
- If still fails, check the specific npm error

#### ❌ Issue: Shows "Nothing here yet :/" but no errors
**Solution:** Environment variables not set!

Go to `front` app → **App Configs** → **Environment Variables**, add:

```env
VITE_API_BASE_URL=https://captain-back--yourdomain.com/api
VITE_DJANGO_ADMIN_URL=https://captain-back--yourdomain.com/admin/
```

**Important Notes:**
- Replace `yourdomain.com` with your actual domain
- Or use your backend's custom domain if you set one
- After adding env vars, click **Save & Update** then **Force Rebuild**

#### ⚠️ Issue: Frontend loads but can't connect to backend
**Solution:** CORS or wrong API URL
- Check browser console (F12) for errors
- Verify VITE_API_BASE_URL matches your backend URL
- Ensure backend CORS_ALLOWED_ORIGINS includes frontend URL

---

## Step 4: Configure Custom Domains (Optional but Recommended)

### Backend Domain:
1. Go to `back` app → **HTTP Settings**
2. Under **Custom Domain**, click **Connect New Domain**
3. Enter: `back.yourdomain.com` or `api.yourdomain.com`
4. Enable **HTTPS** checkbox
5. Click **Save**
6. Wait 1-2 minutes for SSL certificate

### Frontend Domain:
1. Go to `front` app → **HTTP Settings**
2. Under **Custom Domain**, click **Connect New Domain**
3. Enter: `yourdomain.com` or `www.yourdomain.com`
4. Enable **HTTPS** checkbox
5. Click **Save**
6. Wait 1-2 minutes for SSL certificate

### Update DNS (if using custom domains):
Add these DNS records at your domain provider:

**For backend (back.yourdomain.com):**
```
Type: A
Name: back
Value: [Your VPS IP]
TTL: 3600
```

**For frontend (yourdomain.com):**
```
Type: A
Name: @ (or www)
Value: [Your VPS IP]
TTL: 3600
```

---

## Step 5: Enable HTTPS

### For Both Apps (back & front):
1. Go to app → **HTTP Settings**
2. Enable: **✅ HTTPS**
3. Enable: **✅ Force HTTPS by redirecting all HTTP traffic to HTTPS**
4. Enable: **✅ Websocket Support** (optional, for real-time features)
5. Click **Save & Update**

---

## Step 6: Test Your Apps

### Test Backend:
1. **Default CapRover URL:**
   - Visit: `https://captain-back--yourdomain.com/admin/`
   - You should see Django admin login page ✅

2. **If you see 404 or error:**
   - Check environment variables are set
   - Check logs for errors
   - Verify app is running (green status)

### Test Frontend:
1. **Default CapRover URL:**
   - Visit: `https://captain-front--yourdomain.com`
   - You should see your Vue.js app ✅

2. **If you see "Nothing here yet :/":**
   - App might still be building (check status)
   - Check logs for build errors
   - Verify environment variables are set

### Test Database Connection:
1. Go to `back` app → **Deployment** → **View Logs** → **Web Terminal**
2. Run:
```bash
python manage.py dbshell
```
3. If it connects, type `\q` to quit - Database works! ✅

---

## Step 7: Create Django Superuser

After backend is running:
1. Go to `back` app → **Deployment** → **View Logs** → **Web Terminal**
2. Run:
```bash
python manage.py createsuperuser
```
3. Follow prompts to create admin account
4. Visit backend admin URL and try logging in

---

## Step 8: Verify Everything Works

### Checklist:
- [ ] Database app (`db`) is running
- [ ] Backend app (`back`) is running (green status)
- [ ] Frontend app (`front`) is running (green status)
- [ ] Can access backend admin: `https://captain-back--yourdomain.com/admin/`
- [ ] Can access backend API: `https://captain-back--yourdomain.com/api/`
- [ ] Can access frontend: `https://captain-front--yourdomain.com`
- [ ] Frontend can make API calls (check browser console F12)
- [ ] No CORS errors in browser console
- [ ] Can login to Django admin
- [ ] HTTPS is working (green lock icon)

---

## Quick Troubleshooting Commands

### In Backend Terminal:
```bash
# Check if Django is configured correctly
python manage.py check

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test database connection
python manage.py dbshell

# Collect static files
python manage.py collectstatic --noinput
```

---

## Common "Nothing here yet :/" Causes

| Cause | Solution |
|-------|----------|
| App still building | Wait for build to complete (yellow → green) |
| Environment variables missing | Add all required env vars, save, force rebuild |
| Build failed | Check logs for errors, fix code/config, rebuild |
| Wrong port in Dockerfile | Should be 80 (already fixed in our branches) |
| Domain not configured | Use CapRover default URL first |
| SSL certificate pending | Wait 1-2 minutes after enabling HTTPS |
| App crashed on startup | Check logs for Python/Node errors |

---

## What to Check Right Now:

### 1. **Backend Status:**
Go to `back` app → Check if status is **green (running)**

If NOT green:
- Click **View Logs** → Look for error messages
- Check if environment variables are set
- Try **Force Rebuild**

### 2. **Frontend Status:**
Go to `front` app → Check if status is **green (running)**

If NOT green:
- Click **View Logs** → Look for build errors
- Check if environment variables are set
- Try **Force Rebuild**

### 3. **Access the Apps:**
- Backend: `https://captain-back--[your-captain-domain]`
- Frontend: `https://captain-front--[your-captain-domain]`

Replace `[your-captain-domain]` with your actual CapRover domain.

---

## Need More Help?

**Provide me with:**
1. Status of `back` app (green/yellow/red)
2. Status of `front` app (green/yellow/red)
3. Any error messages from logs
4. Which URL you're trying to access
5. Screenshot of error if possible

I'll help you debug specifically! 🚀

---

**Next Steps:**
1. Check app statuses
2. Add environment variables if missing
3. Check logs for errors
4. Force rebuild if needed
5. Test the URLs
6. Report back what you see!


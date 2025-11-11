# 🚀 Quick Deploy Guide

## Status: ✅ READY TO DEPLOY

### What Was Fixed:
1. ✅ Updated CI/CD workflows for Nuxt 3 directory structure
2. ✅ Removed hardcoded secrets from tracked files
3. ✅ Added lint scripts to package.json
4. ✅ Created comprehensive deployment readiness report

---

## 📝 Step-by-Step Deployment

### 1. Commit and Push Changes (5 minutes)

```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform"

# Stage all changes
git add .

# Commit
git commit -m "chore: prepare project for production deployment

- Update CI workflows for Nuxt 3 directory structure
- Remove hardcoded secrets from env files
- Add lint scripts to package.json
- Add deployment readiness report
- Security improvements"

# Push to trigger deployment
git push origin main
```

### 2. Set GitHub Secrets (5 minutes)

Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`

Add these secrets:
```
CAPROVER_URL = https://captain.indexo.ir
CAPROVER_PASSWORD = <your-caprover-password>
CAPROVER_BACKEND_APP_NAME = multivendor-backend
CAPROVER_FRONTEND_APP_NAME = multivendor-frontend
```

### 3. Setup CapRover Apps (15 minutes)

#### Create PostgreSQL Database:
1. Go to https://captain.indexo.ir
2. Apps → One-Click Apps/Databases → PostgreSQL
3. App Name: `postgres-db`
4. Password: (generate strong password)
5. Click Deploy

#### Create Backend App:
1. Apps → Create New App
2. App Name: `multivendor-backend`
3. After creation:
   - Enable HTTPS
   - Add domain: `multivendor-backend.indexo.ir`
   - Add Persistent Volumes:
     - `/app/media` → label: `media-files`
     - `/app/staticfiles` → label: `static-files`
   - Add Environment Variables (see below)

#### Backend Environment Variables:
```bash
SECRET_KEY=<generate-with-python-command-below>
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir,185.208.172.76
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=<your-postgres-password>
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir,https://multivendor-backend.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CSRF_TRUSTED_ORIGINS=https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir
BASE_URL=https://multivendor-backend.indexo.ir
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
```

**Generate SECRET_KEY:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Create Frontend App:
1. Apps → Create New App
2. App Name: `multivendor-frontend`
3. After creation:
   - Enable HTTPS
   - Add domains: `indexo.ir` and `www.indexo.ir`
   - Add Environment Variable:
     ```
     NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
     ```

### 4. Deploy via Git Push (Automatic - 10 minutes)

After pushing to main, GitHub Actions will:
1. Run tests ✅
2. Build Docker images ✅
3. Deploy to CapRover ✅
4. Report status ✅

Monitor at: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

### 5. Post-Deployment Setup (5 minutes)

#### Create Superuser:
1. Go to CapRover → Apps → multivendor-backend → Logs
2. Click "Web Terminal"
3. Run:
```bash
python manage.py createsuperuser
```

#### Test the Application:
- Frontend: https://indexo.ir
- Backend API: https://multivendor-backend.indexo.ir/api/
- Admin Panel: https://multivendor-backend.indexo.ir/admin/

---

## 🔧 Troubleshooting

### Backend won't start:
1. Check logs in CapRover
2. Verify environment variables are set correctly
3. Check database connection (HOST should be `srv-captain--postgres-db`)

### Frontend shows API errors:
1. Check CORS settings in backend
2. Verify `NUXT_PUBLIC_API_BASE` is set correctly
3. Check backend is responding: `curl https://multivendor-backend.indexo.ir/api/`

### Static files not loading:
1. Check persistent volumes are mounted
2. Backend runs `collectstatic` automatically on startup
3. Check logs for collection errors

### Database connection failed:
1. Verify PostgreSQL app is running
2. Check DB_HOST is `srv-captain--postgres-db`
3. Verify credentials match PostgreSQL app settings

---

## 📊 Deployment Timeline

| Step | Time | Status |
|------|------|--------|
| Commit & Push | 5 min | ⏳ |
| Set GitHub Secrets | 5 min | ⏳ |
| Setup CapRover Apps | 15 min | ⏳ |
| Automatic Deployment | 10 min | ⏳ |
| Post-Deployment | 5 min | ⏳ |
| **TOTAL** | **40 min** | ⏳ |

---

## 📞 Support

If you encounter issues:
1. Check `DEPLOYMENT_READINESS_REPORT.md` for detailed information
2. Review CapRover logs for specific error messages
3. Verify all environment variables are set correctly
4. Check DNS settings for your domains

---

## ✅ Success Criteria

Your deployment is successful when:
- [ ] Frontend loads at https://indexo.ir
- [ ] Backend API responds at https://multivendor-backend.indexo.ir/api/
- [ ] Admin panel accessible at https://multivendor-backend.indexo.ir/admin/
- [ ] Product images display correctly
- [ ] Search functionality works
- [ ] Blog posts load
- [ ] RFQ form submits successfully

---

**Ready to deploy?** Start with step 1! 🚀


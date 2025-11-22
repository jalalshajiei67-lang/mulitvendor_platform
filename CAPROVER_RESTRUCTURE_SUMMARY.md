# CapRover Restructure Summary

## ✅ Changes Made

### 1. Updated Backend Dockerfile
**File**: `Dockerfile`

**Change**: Switched from Gunicorn to Daphne for WebSocket support
```dockerfile
# Before
CMD gunicorn multivendor_platform.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120

# After
CMD daphne -b 0.0.0.0 -p 8000 multivendor_platform.asgi:application
```

**Why**: Your chat system requires WebSocket support, which needs ASGI (Daphne), not WSGI (Gunicorn).

### 2. Created CapRover Definition Files
- ✅ `captain-definition` (root) - For backend deployment
- ✅ `multivendor_platform/front_end/nuxt/captain-definition` - For frontend deployment

### 3. Updated docker-compose.yml
- ✅ Added clear comment: "FOR LOCAL DEVELOPMENT ONLY"
- ✅ Kept all services for local testing
- ✅ Exposed ports for easier local development

### 4. Created GitHub Actions CI/CD
**File**: `.github/workflows/deploy-caprover.yml`

**Features**:
- Automatic deployment on push to `main`
- Sequential deployment (backend first, then frontend)
- Manual trigger option
- Requires GitHub secrets configuration

### 5. Created Documentation

| File | Purpose |
|------|---------|
| `CAPROVER_DEPLOYMENT.md` | Complete CapRover setup guide |
| `GITHUB_SECRETS_SETUP.md` | How to configure GitHub secrets |
| `LOCAL_VS_CAPROVER.md` | Differences between local and production |
| `QUICK_START.md` | Quick reference for both environments |
| `CAPROVER_RESTRUCTURE_SUMMARY.md` | This file |

## 📋 What You Need to Do

### A. CapRover Server Setup (One-Time)

1. **Create PostgreSQL Database App**
   ```
   Name: multivendor-db
   Type: One-Click App → PostgreSQL 15
   Password: <strong-password>
   ```

2. **Create Redis App**
   ```
   Name: multivendor-redis
   Type: One-Click App → Redis
   ```

3. **Create Backend App**
   ```
   Name: multivendor-backend
   Has Persistent Data: Yes
   Enable HTTPS: Yes
   ```

4. **Create Frontend App**
   ```
   Name: multivendor-frontend
   Has Persistent Data: No
   Enable HTTPS: Yes
   ```

### B. Configure Backend Environment Variables

In CapRover → Apps → multivendor-backend → App Configs:

```env
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<your-postgres-password>
DB_HOST=srv-captain--multivendor-db
DB_PORT=5432

# Redis
REDIS_HOST=srv-captain--multivendor-redis
REDIS_PORT=6379

# Security
ALLOWED_HOSTS=api.indexo.ir,indexo.ir,www.indexo.ir,multivendor-backend.indexo.ir
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CSRF_TRUSTED_ORIGINS=https://indexo.ir,https://www.indexo.ir,https://api.indexo.ir
```

### C. Configure Frontend Environment Variables

In CapRover → Apps → multivendor-frontend → App Configs:

```env
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://api.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://indexo.ir
```

### D. Configure GitHub Secrets

Go to GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
1. `CAPROVER_SERVER` = `https://captain.indexo.ir`
2. `CAPROVER_APP_BACKEND` = `multivendor-backend`
3. `CAPROVER_APP_FRONTEND` = `multivendor-frontend`
4. `CAPROVER_APP_TOKEN_BACKEND` = <get from CapRover app settings>
5. `CAPROVER_APP_TOKEN_FRONTEND` = <get from CapRover app settings>

### E. Deploy!

**Option 1: GitHub Actions (Recommended)**
```bash
git add .
git commit -m "Deploy to CapRover"
git push origin main
```
→ Automatic deployment via GitHub Actions

**Option 2: Manual CLI**
```bash
# Install CapRover CLI
npm install -g caprover

# Deploy backend
cd /path/to/project
caprover deploy -a multivendor-backend

# Deploy frontend
cd multivendor_platform/front_end/nuxt
caprover deploy -a multivendor-frontend
```

### F. Post-Deployment

1. **Create superuser**
   ```
   CapRover → multivendor-backend → Deployment → Execute Command
   python manage.py createsuperuser
   ```

2. **Configure domains**
   - Backend: `api.indexo.ir` or keep default subdomain
   - Frontend: `indexo.ir` and `www.indexo.ir`

3. **Test**
   - Visit https://indexo.ir
   - Test login
   - Test chat functionality
   - Access admin at https://api.indexo.ir/admin

## 🎯 Architecture Overview

### Before (Confused)
```
❌ docker-compose.yml for production?
❌ Gunicorn without WebSocket support
❌ Unclear deployment process
```

### After (Clear)
```
✅ Local Development:
   - docker-compose.yml
   - All services in containers
   - Hot reload enabled
   - Access: localhost

✅ CapRover Production:
   - Separate apps for each service
   - PostgreSQL: One-Click App
   - Redis: One-Click App
   - Backend: Daphne (ASGI) with WebSockets
   - Frontend: Nuxt SSR
   - CI/CD: GitHub Actions
   - Access: indexo.ir
```

## 🔄 Typical Workflow

```
1. Developer writes code locally
2. Tests with docker-compose up
3. Commits to Git
4. Pushes to main branch
5. GitHub Actions triggers
6. Deploys to CapRover automatically
7. CapRover manages SSL, domains, containers
8. Users access via https://indexo.ir
```

## ⚠️ Important Notes

1. **docker-compose.yml is ONLY for local development**
   - Don't use it on your VPS
   - CapRover manages containers differently

2. **Backend uses Daphne (not Gunicorn)**
   - Required for WebSocket chat
   - Configured in Dockerfile

3. **Separate apps in CapRover**
   - Backend and frontend are separate
   - Database and Redis are separate
   - All communicate via internal CapRover network

4. **Environment variables are different**
   - Local: Uses DB_HOST=db
   - CapRover: Uses DB_HOST=srv-captain--multivendor-db

5. **Secrets management**
   - Never commit secrets to Git
   - Use CapRover environment variables
   - Use GitHub secrets for CI/CD

## 📊 File Status

### Files to Keep
- ✅ `docker-compose.yml` - For local development
- ✅ `Dockerfile` - For backend (works for both)
- ✅ `multivendor_platform/front_end/nuxt/Dockerfile` - For frontend
- ✅ `captain-definition` - For CapRover backend
- ✅ `multivendor_platform/front_end/nuxt/captain-definition` - For CapRover frontend
- ✅ `.github/workflows/deploy-caprover.yml` - For CI/CD

### Files NOT Used in CapRover (but kept for reference)
- `captain-definition-backend` - Replaced by `captain-definition`
- `captain-definition-frontend` - Moved to nuxt directory
- `Dockerfile.backend` - Replaced by `Dockerfile`
- `Dockerfile.frontend.nuxt` - Replaced by nuxt/Dockerfile

## 🚀 Next Steps

1. ✅ Set up CapRover apps (PostgreSQL, Redis, Backend, Frontend)
2. ✅ Configure environment variables in CapRover
3. ✅ Add GitHub secrets
4. ✅ Push to GitHub main branch
5. ✅ Watch GitHub Actions deploy
6. ✅ Test on https://indexo.ir
7. ✅ Create superuser
8. ✅ Configure domains
9. ✅ Test chat functionality

## 📚 Additional Resources

- CapRover Documentation: https://caprover.com/docs/
- Django Channels: https://channels.readthedocs.io/
- Nuxt Deployment: https://nuxt.com/docs/getting-started/deployment
- GitHub Actions: https://docs.github.com/en/actions

## 🆘 Troubleshooting

See `QUICK_START.md` for common issues and solutions.

---

**Questions?** Check the documentation files or CapRover logs!



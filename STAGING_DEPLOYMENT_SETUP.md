# Staging Deployment Setup Guide

This guide explains how to set up automatic deployment to CapRover staging environment when pushing to the `staging` branch.

## 📋 Overview

When you push code to the `staging` branch, GitHub Actions will automatically:
1. Deploy the backend to CapRover staging
2. Deploy the frontend to CapRover staging (after backend succeeds)
3. Send a deployment summary

## 🔐 Required GitHub Secrets

Configure these secrets in **GitHub → Settings → Secrets and variables → Actions → New repository secret**:

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `CAPROVER_URL` | Your CapRover dashboard URL | `https://captain.indexo.ir` |
| `CAPROVER_PASSWORD` | Your CapRover dashboard password | `YourCapRoverPassword` |
| `CAPROVER_BACKEND_STAGING_APP_NAME` | Staging backend app name in CapRover | `multivendor-backend-staging` |
| `CAPROVER_FRONTEND_STAGING_APP_NAME` | Staging frontend app name in CapRover | `multivendor-frontend-staging` |

### How to Get CapRover Password:

1. If you remember your password, use it directly
2. If you forgot, you can reset it:
   - SSH into your VPS: `ssh root@185.208.172.76`
   - Run: `docker exec captain-captain.1.<container-id> cat /captain/data/config-captain.json | grep password`
   - Or reset via CapRover dashboard if you have access

## 🖥️ CapRover Setup

### 1. Create Staging Backend App in CapRover

1. Go to CapRover dashboard: `https://captain.indexo.ir`
2. Navigate to **Apps** → **Create New App**
3. App Name: `multivendor-backend-staging` (or match your `CAPROVER_BACKEND_STAGING_APP_NAME` secret)
4. Has Persistent Data: **Yes**
5. Enable HTTPS: **Yes**
6. Add custom domains: `staging-api.indexo.ir`, `staging-backend.indexo.ir`

### 2. Configure Backend Environment Variables

In CapRover → Apps → `multivendor-backend-staging` → **App Configs**, add these environment variables:

```env
# Django Configuration
DEBUG=True
SECRET_KEY=<generate-strong-secret-key>
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover

# Database Configuration - Staging PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<your-staging-postgres-password>
DB_HOST=srv-captain--postgres-db-staging
DB_PORT=5432

# Redis Configuration (for WebSocket/Chat) - Staging Redis
REDIS_HOST=srv-captain--multivendor-redis-staging
REDIS_PORT=6379
REDIS_PASSWORD=<your-staging-redis-password-if-set>

# Security Configuration
ALLOWED_HOSTS=staging-api.indexo.ir,staging-backend.indexo.ir,staging.indexo.ir
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir,https://staging-frontend.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True
CSRF_TRUSTED_ORIGINS=https://staging-api.indexo.ir,https://staging.indexo.ir

# Static Files Configuration
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media

# Site Configuration
USE_TLS=True
SITE_URL=https://staging.indexo.ir
```

**Note:** See `caprover-env-backend-staging.txt` for a complete template.

### 3. Create Staging Frontend App in CapRover

1. Go to CapRover dashboard: `https://captain.indexo.ir`
2. Navigate to **Apps** → **Create New App**
3. App Name: `multivendor-frontend-staging` (or match your `CAPROVER_FRONTEND_STAGING_APP_NAME` secret)
4. Has Persistent Data: **No**
5. Enable HTTPS: **Yes**
6. Add custom domain: `staging.indexo.ir`

### 4. Configure Frontend Environment Variables

In CapRover → Apps → `multivendor-frontend-staging` → **App Configs**, add these environment variables:

```env
# API Configuration (CRITICAL - must be set for API calls to work)
NUXT_PUBLIC_API_BASE=https://staging-api.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://staging.indexo.ir

# Django Admin URL (optional - for admin panel links)
NUXT_PUBLIC_DJANGO_ADMIN_URL=https://staging-api.indexo.ir/admin/

# App Configuration
NUXT_PUBLIC_APP_TITLE=Multivendor Platform (Staging)
NUXT_PUBLIC_APP_DESCRIPTION=Your Multivendor E-commerce Platform - Staging Environment

# Node.js Configuration
NODE_ENV=production
NUXT_HOST=0.0.0.0
NUXT_PORT=3000
```

**Note:** See `caprover-env-frontend-staging.txt` for a complete template.

**Important:** The staging Dockerfile (`Dockerfile.frontend.staging.nuxt`) is already configured with staging URLs, so these environment variables are mainly for runtime overrides.

## 🚀 Deployment Workflow

### Automatic Deployment

1. Make your changes on any branch
2. Merge or push to the `staging` branch:
   ```bash
   git checkout staging
   git merge main  # or your feature branch
   git push origin staging
   ```
3. GitHub Actions will automatically:
   - Deploy backend to staging
   - Deploy frontend to staging (after backend)
   - Show deployment summary

### Manual Deployment

You can also trigger deployment manually:
1. Go to GitHub → **Actions** tab
2. Select **Deploy Backend to Staging** or **Deploy Frontend to Staging**
3. Click **Run workflow** → Select `staging` branch → Click **Run workflow**

## 📊 Deployment URLs

After deployment, access your staging environment at:

- **Frontend:** https://staging.indexo.ir
- **Backend API:** https://staging-api.indexo.ir/api
- **Django Admin:** https://staging-api.indexo.ir/admin

## 🔍 Monitoring Deployments

1. Go to **GitHub → Actions** tab to see deployment status
2. Check CapRover dashboard for app logs and status
3. Deployment summary will show success/failure status

## ⚠️ Important Notes

1. **Staging vs Production:**
   - Staging uses `Dockerfile.frontend.staging.nuxt` with staging URLs baked in
   - Production uses `Dockerfile.frontend.nuxt` with production URLs
   - Backend uses the same `Dockerfile.backend` for both (configurable via env vars)

2. **Database & Redis:**
   - Staging should use separate databases and Redis instances
   - Update `DB_HOST` and `REDIS_HOST` in staging app configs

3. **Environment Variables:**
   - Staging frontend build uses staging URLs at build time (for SSR)
   - Runtime env vars in CapRover can override, but SSR needs build-time vars

4. **Workflow Dependencies:**
   - Frontend deployment waits for backend deployment to complete
   - If backend fails, frontend won't deploy

## 🐛 Troubleshooting

### Deployment Fails: "App not found"
- Verify app names in CapRover match GitHub secrets
- Check `CAPROVER_BACKEND_STAGING_APP_NAME` and `CAPROVER_FRONTEND_STAGING_APP_NAME`

### Frontend Build Fails: Wrong API URL
- Check that `Dockerfile.frontend.staging.nuxt` has correct staging URLs
- Verify CapRover app config has `NUXT_PUBLIC_API_BASE` set correctly

### Backend Deployment Fails: Database Connection
- Verify database service exists in CapRover
- Check `DB_HOST` matches the actual service name
- Ensure database credentials are correct

### Authentication Fails
- Verify `CAPROVER_URL` and `CAPROVER_PASSWORD` secrets are correct
- Test login to CapRover dashboard with these credentials

## 📝 Files Involved

- `.github/workflows/deploy-backend-staging.yml` - Backend staging deployment
- `.github/workflows/deploy-frontend-staging.yml` - Frontend staging deployment
- `.github/workflows/deployment-summary-staging.yml` - Deployment summary
- `Dockerfile.frontend.staging.nuxt` - Staging frontend Dockerfile
- `captain-definition-frontend-staging` - Staging frontend captain definition
- `caprover-env-backend-staging.txt` - Backend environment variables template
- `caprover-env-frontend-staging.txt` - Frontend environment variables template





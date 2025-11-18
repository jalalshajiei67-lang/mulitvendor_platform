# Environment Variables Guide

## Overview
This guide explains all environment variables needed for the Nuxt migration.

## Backend (Django) Variables

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
CORS_ALLOW_ALL_ORIGINS=False

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=your-secure-password-here
DB_HOST=db
DB_PORT=5432
```

## Frontend (Nuxt) Variables

### Local Development (Docker)
```bash
NUXT_PUBLIC_API_BASE=http://backend:8000/api
```

### Local Development (No Docker)
```bash
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api
```

### Production (CapRover)
```bash
NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
```

## CapRover Deployment

### Backend App Configuration
1. Go to CapRover dashboard
2. Navigate to your backend app
3. Add environment variables:
   - All Django variables listed above
   - Set `ALLOWED_HOSTS` to include your domain
   - Set `CORS_ALLOWED_ORIGINS` to include frontend URL

### Frontend App Configuration
1. Go to CapRover dashboard
2. Navigate to your frontend app
3. Add environment variable:
   ```
   NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
   ```

## Important Notes

1. **NUXT_PUBLIC_API_BASE** must be set at **build time** for production
2. The variable is embedded in the built JavaScript
3. For CapRover, set it in the app's environment variables before deployment
4. For Docker, pass it as build arg in docker-compose.yml (already configured)










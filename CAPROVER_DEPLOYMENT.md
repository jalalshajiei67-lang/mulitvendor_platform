# CapRover Deployment Guide

## Architecture

Your project will run as **3 separate CapRover apps**:

1. **backend** - Django API with WebSocket support (Daphne)
2. **frontend** - Nuxt 3 SSR
3. **PostgreSQL** - One-Click App
4. **Redis** - One-Click App

## Setup Steps

### 1. Create One-Click Apps in CapRover

#### PostgreSQL Database
1. Go to CapRover → Apps → One-Click Apps/Databases
2. Search for "PostgreSQL"
3. App Name: `multivendor-db`
4. PostgreSQL Version: `15`
5. PostgreSQL Password: (generate a strong password)
6. Click "Deploy"
7. Note the connection details:
   - Host: `srv-captain--multivendor-db`
   - Port: `5432`
   - Database: `postgres`
   - User: `postgres`

#### Redis
1. Go to One-Click Apps/Databases
2. Search for "Redis"
3. App Name: `multivendor-redis`
4. Click "Deploy"
5. Note the connection:
   - Host: `srv-captain--multivendor-redis`
   - Port: `6379`

### 2. Deploy Backend App

1. Create a new app: `multivendor-backend`
2. Enable HTTPS
3. Set Environment Variables:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   
   # Database
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your-postgres-password
   DB_HOST=srv-captain--multivendor-db
   DB_PORT=5432
   
   # Redis
   REDIS_HOST=srv-captain--multivendor-redis
   REDIS_PORT=6379
   
   # Allowed Hosts
   ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
   
   # CORS
   CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
   CORS_ALLOW_ALL_ORIGINS=False
   
   # CSRF
   CSRF_TRUSTED_ORIGINS=https://indexo.ir,https://www.indexo.ir,https://multivendor-backend.indexo.ir
   ```

4. Deploy from GitHub:
   - Method 1: Connect GitHub repo
   - Method 2: Use CLI: `caprover deploy`

### 3. Deploy Frontend App

1. Create a new app: `multivendor-frontend`
2. Enable HTTPS
3. Set Environment Variables:
   ```
   NODE_ENV=production
   NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
   NUXT_PUBLIC_SITE_URL=https://indexo.ir
   ```

4. Deploy from GitHub

### 4. Create Django Superuser

Connect to backend app terminal and run:
```bash
python manage.py createsuperuser
```

## File Structure for CapRover

```
/
├── captain-definition          # For backend deployment
├── Dockerfile.backend          # Backend Dockerfile with Daphne
├── multivendor_platform/
│   └── front_end/
│       └── nuxt/
│           ├── captain-definition  # For frontend deployment
│           └── Dockerfile         # Frontend Dockerfile
```

## GitHub Actions CI/CD

Deploy automatically on push to main branch. See `.github/workflows/deploy.yml`

## Useful Commands

### Deploy Backend
```bash
cd /path/to/project
caprover deploy -a multivendor-backend
```

### Deploy Frontend
```bash
cd /path/to/project/multivendor_platform/front_end/nuxt
caprover deploy -a multivendor-frontend
```

### View Logs
- CapRover Dashboard → Apps → Select App → App Logs

## Domain Setup

1. **Backend**: `multivendor-backend.indexo.ir` (or api.indexo.ir)
2. **Frontend**: `indexo.ir` and `www.indexo.ir`

Configure in CapRover → Apps → Select App → HTTP Settings → Add Domain

## Important Notes

- ✅ Docker Compose is **only for local development**
- ✅ CapRover manages PostgreSQL and Redis as separate apps
- ✅ Backend uses **Daphne** for WebSocket support (chat)
- ✅ Frontend is SSR with Nuxt 3
- ✅ Static/Media files are served by backend
- ✅ HTTPS is managed by CapRover automatically






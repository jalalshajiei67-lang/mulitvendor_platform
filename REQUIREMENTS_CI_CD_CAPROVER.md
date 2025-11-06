# Requirements for GitHub Actions CI/CD & CapRover Deployment

## 📋 Overview
This document outlines all requirements needed for GitHub Actions CI/CD pipeline and CapRover deployment on your VPS.

---

## 🔐 1. GitHub Repository Secrets

You need to configure the following secrets in your GitHub repository:

**Location:** `Settings → Secrets and variables → Actions → New repository secret`

### Required Secrets:

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `CAPROVER_URL` | Your CapRover instance URL | `https://captain.indexo.ir` |
| `CAPROVER_PASSWORD` | CapRover dashboard password | `YourCapRoverPassword` |
| `CAPROVER_BACKEND_APP_NAME` | Backend app name in CapRover | `multivendor-backend` |
| `CAPROVER_FRONTEND_APP_NAME` | Frontend app name in CapRover | `multivendor-frontend` |

### How to Get CapRover Password:
1. SSH into your VPS: `ssh root@185.208.172.76`
2. Run: `docker exec captain-captain.1.<container-id> cat /captain/data/config-captain.json | grep password`
3. Or check CapRover dashboard at first login

---

## 🖥️ 2. CapRover VPS Requirements

### 2.1 Server Specifications

**Minimum Requirements:**
- **RAM:** 2GB minimum (4GB recommended)
- **CPU:** 2 cores minimum
- **Storage:** 20GB minimum (50GB recommended for images/media)
- **OS:** Ubuntu 20.04+ / Debian 10+ / CentOS 7+

### 2.2 CapRover Installation

Ensure CapRover is installed and running on your VPS:
```bash
# Check if CapRover is running
docker ps | grep captain

# If not installed, install CapRover:
docker run -p 80:80 -p 443:443 -p 3000:3000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /captain:/captain caprover/caprover
```

### 2.3 Domain Configuration in CapRover

1. **Backend App:**
   - App Name: `multivendor-backend`
   - Domain: `multivendor-backend.indexo.ir`
   - Port: `80` (internal)

2. **Frontend App:**
   - App Name: `multivendor-frontend`
   - Domain: `indexo.ir` or `multivendor-frontend.indexo.ir`
   - Port: `80` (internal)

### 2.4 Environment Variables in CapRover Apps

#### Backend App Environment Variables:

```env
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover

# Database (if using external PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=srv-captain--postgres (or your DB host)
DB_PORT=5432

# Django
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir,185.208.172.76

# CORS
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
```

#### Frontend App Environment Variables:

```env
VITE_API_BASE_URL=https://multivendor-backend.indexo.ir/api
NODE_ENV=production
```

---

## 🗄️ 3. Database Requirements

### Option A: PostgreSQL in CapRover (Recommended)

1. **Install PostgreSQL One-Click App:**
   - Go to CapRover dashboard → Apps → One-Click Apps/Databases
   - Install PostgreSQL
   - Note the service name (usually `srv-captain--postgres`)

2. **Connection Details:**
   - Host: `srv-captain--postgres`
   - Port: `5432`
   - Database: Create database in CapRover or use default
   - User: `postgres` (default)
   - Password: Set during installation

### Option B: External PostgreSQL

Use the connection details from your external PostgreSQL service.

---

## 📦 4. Python Package Requirements

### For CI/CD (GitHub Actions):
Uses Python 3.11 as specified in `.github/workflows/ci.yml`

### For Production (CapRover):
Uses Python 3.11 as specified in `Dockerfile.backend`

**Required packages are in:**
- `requirements.txt` (root) - Used for deployment
- `multivendor_platform/requirements.txt` - Alternative requirements file

**Key packages:**
- Django 5.2.7
- djangorestframework 3.14.0
- psycopg2-binary 2.9.11
- gunicorn 23.0.0
- Pillow, lxml, beautifulsoup4, requests
- django-cors-headers, django-filter, django-tinymce

---

## 🐳 5. Docker Requirements

### Backend Dockerfile:
- Base Image: `python:3.11-slim`
- Port: `80`
- Build Context: `multivendor_platform/multivendor_platform/`

### Frontend Dockerfile:
- Build Stage: `node:20-alpine`
- Production Stage: `nginx:alpine`
- Port: `80`

### Required Files:
- ✅ `Dockerfile.backend`
- ✅ `Dockerfile.frontend`
- ✅ `captain-definition-backend`
- ✅ `captain-definition-frontend`

---

## 🔧 6. GitHub Actions Requirements

### 6.1 Workflow Files:
- ✅ `.github/workflows/ci.yml` - Continuous Integration
- ✅ `.github/workflows/deploy-caprover.yml` - Deployment

### 6.2 Actions Used:
- `actions/checkout@v4` - Code checkout
- `actions/setup-node@v4` - Node.js setup
- `actions/setup-python@v5` - Python setup
- `actions/cache@v4` - Dependency caching
- `actions/upload-artifact@v4` - Artifact upload

### 6.3 CI Requirements:
- **Backend Tests:** PostgreSQL 15 service
- **Frontend Build:** Node.js 20
- **Coverage:** Minimum 50% code coverage

### 6.4 Deployment Requirements:
- CapRover CLI: `npm install -g caprover`
- Tarball creation for backend and frontend
- Separate deployment jobs for backend and frontend

---

## 📁 7. Project Structure Requirements

### Required Files for Deployment:

```
multivendor_platform/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy-caprover.yml
├── multivendor_platform/
│   ├── multivendor_platform/
│   │   ├── settings_caprover.py  # ⚠️ REQUIRED
│   │   ├── wsgi.py
│   │   └── urls.py
│   └── requirements.txt
├── multivendor_platform/front_end/
│   ├── package.json
│   └── vite.config.js
├── Dockerfile.backend
├── Dockerfile.frontend
├── captain-definition-backend
├── captain-definition-frontend
├── requirements.txt
└── nginx/
    └── frontend.conf
```

### Critical Settings File:
- ✅ `settings_caprover.py` must exist and be properly configured
- ✅ Must use `DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover` in Dockerfile

---

## 🌐 8. Domain & DNS Requirements

### DNS Configuration:
- `indexo.ir` → Points to your VPS IP (185.208.172.76)
- `multivendor-backend.indexo.ir` → Points to your VPS IP
- `www.indexo.ir` → Points to your VPS IP (optional)

### SSL Certificates:
CapRover handles SSL automatically via Let's Encrypt. Ensure:
- DNS A records are properly configured
- Ports 80 and 443 are open on VPS
- CapRover SSL settings are enabled in dashboard

---

## ✅ 9. Pre-Deployment Checklist

### GitHub Repository:
- [ ] Secrets configured (CAPROVER_URL, CAPROVER_PASSWORD, APP_NAMES)
- [ ] Workflow files committed
- [ ] Main branch protected (optional but recommended)

### CapRover Dashboard:
- [ ] Backend app created: `multivendor-backend`
- [ ] Frontend app created: `multivendor-frontend`
- [ ] Domains configured for each app
- [ ] SSL enabled for domains
- [ ] Environment variables set (if not using secrets)
- [ ] PostgreSQL one-click app installed (if using)

### VPS Server:
- [ ] Docker and Docker Compose installed
- [ ] CapRover running and accessible
- [ ] Ports 80, 443, 3000 open in firewall
- [ ] Sufficient disk space (check with `df -h`)

### Project Files:
- [ ] `settings_caprover.py` exists and configured
- [ ] Dockerfiles are correct and tested
- [ ] `captain-definition` files are correct
- [ ] Requirements files are up to date

---

## 🚀 10. Deployment Flow

1. **Developer pushes to `main` branch**
2. **GitHub Actions CI runs:**
   - Backend tests with PostgreSQL
   - Frontend linting and build
3. **GitHub Actions Deploy runs:**
   - Creates backend tarball
   - Deploys backend to CapRover
   - Creates frontend tarball
   - Deploys frontend to CapRover
4. **CapRover:**
   - Builds Docker images
   - Runs migrations automatically (via Dockerfile CMD)
   - Collects static files
   - Restarts containers

---

## 🔍 11. Monitoring & Debugging

### Check Deployment Status:
```bash
# Via CapRover Dashboard
- Go to Apps → multivendor-backend → App Logs
- Go to Apps → multivendor-frontend → App Logs

# Via SSH
ssh root@185.208.172.76
docker logs srv-captain--<app-name>.<container-id>
```

### Common Issues:
1. **Build failures:** Check Dockerfile and requirements
2. **Database connection:** Verify environment variables
3. **Static files 404:** Ensure `collectstatic` runs in Dockerfile CMD
4. **CORS errors:** Check `CORS_ALLOWED_ORIGINS` in settings

---

## 📝 12. Additional Notes

### Python Version Compatibility:
- Your local: Python 3.14 (newer)
- CI/CD: Python 3.11 (as per workflow)
- Production: Python 3.11 (as per Dockerfile)

**Note:** Some packages (Pillow, lxml) were upgraded locally for Python 3.14 compatibility. Production uses Python 3.11, so pinned versions should work fine.

### Updating Requirements:
If you update Python packages locally, ensure:
1. Update `requirements.txt` with compatible versions
2. Test with Python 3.11 (production version)
3. Commit and push to trigger deployment

---

## 🆘 Quick Reference

### Test Deployment Locally First:
```bash
# Build backend image
docker build -f Dockerfile.backend -t multivendor-backend:test .

# Build frontend image
docker build -f Dockerfile.frontend -t multivendor-frontend:test .
```

### Manual Deployment (if needed):
```bash
# Install CapRover CLI
npm install -g caprover

# Deploy backend
caprover deploy \
  --caproverUrl "https://captain.indexo.ir" \
  --caproverPassword "your-password" \
  --appName "multivendor-backend" \
  --tarFile backend-deploy.tar.gz
```

---

**Last Updated:** 2025-01-27
**Maintained by:** Development Team










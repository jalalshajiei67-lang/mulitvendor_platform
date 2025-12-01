# 🚀 Deployment Structure Summary

## Overview
This is a **Django REST API + Nuxt.js** multivendor e-commerce platform deployed using **Docker Compose** with **Traefik** as reverse proxy.

---

## 📁 Project Structure

```
mulitvendor_platform/
├── 📦 Docker Configuration
│   ├── docker-compose.yml          # Main production compose file
│   ├── docker-compose.local.yml    # Local development compose
│   ├── Dockerfile                  # Backend Dockerfile (Django)
│   ├── Dockerfile.local            # Local dev backend Dockerfile
│   ├── Dockerfile.nginx-static     # Nginx static files server
│   └── deploy.sh                   # Main deployment script
│
├── 🔧 GitHub Actions (CI/CD)
│   └── .github/workflows/
│       ├── docker-deploy.yml       # Main deployment workflow
│       ├── ci.yml                  # CI pipeline (tests & linting)
│       └── test.yml                # Test workflow
│
├── 🎯 Backend (Django)
│   └── multivendor_platform/multivendor_platform/
│       ├── manage.py
│       ├── multivendor_platform/
│       │   ├── settings.py         # Django settings
│       │   ├── asgi.py             # ASGI config (Daphne)
│       │   ├── urls.py             # Main URL routing
│       │   └── wsgi.py
│       ├── products/               # Products app
│       ├── users/                  # User management
│       ├── orders/                 # Order management
│       ├── chat/                   # Chat/WebSocket
│       ├── blog/                   # Blog functionality
│       ├── pages/                  # Static pages
│       └── gamification/           # Gamification features
│
├── 🎨 Frontend (Nuxt.js)
│   └── multivendor_platform/front_end/nuxt/
│       ├── Dockerfile              # Frontend Dockerfile
│       ├── nuxt.config.ts          # Nuxt configuration
│       ├── package.json
│       ├── pages/                  # Vue pages (routing)
│       ├── components/             # Vue components
│       ├── composables/            # Composables (Vue 3)
│       ├── stores/                 # Pinia stores
│       ├── layouts/                # Layout components
│       ├── middleware/             # Route middleware
│       └── server/                 # Server-side code
│
├── 🌐 Reverse Proxy & Static Files
│   └── nginx/
│       ├── nginx.conf              # Nginx configuration
│       └── static-server.conf      # Static files serving
│
└── 📄 Configuration Files
    ├── requirements.txt            # Python dependencies
    └── env.template                # Environment variables template
```

---

## 🐳 Docker Services Architecture

### Services in `docker-compose.yml`:

1. **PostgreSQL Database** (`db`)
   - Image: `postgres:15-alpine`
   - Port: `5432`
   - Volume: `postgres_data`
   - Health check: `pg_isready`

2. **Redis** (`redis`)
   - Image: `redis:7-alpine`
   - Port: `6379`
   - Volume: `redis_data`
   - Health check: `redis-cli ping`

3. **Django Backend** (`backend`)
   - Build: `./Dockerfile`
   - Port: `8000`
   - Command: `daphne` (ASGI server)
   - Volumes:
     - Code: `./multivendor_platform/multivendor_platform:/app`
     - Media: `media_files:/app/media`
     - Static: `static_files:/app/static`
   - Depends on: `db`, `redis`

4. **Nuxt Frontend** (`frontend`)
   - Build: `./multivendor_platform/front_end/nuxt/Dockerfile`
   - Port: `3000`
   - Environment: `NUXT_PUBLIC_API_BASE=http://backend:8000/api`
   - Depends on: `backend`

5. **Traefik Reverse Proxy** (`traefik`)
   - Image: `traefik:v2.10`
   - Ports: `80`, `443`, `8080` (dashboard)
   - SSL: Let's Encrypt certificates
   - Routes:
     - `indexo.ir` / `www.indexo.ir` → Frontend (port 3000)
     - `api.indexo.ir` → Static/Media files via Nginx

6. **Nginx Static Server** (`nginx`)
   - Image: `nginx:alpine`
   - Serves: Static files and media files
   - Volumes: `static_files`, `media_files`
   - Route: `api.indexo.ir/static`, `api.indexo.ir/media`

---

## 🔄 Deployment Flow

### 1. **GitHub Actions Workflow** (`.github/workflows/docker-deploy.yml`)

```yaml
Trigger: Push to main branch OR manual dispatch
Steps:
  1. Checkout code
  2. SSH to VPS (using secrets: VPS_HOST, VPS_USER, VPS_SSH_KEY)
  3. Navigate to: /home/{user}/docker-deploy
  4. Pull latest code: git reset --hard origin/main
  5. Execute: bash deploy.sh
```

### 2. **Deployment Script** (`deploy.sh`)

```bash
Steps:
  1. Build Docker images: docker compose build
  2. Start services: docker compose up -d --remove-orphans
  3. Wait for database health check
  4. Run migrations: python manage.py migrate
  5. Collect static files: python manage.py collectstatic
  6. Verify backend health
  7. Clean up unused images: docker image prune -f
```

### 3. **Build Process**

**Backend Build** (`Dockerfile`):
- Base: `python:3.11-slim`
- Install: PostgreSQL client, build tools, Python dependencies
- Copy: Django project code
- Run as: Non-root user (`appuser`)
- Command: `daphne -b 0.0.0.0 -p 8000 multivendor_platform.asgi:application`

**Frontend Build** (`multivendor_platform/front_end/nuxt/Dockerfile`):
- Multi-stage build:
  - **Build stage**: Install dependencies, build Nuxt app
  - **Production stage**: Copy built `.output`, install production deps only
- Command: `node .output/server/index.mjs`
- Health check: `curl http://localhost:3000/`

---

## 🌐 Network & Routing

### Internal Network
- **Network**: `multivendor_network` (bridge)
- **Services communicate via service names**:
  - Frontend → Backend: `http://backend:8000/api`
  - Backend → Database: `db:5432`
  - Backend → Redis: `redis:6379`

### External Access (via Traefik)
- **HTTP (80)**: Redirects to HTTPS
- **HTTPS (443)**: Main entry point
- **Traefik Dashboard (8080)**: Monitoring (insecure, should be secured)

### Domain Routing
- `indexo.ir` / `www.indexo.ir` → Frontend (port 3000)
- `api.indexo.ir/static/*` → Nginx (static files)
- `api.indexo.ir/media/*` → Nginx (media files)

---

## 📦 Volumes & Data Persistence

### Named Volumes:
1. **postgres_data**: Database data
2. **redis_data**: Redis persistence
3. **media_files**: User-uploaded media (images, files)
4. **static_files**: Collected static files (CSS, JS, images)

### Bind Mounts:
- Backend code: `./multivendor_platform/multivendor_platform:/app` (for development)

---

## 🔐 Environment Variables

### Required Secrets (GitHub Actions):
- `VPS_HOST`: VPS IP address
- `VPS_USER`: SSH username
- `VPS_SSH_KEY`: SSH private key

### Backend Environment Variables:
- `DEBUG`: `False` (production)
- `SECRET_KEY`: Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database credentials
- `DB_HOST`: `db` (service name)
- `DB_PORT`: `5432`
- `REDIS_HOST`: `redis`
- `REDIS_PORT`: `6379`
- `ALLOWED_HOSTS`: Domain names
- `CORS_ALLOW_ALL_ORIGINS`: `True` (or specific origins)

### Frontend Environment Variables:
- `NODE_ENV`: `production`
- `NUXT_PUBLIC_API_BASE`: `http://backend:8000/api`
- `NUXT_HOST`: `0.0.0.0`
- `NUXT_PORT`: `3000`

---

## 🚀 Deployment Commands

### Manual Deployment (on VPS):
```bash
cd /home/{user}/docker-deploy
git pull origin main
bash deploy.sh
```

### Local Development:
```bash
docker compose -f docker-compose.local.yml up --build
```

### Useful Commands:
```bash
# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart service
docker compose restart backend

# Run migrations manually
docker exec multivendor_backend python manage.py migrate

# Create superuser
docker exec -it multivendor_backend python manage.py createsuperuser

# Access database
docker exec -it multivendor_db psql -U postgres -d multivendor_db

# Stop all services
docker compose down

# Stop and remove volumes (⚠️ deletes data)
docker compose down -v
```

---

## 🔍 Health Checks

### Service Health Checks:
- **Database**: `pg_isready` (every 10s)
- **Redis**: `redis-cli ping` (every 10s)
- **Frontend**: `curl http://localhost:3000/` (every 30s)

### Deployment Verification:
1. Check all containers are running: `docker compose ps`
2. Check backend health: `curl http://localhost:8000/api/`
3. Check frontend: `curl http://localhost:3000/`
4. Check Traefik dashboard: `http://{VPS_IP}:8080`

---

## 📝 Key Files Reference

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Main production orchestration |
| `deploy.sh` | Deployment automation script |
| `Dockerfile` | Backend container definition |
| `multivendor_platform/front_end/nuxt/Dockerfile` | Frontend container definition |
| `.github/workflows/docker-deploy.yml` | CI/CD pipeline |
| `nginx/nginx.conf` | Static files server config |
| `requirements.txt` | Python dependencies |
| `multivendor_platform/multivendor_platform/settings.py` | Django settings |

---

## ⚠️ Important Notes

1. **SSL Certificates**: Managed by Traefik via Let's Encrypt
   - Storage: `./letsencrypt/acme.json`
   - Email: `jalal.shajiei67@gmail.com`

2. **Static Files**: Collected during deployment, served by Nginx

3. **Media Files**: Stored in `media_files` volume, served by Nginx

4. **Database Migrations**: Run automatically during deployment

5. **Code Updates**: Code is bind-mounted for development, but in production should be copied into image

6. **Traefik Dashboard**: Currently insecure (port 8080), should be secured in production

---

## 🎯 Deployment Checklist

- [ ] VPS has Docker and Docker Compose installed
- [ ] GitHub secrets configured (VPS_HOST, VPS_USER, VPS_SSH_KEY)
- [ ] Domain DNS points to VPS IP
- [ ] Ports 80, 443, 8080 are open in firewall
- [ ] Environment variables set (or use defaults in docker-compose.yml)
- [ ] SSL certificates will be auto-generated by Traefik
- [ ] Database credentials configured
- [ ] Superuser created for Django admin

---

## 📞 Troubleshooting

### Backend not starting:
```bash
docker compose logs backend
docker exec multivendor_backend python manage.py check
```

### Frontend build fails:
```bash
docker compose logs frontend
docker compose build --no-cache frontend
```

### Database connection issues:
```bash
docker compose logs db
docker exec -it multivendor_db psql -U postgres -d multivendor_db
```

### Traefik routing issues:
- Check Traefik dashboard: `http://{VPS_IP}:8080`
- Verify container labels in `docker-compose.yml`
- Check SSL certificate generation in `./letsencrypt/`

---

**Last Updated**: After CapRover migration cleanup
**Deployment Method**: Pure Docker with Traefik reverse proxy


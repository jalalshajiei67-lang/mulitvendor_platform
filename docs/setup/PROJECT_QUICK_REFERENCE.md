# 🚀 Project Quick Reference Card

**One-Page Cheat Sheet for Multivendor Platform**

---

## 📦 Tech Stack
```
Backend:  Django 4.2 + DRF + PostgreSQL 15
Frontend: Vue.js 3.5 + Vuetify 3.10 + Vite 7
DevOps:   Docker + Nginx + Certbot
Deploy:   CapRover / VPS (158.255.74.123)
```

---

## 🎯 Quick Start Commands

### Local Development (Docker)
```bash
# Start
docker-compose -f docker-compose.local.yml up --build

# Access
Frontend: http://localhost:8080
Backend:  http://localhost:8000
Admin:    http://localhost:8000/admin

# Stop
docker-compose -f docker-compose.local.yml down
```

### Local Development (No Docker)
```bash
# Backend
cd multivendor_platform/multivendor_platform
python manage.py runserver

# Frontend (new terminal)
cd multivendor_platform/front_end
npm run dev
```

### Production Deployment
```bash
# Option 1: One Command (Linux/Mac)
./deploy-one-command.sh

# Option 2: Windows
deploy-windows.bat

# Option 3: Manual
docker-compose up -d --build
```

---

## 📁 Key File Locations

```
Settings:       multivendor_platform/multivendor_platform/multivendor_platform/settings.py
API Config:     multivendor_platform/front_end/src/services/api.js
Nginx:          nginx/conf.d/default.conf
Docker:         docker-compose.yml (prod), docker-compose.local.yml (dev)
Environment:    .env (create from .env.production)
```

---

## 🔑 Environment Variables

```env
SECRET_KEY=<generate-random-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=<secure-password>
DB_HOST=db
DB_PORT=5432

CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-domain.com
```

---

## 🌐 API Endpoints

### Products
```
GET    /api/products/              List products
GET    /api/products/{id}/         Product detail
POST   /api/products/              Create (auth required)
GET    /api/products/my_products/  My products (seller)
```

### Auth
```
POST   /api/auth/login/            Login
POST   /api/auth/register/         Register
GET    /api/auth/me/               Current user
```

### Blog
```
GET    /api/blog/posts/            List posts
GET    /api/blog/posts/{slug}/     Post detail
GET    /api/blog/categories/       Blog categories
```

### Admin
```
/admin/                            Django admin panel
```

---

## 🐳 Docker Commands

```bash
# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Restart specific service
docker-compose restart backend

# Execute commands
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --noinput

# Database access
docker-compose exec db psql -U postgres -d multivendor_db

# Clean up
docker-compose down -v  # Remove volumes
docker system prune -a  # Clean everything
```

---

## 🛠️ Django Management Commands

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# User management
python manage.py createsuperuser
python manage.py changepassword <username>

# Static files
python manage.py collectstatic --noinput

# Database
python manage.py dbshell
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json

# Dev server
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
```

---

## 📱 Frontend Commands

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Linting
npm run lint
```

---

## 🔍 Troubleshooting Quick Fixes

### Frontend Can't Connect to Backend
```bash
# Check API URL in frontend
cat multivendor_platform/front_end/src/services/api.js

# Check CORS settings
docker-compose exec backend python manage.py shell
>>> from django.conf import settings
>>> print(settings.CORS_ALLOWED_ORIGINS)
```

### Database Connection Issues
```bash
# Check database is running
docker-compose ps

# Check connection
docker-compose exec db pg_isready -U postgres

# Reset database
docker-compose down -v
docker-compose up -d
docker-compose exec backend python manage.py migrate
```

### Static Files Not Loading
```bash
# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Check Nginx config
docker-compose exec nginx nginx -t
docker-compose restart nginx
```

### Container Won't Start
```bash
# Check logs
docker-compose logs <service-name>

# Rebuild
docker-compose down
docker-compose up -d --build --force-recreate
```

---

## 📊 Service Ports

```
Service          Port    Access
─────────────────────────────────────
Frontend         8080    http://localhost:8080
Backend          8000    http://localhost:8000
PostgreSQL       5432    localhost:5432
Nginx (prod)     80      http://localhost
Nginx SSL        443     https://localhost
```

---

## 🎯 User Roles & Permissions

```
Role            Capabilities
───────────────────────────────────────────────
Buyer           Browse, purchase, review
Seller/Vendor   Manage products, view orders, ads
Admin           Full access, user management
Anonymous       Browse public content
```

---

## 📝 File Upload Paths

```
Media Files:     /media/
  Products:      /media/product_images/
  Blog:          /media/blog_images/
  Categories:    /media/category_images/
  Vendor Logos:  /media/vendor_logos/

Static Files:    /static/
```

---

## 🔗 Important URLs

### Local Development
```
Frontend:   http://localhost:8080
Backend:    http://localhost:8000
API:        http://localhost:8000/api/
Admin:      http://localhost:8000/admin/
```

### Production (VPS)
```
Frontend:   http://158.255.74.123
Backend:    http://158.255.74.123/api/
Admin:      http://158.255.74.123/admin/
```

---

## 📚 Documentation Files

```
START HERE:     🚀_START_HERE_FIRST.txt
Quick Start:    QUICK_START.md
Full Guide:     DEPLOYMENT_GUIDE.md
Local Test:     TESTING_GUIDE.md
CapRover:       CAPROVER_DEPLOYMENT_GUIDE.md
Troubleshoot:   TROUBLESHOOTING_DEPLOYMENT.md
Project State:  PROJECT_CURRENT_STATE.md
```

---

## 🔐 Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set strong DB_PASSWORD
- [ ] Configure CORS properly
- [ ] Enable SSL/HTTPS
- [ ] Set up firewall (UFW)
- [ ] Regular backups
- [ ] Update dependencies regularly

---

## 🚨 Emergency Commands

```bash
# Quick restart everything
docker-compose restart

# Nuclear option (rebuild everything)
docker-compose down -v
docker-compose up -d --build --force-recreate

# Backup database NOW
docker-compose exec db pg_dump -U postgres multivendor_db > emergency_backup.sql

# Restore from backup
cat emergency_backup.sql | docker-compose exec -T db psql -U postgres multivendor_db

# Check what's eating resources
docker stats

# View all container logs
docker-compose logs --tail=100
```

---

## 📞 Get Help

```
Documentation:  See /docs in project root
Logs:           docker-compose logs -f
Health Check:   ./health-check.sh
Status:         docker-compose ps
```

---

**Last Updated**: October 27, 2025  
**Keep this handy for daily development!** 📌


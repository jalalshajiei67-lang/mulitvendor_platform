# 🎯 Deployment Action Plan

**Step-by-Step Plan to Deploy Multivendor Platform to Production**

---

## 📋 Pre-Deployment Checklist

### Phase 1: Code Cleanup & Git Management

#### Step 1.1: Review Current Changes
```bash
# See what has changed
git status
git diff

# Review modified files
git diff Dockerfile
git diff docker-compose.yml
git diff multivendor_platform/front_end/src/services/api.js
git diff multivendor_platform/front_end/vite.config.js
git diff multivendor_platform/multivendor_platform/multivendor_platform/settings.py
```

#### Step 1.2: Handle Deleted Documentation Files
```bash
# Confirm deletions (these are old/redundant docs)
git rm multivendor_platform/ADMIN_REDIRECT_GUIDE.md
git rm multivendor_platform/APPLY_CHANGES_NOW.md
git rm multivendor_platform/BATCH_REPORTING_SYSTEM.md
git rm multivendor_platform/BATCH_SCRAPER_UI_GUIDE.md
git rm multivendor_platform/HOW_TO_VIEW_ERRORS.md
git rm multivendor_platform/HTML_VALIDATION_SYSTEM.md
git rm multivendor_platform/MIGRATION_INSTRUCTIONS.md
git rm multivendor_platform/PRODUCT_SCRAPER_GUIDE.md
git rm multivendor_platform/README_SCRAPER.md
git rm multivendor_platform/RESTART_SERVER.md
git rm multivendor_platform/ROBUST_ERROR_HANDLING_SYSTEM.md
git rm multivendor_platform/SCRAPER_COMPLETE_SYSTEM.md
git rm multivendor_platform/SCRAPER_QUICK_START.md
git rm multivendor_platform/SCRAPER_READY_TO_USE.md
git rm multivendor_platform/SCRAPER_TROUBLESHOOTING.md
git rm multivendor_platform/SITEMAP_GUIDE.md
git rm multivendor_platform/SITEMAP_QUICKSTART.md
git rm multivendor_platform/SLUG_GENERATION_INFO.md
```

#### Step 1.3: Add New Files
```bash
# Add new documentation and config files
git add PROJECT_CURRENT_STATE.md
git add PROJECT_QUICK_REFERENCE.md
git add DEPLOYMENT_ACTION_PLAN.md
git add docker-compose.local.yml
git add Dockerfile.backend
git add Dockerfile.frontend
git add multivendor_platform/multivendor_platform/multivendor_platform/settings_caprover.py
git add test-local.bat
git add test-local-background.bat
git add view-logs.bat
git add stop-local.bat

# Add CapRover configs
git add captain-definition-backend
git add captain-definition-frontend
git add caprover-env-backend.txt
git add caprover-env-frontend.txt

# Add guides
git add TESTING_GUIDE.md
git add LOCAL_DOCKER_SETUP_SUMMARY.md
git add CAPROVER_DEPLOYMENT_GUIDE.md
```

#### Step 1.4: Stage Modified Files
```bash
# Add modified files
git add Dockerfile
git add docker-compose.yml
git add nginx/conf.d/default.conf
git add requirements.txt
git add multivendor_platform/requirements.txt
git add multivendor_platform/front_end/src/services/api.js
git add multivendor_platform/front_end/vite.config.js
git add multivendor_platform/multivendor_platform/multivendor_platform/settings.py
git add multivendor_platform/multivendor_platform/products/migrations/0010_add_product_image_model.py
git add multivendor_platform/multivendor_platform/products/migrations/0017_alter_product_options_product_canonical_url_and_more.py
```

#### Step 1.5: Commit Changes
```bash
git commit -m "Prepare for production deployment

- Update Docker configurations for production and local testing
- Add CapRover deployment configurations
- Update API service with environment-based URLs
- Configure Vite for production builds
- Add comprehensive project documentation
- Add testing scripts for Windows
- Update nginx configuration for proper routing
- Clean up redundant documentation files
- Add migration files for SEO fields and product images"

git push origin main
```

**Estimated Time**: 15 minutes

---

## 🧪 Phase 2: Local Testing (CRITICAL - DO NOT SKIP)

### Step 2.1: Test Local Docker Environment
```bash
# Clean any existing containers
docker-compose -f docker-compose.local.yml down -v

# Start fresh
docker-compose -f docker-compose.local.yml up --build

# Wait for all services to be healthy (2-3 minutes)
```

### Step 2.2: Verify Services
```bash
# In a new terminal
# Check all containers are running
docker-compose -f docker-compose.local.yml ps

# Expected output:
# backend   - Up (healthy)
# frontend  - Up (healthy)
# db        - Up (healthy)
```

### Step 2.3: Test Endpoints
```bash
# Test backend API
curl http://localhost:8000/api/

# Test frontend
curl http://localhost:8080/

# Test admin panel
curl http://localhost:8000/admin/
```

### Step 2.4: Browser Testing
- [ ] Open http://localhost:8080
- [ ] Navigate through pages
- [ ] Check browser console for errors
- [ ] Test product listing
- [ ] Test blog pages

### Step 2.5: Create Test Superuser
```bash
docker-compose -f docker-compose.local.yml exec backend python manage.py createsuperuser

# Create user:
# Username: admin
# Email: admin@example.com
# Password: <strong-password>
```

### Step 2.6: Test Admin Panel
- [ ] Login to http://localhost:8000/admin/
- [ ] Create test product
- [ ] Upload product image
- [ ] Verify image displays

### Step 2.7: Stop Local Environment
```bash
docker-compose -f docker-compose.local.yml down
# Keep volumes for now: docker-compose -f docker-compose.local.yml down -v
```

**Estimated Time**: 30 minutes

---

## 🚀 Phase 3: Choose Deployment Method

### Option A: CapRover Deployment (RECOMMENDED)

#### Step 3A.1: Install CapRover CLI
```bash
npm install -g caprover
```

#### Step 3A.2: Login to CapRover
```bash
caprover login
# Enter your CapRover URL and password
```

#### Step 3A.3: Create Backend App
```bash
# On CapRover dashboard:
# 1. Create new app: "multivendor-backend"
# 2. Enable HTTPS
# 3. Set environment variables from caprover-env-backend.txt
```

**Backend Environment Variables**:
```env
SECRET_KEY=<generate-with-openssl-rand-base64-32>
DEBUG=False
ALLOWED_HOSTS=multivendor-backend.your-caprover-domain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=<strong-password>
DB_HOST=srv-captain--postgres
DB_PORT=5432
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://multivendor-frontend.your-caprover-domain.com
```

#### Step 3A.4: Create Frontend App
```bash
# On CapRover dashboard:
# 1. Create new app: "multivendor-frontend"
# 2. Enable HTTPS
# 3. Set environment variables from caprover-env-frontend.txt
```

**Frontend Environment Variables**:
```env
VITE_API_BASE_URL=https://multivendor-backend.your-caprover-domain.com
```

#### Step 3A.5: Create PostgreSQL Database
```bash
# On CapRover dashboard:
# 1. Go to "One-Click Apps/Databases"
# 2. Select PostgreSQL
# 3. Name it: postgres
# 4. Set password (same as DB_PASSWORD above)
```

#### Step 3A.6: Deploy Backend
```bash
cd /path/to/project
caprover deploy -a multivendor-backend

# Or use tar deployment
tar -czf backend-deploy.tar.gz \
  --exclude=node_modules \
  --exclude=venv \
  --exclude=front_end \
  captain-definition-backend \
  Dockerfile.backend \
  multivendor_platform/multivendor_platform \
  multivendor_platform/requirements.txt

# Upload backend-deploy.tar.gz via CapRover UI
```

#### Step 3A.7: Deploy Frontend
```bash
cd multivendor_platform/front_end
caprover deploy -a multivendor-frontend

# Or use CapRover UI to deploy
```

#### Step 3A.8: Run Backend Migrations
```bash
# Via CapRover console (backend app)
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

**Estimated Time**: 45 minutes

---

### Option B: Direct VPS Deployment

#### Step 3B.1: Prepare VPS
```bash
# SSH into VPS
ssh root@158.255.74.123

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Install Git
apt install git -y
```

#### Step 3B.2: Clone Repository
```bash
cd /opt
git clone <your-repo-url> multivendor_platform
cd multivendor_platform
```

#### Step 3B.3: Configure Environment
```bash
# Create .env file
cp .env.production .env
nano .env

# Set these values:
SECRET_KEY=<generate-random-key>
DEBUG=False
ALLOWED_HOSTS=158.255.74.123,your-domain.com
DB_PASSWORD=<strong-password>
CORS_ALLOWED_ORIGINS=http://158.255.74.123,https://your-domain.com
```

#### Step 3B.4: Build and Start
```bash
# Make scripts executable
chmod +x *.sh

# Start services
docker-compose up -d --build

# Wait 2-3 minutes for services to start
```

#### Step 3B.5: Run Migrations
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
docker-compose exec backend python manage.py createsuperuser
```

#### Step 3B.6: Configure Firewall
```bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

#### Step 3B.7: Setup SSL (Optional but Recommended)
```bash
./setup-ssl.sh your-domain.com
```

**Estimated Time**: 60 minutes

---

## ✅ Phase 4: Post-Deployment Verification

### Step 4.1: Check All Services Running
```bash
# For Docker Compose
docker-compose ps

# All services should show "Up" and "healthy"
```

### Step 4.2: Test Endpoints

#### Backend API
```bash
curl https://your-backend-url/api/
# Should return JSON response
```

#### Frontend
```bash
curl https://your-frontend-url/
# Should return HTML
```

#### Health Check
```bash
# If on VPS
./health-check.sh

# Manual check
curl https://your-backend-url/api/products/
curl https://your-backend-url/admin/
```

### Step 4.3: Browser Testing
- [ ] Open frontend URL in browser
- [ ] Check for console errors (F12)
- [ ] Navigate to products page
- [ ] Navigate to blog page
- [ ] Test search functionality
- [ ] Check responsive design (mobile view)

### Step 4.4: Admin Panel Testing
- [ ] Login to admin panel
- [ ] Create a product with image
- [ ] Create a blog post
- [ ] Verify images display correctly
- [ ] Check media files are accessible

### Step 4.5: Performance Check
```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s https://your-frontend-url/

# Check Docker resources
docker stats

# Check disk space
df -h
```

**Estimated Time**: 30 minutes

---

## 🔧 Phase 5: Configuration & Optimization

### Step 5.1: Setup Automated Backups
```bash
# On VPS
./setup-cron-backup.sh

# Verify cron job
crontab -l
```

### Step 5.2: Configure Monitoring
```bash
# Test monitoring script
./monitor.sh

# Setup as systemd service (optional)
# See DEPLOYMENT_GUIDE.md for details
```

### Step 5.3: Load Initial Data (Optional)
```bash
# If you have seed data
docker-compose exec backend python manage.py loaddata initial_data.json

# Or use management commands
docker-compose exec backend python manage.py populate_blog
```

### Step 5.4: Configure Email (Optional)
```bash
# Add to .env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Restart backend
docker-compose restart backend
```

### Step 5.5: Setup CDN (Optional)
- Configure Cloudflare or similar
- Update CORS settings
- Update ALLOWED_HOSTS

**Estimated Time**: 45 minutes

---

## 📊 Phase 6: Final Checks

### Step 6.1: Security Audit
- [ ] DEBUG is False
- [ ] SECRET_KEY is random and secure
- [ ] Database password is strong
- [ ] ALLOWED_HOSTS is configured
- [ ] CORS is properly restricted
- [ ] SSL/HTTPS is enabled
- [ ] Firewall is active
- [ ] Sensitive files not exposed

### Step 6.2: Performance Audit
- [ ] Static files are compressed
- [ ] Images are optimized
- [ ] Database has proper indexes
- [ ] Caching is configured
- [ ] Logs are rotating
- [ ] Resource limits are set

### Step 6.3: Functionality Audit
- [ ] All pages load correctly
- [ ] Forms submit successfully
- [ ] File uploads work
- [ ] Authentication works
- [ ] Search works
- [ ] APIs return correct data

### Step 6.4: Documentation Update
```bash
# Update README with production URLs
# Update DEPLOYMENT_SUMMARY.md
# Document any custom configurations
```

**Estimated Time**: 30 minutes

---

## 🎉 Phase 7: Go Live!

### Step 7.1: Announce Deployment
- [ ] Notify team members
- [ ] Update status page
- [ ] Send announcement email

### Step 7.2: Monitor Closely
```bash
# Watch logs for first hour
docker-compose logs -f

# Check error logs
docker-compose logs backend | grep ERROR
docker-compose logs frontend | grep ERROR
```

### Step 7.3: Have Rollback Plan Ready
```bash
# If something goes wrong:
docker-compose down
git checkout <previous-commit>
docker-compose up -d --build
```

**Estimated Time**: Ongoing monitoring for first 24 hours

---

## 📅 Total Estimated Timeline

| Phase | Description | Time |
|-------|-------------|------|
| 1 | Code Cleanup & Git | 15 min |
| 2 | Local Testing | 30 min |
| 3 | Deployment | 45-60 min |
| 4 | Verification | 30 min |
| 5 | Optimization | 45 min |
| 6 | Final Checks | 30 min |
| **Total** | | **3-4 hours** |

---

## 🆘 Emergency Contacts & Resources

### Quick Links
- **Documentation**: `PROJECT_CURRENT_STATE.md`
- **Quick Reference**: `PROJECT_QUICK_REFERENCE.md`
- **Troubleshooting**: `TROUBLESHOOTING_DEPLOYMENT.md`

### Emergency Commands
```bash
# Restart everything
docker-compose restart

# View all logs
docker-compose logs -f

# Rollback
git checkout <previous-commit>
docker-compose up -d --build --force-recreate

# Backup NOW
./backup-database.sh
```

---

## ✅ Success Criteria

Deployment is successful when:
- [ ] All services are running and healthy
- [ ] Frontend is accessible and functional
- [ ] Backend API responds correctly
- [ ] Admin panel is accessible
- [ ] Database is populated and accessible
- [ ] File uploads work
- [ ] No errors in logs
- [ ] SSL/HTTPS works (if configured)
- [ ] Monitoring is active
- [ ] Backups are configured

---

**Ready to Deploy?** Start with Phase 1! 🚀

**Last Updated**: October 27, 2025  
**Status**: Ready to Execute


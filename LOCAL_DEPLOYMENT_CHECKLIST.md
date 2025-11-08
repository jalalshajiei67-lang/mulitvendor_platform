# ✅ Local Deployment Checklist

Quick reference checklist for deploying the multivendor platform locally.

---

## 🔧 Prerequisites (One-Time Setup)

### System Requirements
- [ ] Windows 10/11, macOS 10.15+, or Linux
- [ ] 4GB+ RAM available (8GB recommended)
- [ ] 10GB+ free disk space
- [ ] Internet connection

### Software Installation
- [ ] **Docker Desktop** installed
  - Download: https://www.docker.com/products/docker-desktop/
  - Windows: Enable WSL 2 backend
  - macOS/Linux: Standard installation
- [ ] Docker Desktop is **running** (whale icon visible)
- [ ] Docker allocated at least 4GB RAM
  - Settings → Resources → Memory

---

## 🚀 Quick Start (5 Steps)

### Step 1: Verify Docker
```powershell
docker info
```
Expected: Docker information displayed (not an error)

### Step 2: Navigate to Project
```powershell
cd C:\Users\F003\Desktop\damirco
```

### Step 3: Start Services
**Windows:**
```powershell
# Double-click this file, or run:
test-local.bat
```

**Linux/Mac:**
```bash
docker-compose --env-file .env.local -f docker-compose.local.yml up --build
```

### Step 4: Wait for Services
- ⏱️ First time: 5-10 minutes (downloading images)
- ⏱️ Subsequent runs: 30-60 seconds
- ✅ Look for "healthy" status in logs

### Step 5: Access Application
- 🎨 **Frontend**: http://localhost:8080
- ⚙️ **Backend API**: http://localhost:8000/api/
- 👤 **Admin Panel**: http://localhost:8000/admin/

---

## ✅ Verification Checklist

### Service Status
```powershell
docker-compose -f docker-compose.local.yml ps
```

- [ ] `multivendor_db_local` - Up (healthy)
- [ ] `multivendor_backend_local` - Up (healthy)
- [ ] `multivendor_frontend_local` - Up (healthy)

### Functional Tests
- [ ] Frontend loads without errors
- [ ] API endpoint responds: http://localhost:8000/api/
- [ ] Admin panel accessible: http://localhost:8000/admin/
- [ ] No error messages in logs

### Database Tests
- [ ] Can create superuser:
```bash
docker exec -it multivendor_backend_local python manage.py createsuperuser
```
- [ ] Can login to admin panel
- [ ] Can create/view data through admin

---

## 📋 Common Tasks

### View Logs
```powershell
# All services
view-logs.bat

# Or manually
docker-compose -f docker-compose.local.yml logs -f
```

### Stop Services
```powershell
# Stop (keep data)
stop-local.bat

# Or manually
docker-compose -f docker-compose.local.yml down
```

### Restart After Changes
```powershell
# Restart specific service
docker-compose -f docker-compose.local.yml restart backend

# Rebuild after code changes
docker-compose -f docker-compose.local.yml up -d --build backend
```

### Fresh Start (Delete All Data)
```powershell
docker-compose -f docker-compose.local.yml down -v
test-local.bat
```

---

## 🐛 Troubleshooting Quick Fix

### Issue: Docker not running
```powershell
# Start Docker Desktop from Start Menu
# Wait for whale icon in system tray
docker info  # Verify it's running
```

### Issue: Port already in use
```powershell
# Find what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8080

# Kill the process or change port in docker-compose.local.yml
```

### Issue: Services keep restarting
```powershell
# Check logs for errors
view-logs.bat

# Or
docker-compose -f docker-compose.local.yml logs -f
```

### Issue: Can't connect to database
```
# Wait 30 seconds - database is initializing
# Check database logs
docker-compose -f docker-compose.local.yml logs db
```

### Issue: Build fails
```powershell
# Clear cache and rebuild
docker-compose -f docker-compose.local.yml build --no-cache
docker-compose -f docker-compose.local.yml up
```

---

## 📊 Resource Check

### Monitor Resource Usage
```powershell
docker stats
```

Expected usage:
- Backend: ~500MB RAM
- Database: ~100MB RAM
- Frontend: ~50MB RAM

### Clean Up Space
```powershell
# Remove unused images/containers
docker system prune -a --volumes

# WARNING: This deletes all data!
```

---

## 🎯 Pre-Production Testing

Before deploying to production, verify:

### Functionality
- [ ] User registration works
- [ ] User login works
- [ ] Products display correctly
- [ ] Orders can be created
- [ ] Admin panel fully functional
- [ ] File uploads work
- [ ] API endpoints respond correctly

### Performance
- [ ] Pages load quickly
- [ ] No memory leaks (check `docker stats`)
- [ ] Database queries are efficient
- [ ] No errors in logs after extended use

### Security
- [ ] Admin panel requires authentication
- [ ] API authentication works
- [ ] CORS configured correctly
- [ ] File upload restrictions work

---

## 🚀 Ready for Production?

Once all local tests pass:
1. ✅ Stop local services
2. 📝 Review production environment variables
3. 🔒 Change all passwords in `.env.production`
4. 📖 Read deployment guide: `DEPLOYMENT_GUIDE.md`
5. 🚀 Deploy using production scripts

---

## 📞 Need Help?

1. **Check logs**: `view-logs.bat`
2. **Read detailed guide**: `DEVOPS_LOCAL_DEPLOYMENT_ASSESSMENT.md`
3. **Review documentation**: 
   - `QUICK_START_LOCAL_TESTING.md`
   - `TEST_LOCALLY.md`
   - `LOCAL_DOCKER_SETUP_SUMMARY.md`
4. **Check Docker Desktop dashboard** for container status

---

## 🎓 Quick Commands Reference

```powershell
# Start everything
test-local.bat

# Stop everything
stop-local.bat

# View logs
view-logs.bat

# Service status
docker-compose -f docker-compose.local.yml ps

# Resource usage
docker stats

# Create admin
docker exec -it multivendor_backend_local python manage.py createsuperuser

# Django shell
docker exec -it multivendor_backend_local python manage.py shell

# Database shell
docker exec -it multivendor_db_local psql -U postgres -d multivendor_db

# Rebuild everything
docker-compose -f docker-compose.local.yml up -d --build

# Clean restart
docker-compose -f docker-compose.local.yml down -v
test-local.bat
```

---

## ⏱️ Time Estimates

| Task | First Time | Subsequent |
|------|-----------|------------|
| Install Docker Desktop | 10-15 min | - |
| Start services | 5-10 min | 30-60 sec |
| Create superuser | 1 min | 1 min |
| Full testing | 15-20 min | 5-10 min |
| **Total setup** | **30-45 min** | **5-10 min** |

---

**Last Updated**: October 26, 2025  
**Project Status**: ✅ Ready for local deployment  
**Next Step**: Run `test-local.bat` 🚀



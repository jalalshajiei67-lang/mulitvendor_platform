# 🚀 Deployment Verification Checklist

## ✅ Pre-Deployment Checks

### 1. Code Quality
- [x] GitHub Actions workflow updated to latest versions
- [x] Security scan added to CI/CD pipeline
- [x] No hardcoded secrets in codebase
- [x] Environment variables properly configured

### 2. Backend Configuration
- [x] Django settings_caprover.py properly configured
- [x] Channels and Redis configuration added for WebSocket chat
- [x] ASGI application configured for Daphne
- [x] Database settings updated for PostgreSQL
- [x] CORS and security settings configured
- [x] Static files and media files configured

### 3. Frontend Configuration
- [x] Nuxt.js configured for SSR
- [x] API base URL environment variable configured
- [x] RTL and Persian localization enabled
- [x] Production build optimized

### 4. Docker Configuration
- [x] Backend Dockerfile uses correct settings module
- [x] Frontend Dockerfile properly configured
- [x] captain-definition files point to correct Dockerfiles
- [x] Health checks configured

### 5. CapRover Setup Requirements
- [ ] PostgreSQL database app created (multivendor-db)
- [ ] Redis app created (multivendor-redis)
- [ ] Backend app created (multivendor-backend)
- [ ] Frontend app created (multivendor-frontend)
- [ ] Environment variables set in CapRover
- [ ] GitHub secrets configured
- [ ] Custom domains configured (api.indexo.ir, indexo.ir, www.indexo.ir)

## 🔧 Environment Variables Checklist

### Backend (CapRover App Configs)
```env
DEBUG=False
SECRET_KEY=<50+ character random key>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<from-caprover-postgres>
DB_HOST=srv-captain--multivendor-db
DB_PORT=5432
REDIS_HOST=srv-captain--multivendor-redis
REDIS_PORT=6379
ALLOWED_HOSTS=api.indexo.ir,indexo.ir,www.indexo.ir,multivendor-backend.indexo.ir
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
CSRF_TRUSTED_ORIGINS=https://indexo.ir,https://www.indexo.ir,https://api.indexo.ir
SITE_URL=https://indexo.ir
```

### Frontend (CapRover App Configs)
```env
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://api.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://indexo.ir
NUXT_HOST=0.0.0.0
NUXT_PORT=3000
```

### GitHub Secrets
```
CAPROVER_SERVER=https://captain.indexo.ir
CAPROVER_APP_BACKEND=multivendor-backend
CAPROVER_APP_FRONTEND=multivendor-frontend
CAPROVER_APP_TOKEN_BACKEND=<from-caprover>
CAPROVER_APP_TOKEN_FRONTEND=<from-caprover>
```

## 🧪 Testing Commands

### Local Testing
```bash
# Test backend build locally
docker build -t multivendor-backend .
docker run --rm -p 8000:8000 multivendor-backend

# Test frontend build locally
cd multivendor_platform/front_end/nuxt
docker build -t multivendor-frontend .
docker run --rm -p 3000:3000 multivendor-frontend
```

### Remote Testing (After Deployment)
```bash
# Test backend API
curl https://api.indexo.ir/api/

# Test frontend
curl https://indexo.ir/

# Test WebSocket (chat functionality)
# Should return WebSocket connection ready
```

## 🚨 Common Issues & Solutions

### Issue: Backend deployment fails
**Solution:** Check environment variables in CapRover, ensure PostgreSQL and Redis are running

### Issue: Frontend can't connect to API
**Solution:** Verify NUXT_PUBLIC_API_BASE is set correctly in frontend app configs

### Issue: Chat/WebSocket not working
**Solution:** Ensure Redis is running and REDIS_HOST/REDIS_PORT are configured in backend

### Issue: Static files not loading
**Solution:** Check STATIC_URL and STATIC_ROOT in Django settings

### Issue: HTTPS not working
**Solution:** Ensure HTTPS is enabled in CapRover app settings

## 📋 Deployment Steps

1. **Push to main branch** - Triggers automatic deployment
2. **Monitor GitHub Actions** - Check deployment logs
3. **Verify backend deployment** - Check CapRover logs
4. **Verify frontend deployment** - Check CapRover logs
5. **Test functionality** - Use testing commands above
6. **Check domains** - Ensure DNS points to CapRover

## 🎯 Post-Deployment Verification

- [ ] Backend API responds: `curl https://api.indexo.ir/api/`
- [ ] Frontend loads: `curl https://indexo.ir/`
- [ ] Admin panel accessible: `https://api.indexo.ir/admin/`
- [ ] Chat functionality works (WebSocket connection)
- [ ] Database migrations ran successfully
- [ ] Static files served correctly
- [ ] HTTPS certificates valid
- [ ] CORS headers working
- [ ] Persian RTL display correct

---

**Ready for deployment!** 🚀

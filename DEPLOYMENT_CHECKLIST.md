# 🚀 Deployment Checklist - Chat System

## ✅ Pre-Deployment Verification

### 1. Backend Verification

#### ✅ Chat App Structure
- [x] Chat app installed in settings.py (`INSTALLED_APPS`)
- [x] Chat URLs included in main urls.py
- [x] WebSocket routing configured in asgi.py
- [x] Daphne installed in requirements.txt
- [x] Redis channels configured in settings.py
- [x] Migrations created (`0001_initial.py` exists)

#### ✅ Required Environment Variables (Backend)

**Database:**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<your-strong-password>
DB_HOST=srv-captain--multivendor-db
DB_PORT=5432
```

**Redis (for WebSocket/Channels):**
```env
REDIS_HOST=srv-captain--multivendor-redis
REDIS_PORT=6379
```

**Django Settings:**
```env
DEBUG=False
SECRET_KEY=<generate-long-random-secret-50-chars-minimum>
```

**CORS & Security:**
```env
ALLOWED_HOSTS=api.indexo.ir,indexo.ir,www.indexo.ir,multivendor-backend.indexo.ir
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CSRF_TRUSTED_ORIGINS=https://indexo.ir,https://www.indexo.ir,https://api.indexo.ir
```

**Optional (for production):**
```env
USE_TLS=True
SITE_URL=https://indexo.ir
```

#### ✅ Backend Files Check
- [x] `Dockerfile` - Uses Daphne for ASGI
- [x] `captain-definition` - Points to Dockerfile
- [x] `requirements.txt` - Contains all dependencies
- [x] `asgi.py` - Configured for WebSocket
- [x] Chat models created
- [x] Chat consumers created
- [x] Chat serializers created
- [x] Chat views created

### 2. Frontend Verification

#### ✅ Chat Components
- [x] `stores/chat.ts` - Pinia store for chat management
- [x] `components/chat/ChatWidget.vue` - Floating chat widget
- [x] `components/chat/ChatPanel.vue` - Room list panel
- [x] `components/chat/ChatRoom.vue` - Chat interface
- [x] `components/product/ProductChatButton.vue` - Chat button on products
- [x] `pages/admin/chats.vue` - Admin chat management
- [x] `pages/vendor/chats.vue` - Vendor chat queue

#### ✅ Required Environment Variables (Frontend)

```env
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://api.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://indexo.ir
```

#### ✅ Frontend Files Check
- [x] `Dockerfile` - Multi-stage build for Nuxt
- [x] `captain-definition` - Points to Dockerfile
- [x] `package.json` - Contains all dependencies
- [x] WebSocket connection in chat store

### 3. Infrastructure Verification

#### ✅ CapRover Apps Required

1. **multivendor-db (PostgreSQL)**
   - Type: One-Click App - PostgreSQL 15
   - Status: Must be running before backend
   - Note password for backend config

2. **multivendor-redis (Redis)**
   - Type: One-Click App - Redis 7
   - Status: Must be running before backend
   - No password needed (internal connection)

3. **multivendor-backend (Django)**
   - Type: Custom App
   - Has Persistent Data: YES
   - Environment variables: See Backend section above
   - Depends on: PostgreSQL, Redis
   - Custom domains: api.indexo.ir

4. **multivendor-frontend (Nuxt)**
   - Type: Custom App
   - Has Persistent Data: NO
   - Environment variables: See Frontend section above
   - Depends on: Backend
   - Custom domains: indexo.ir, www.indexo.ir

#### ✅ Nginx Configuration
- [x] WebSocket proxying configured (`/ws/` location)
- [x] Upgrade headers set
- [x] Long timeout for WebSocket (86400s)
- [x] Buffering disabled for WebSocket

### 4. GitHub Actions CI/CD

#### ✅ Required GitHub Secrets

| Secret Name | Value | Where to Get |
|-------------|-------|--------------|
| `CAPROVER_SERVER` | `https://captain.indexo.ir` | Your CapRover URL |
| `CAPROVER_APP_BACKEND` | `multivendor-backend` | Backend app name |
| `CAPROVER_APP_FRONTEND` | `multivendor-frontend` | Frontend app name |
| `CAPROVER_APP_TOKEN_BACKEND` | `<token>` | CapRover → Backend → Deployment → Enable App Token |
| `CAPROVER_APP_TOKEN_FRONTEND` | `<token>` | CapRover → Frontend → Deployment → Enable App Token |

#### ✅ Workflow Files
- [x] `.github/workflows/deploy-caprover.yml` exists
- [x] Workflow deploys backend first, then frontend
- [x] Triggered on push to main branch

---

## 📋 Deployment Steps

### Step 1: CapRover Setup (Do Once)

#### A. Create PostgreSQL Database
```
1. CapRover Dashboard → Apps → One-Click Apps/Databases
2. Search "PostgreSQL"
3. App Name: multivendor-db
4. PostgreSQL Version: 15
5. Password: <create-strong-password>
6. Click Deploy
7. Wait for deployment to complete
8. Save password for later use
```

#### B. Create Redis
```
1. CapRover Dashboard → Apps → One-Click Apps/Databases
2. Search "Redis"
3. App Name: multivendor-redis
4. Click Deploy
5. Wait for deployment to complete
```

#### C. Create Backend App
```
1. CapRover Dashboard → Apps → Create New App
2. App Name: multivendor-backend
3. Has Persistent Data: YES
4. Click Create New App
5. Go to HTTP Settings → Enable HTTPS
6. Add custom domain: api.indexo.ir (optional)
```

**Add Backend Environment Variables:**
Go to App Configs tab and add all variables from "Backend Environment Variables" section above.

**Enable App Token:**
```
1. Go to Deployment tab
2. Click "Enable App Token"
3. Copy the token
4. Save it for GitHub Secrets
```

#### D. Create Frontend App
```
1. CapRover Dashboard → Apps → Create New App
2. App Name: multivendor-frontend
3. Has Persistent Data: NO
4. Click Create New App
5. Go to HTTP Settings → Enable HTTPS
6. Add custom domains: indexo.ir and www.indexo.ir
```

**Add Frontend Environment Variables:**
Go to App Configs tab and add all variables from "Frontend Environment Variables" section above.

**Enable App Token:**
```
1. Go to Deployment tab
2. Click "Enable App Token"
3. Copy the token
4. Save it for GitHub Secrets
```

### Step 2: GitHub Secrets Setup
```
1. Go to GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add all 5 secrets from the table above
```

### Step 3: Deploy

#### Option A: Automatic (Recommended)
```bash
git add .
git commit -m "Deploy chat system to production"
git push origin main
```

GitHub Actions will automatically:
1. Deploy backend to CapRover
2. Wait for backend to complete
3. Deploy frontend to CapRover

Monitor progress: GitHub → Actions tab

#### Option B: Manual Deploy
```bash
# Install CapRover CLI
npm install -g caprover

# Deploy backend
caprover deploy -a multivendor-backend

# Deploy frontend (from frontend directory)
cd multivendor_platform/front_end/nuxt
caprover deploy -a multivendor-frontend
```

### Step 4: Post-Deployment Tasks

#### A. Run Migrations
```
1. CapRover → Apps → multivendor-backend
2. Deployment tab → Execute Command section
3. Run: python manage.py migrate
4. Check output for success
```

#### B. Create Superuser
```
1. CapRover → Apps → multivendor-backend
2. Deployment tab → Execute Command
3. Run: python manage.py createsuperuser
4. Follow prompts (you'll be asked for username, email, password)
```

#### C. Collect Static Files (if needed)
```
1. CapRover → Apps → multivendor-backend
2. Deployment tab → Execute Command
3. Run: python manage.py collectstatic --noinput
```

### Step 5: Verify Deployment

#### Backend Tests
- [ ] Visit https://api.indexo.ir/api/
- [ ] API responds with data
- [ ] Visit https://api.indexo.ir/admin/
- [ ] Admin panel loads
- [ ] Login with superuser works
- [ ] Check chat models in admin

#### Frontend Tests
- [ ] Visit https://indexo.ir
- [ ] Homepage loads correctly
- [ ] Register/login works
- [ ] WebSocket connection establishes (check browser console)

#### Chat System Tests
- [ ] Open a product page
- [ ] Click "Chat with Vendor" button
- [ ] Chat widget opens
- [ ] Can send messages
- [ ] Messages appear in real-time
- [ ] Typing indicators work
- [ ] Admin can see all chats at `/admin/chats`
- [ ] Vendors can see their chats at `/vendor/chats`

#### WebSocket Tests
```javascript
// Open browser console on https://indexo.ir
// Check for:
// ✅ "WebSocket connected"
// ✅ "Chat connection established"
// ❌ No WebSocket errors
```

---

## 🔍 Debugging & Troubleshooting

### Check Backend Logs
```
CapRover → Apps → multivendor-backend → App Logs
Look for:
- Migration success
- Daphne starting
- WebSocket connections
- Redis connection
```

### Check Frontend Logs
```
CapRover → Apps → multivendor-frontend → App Logs
Look for:
- Nuxt starting
- Port 3000 listening
- No build errors
```

### Check Redis
```
CapRover → Apps → multivendor-redis → App Logs
Redis should be running without errors
```

### Check Database
```
CapRover → Apps → multivendor-db → App Logs
PostgreSQL should be accepting connections
```

### Common Issues

#### 1. WebSocket Connection Failed
**Problem:** Chat widget shows "Disconnected"

**Solutions:**
- Check ALLOWED_HOSTS includes your domain
- Check Redis is running
- Check backend logs for WebSocket errors
- Verify CORS settings allow WebSocket upgrade

#### 2. Database Connection Failed
**Problem:** Backend logs show "could not connect to server"

**Solutions:**
- Verify PostgreSQL app is running
- Check DB_HOST is `srv-captain--multivendor-db`
- Check DB_PASSWORD matches PostgreSQL password
- Check DB_PORT is 6379 (should be 5432)

#### 3. Redis Connection Failed
**Problem:** Backend logs show "Error connecting to Redis"

**Solutions:**
- Verify Redis app is running
- Check REDIS_HOST is `srv-captain--multivendor-redis`
- Check REDIS_PORT is 6379

#### 4. Frontend Can't Reach Backend
**Problem:** API requests fail with CORS errors

**Solutions:**
- Check CORS_ALLOWED_ORIGINS includes frontend domain
- Check CSRF_TRUSTED_ORIGINS includes frontend domain
- Verify NUXT_PUBLIC_API_BASE is correct

#### 5. Migrations Not Applied
**Problem:** Backend shows "no such table" errors

**Solutions:**
- Run migrations manually in CapRover
- Check migration files exist
- Verify database connection works

---

## 🔐 Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY (50+ random characters)
- [ ] Strong database password
- [ ] HTTPS enabled for all apps
- [ ] CORS configured (not allowing all origins)
- [ ] CSRF protection enabled
- [ ] ALLOWED_HOSTS restricted to actual domains
- [ ] No sensitive data in Git repository
- [ ] GitHub secrets configured properly
- [ ] Database backups enabled in CapRover

---

## 📊 Monitoring

### CapRover Monitoring
- Check app health in dashboard
- Monitor resource usage (CPU, Memory)
- Check logs for errors
- Set up alerts if needed

### Application Monitoring
- Test chat functionality daily
- Check WebSocket connections
- Monitor message delivery
- Test typing indicators
- Verify read receipts

### Performance
- Check response times
- Monitor database queries
- Check Redis memory usage
- Test under load

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ All CapRover apps show "Running" status
- ✅ Frontend loads at https://indexo.ir
- ✅ Backend API responds at https://api.indexo.ir/api/
- ✅ Admin panel accessible at https://api.indexo.ir/admin/
- ✅ WebSocket connects successfully
- ✅ Chat messages send and receive in real-time
- ✅ No errors in browser console
- ✅ No errors in CapRover logs
- ✅ Typing indicators work
- ✅ Read receipts work
- ✅ Both authenticated and guest users can chat

---

## 📞 Next Steps After Deployment

1. **Test thoroughly** - Try all chat features
2. **Create test accounts** - Test as buyer and vendor
3. **Monitor logs** - Check for any issues
4. **Set up backups** - Enable database backups in CapRover
5. **Performance testing** - Test with multiple users
6. **Mobile testing** - Test on mobile devices
7. **Documentation** - Update any user documentation

---

**Last Updated:** 2024-11-21
**Status:** ✅ Ready for Production Deployment

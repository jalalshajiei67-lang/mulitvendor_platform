# 🎯 START HERE - CapRover Deployment

## 📌 Quick Answer to Your Question

**Q: Do we need docker-compose.yml for CapRover?**

**A: NO!** CapRover doesn't use docker-compose.yml. However, we **kept it for local development**.

---

## 🏗️ What Was Done

### ✅ Project Restructured for CapRover

1. **Backend Dockerfile** - Updated to use Daphne (for WebSocket chat)
2. **captain-definition files** - Created for CapRover deployment
3. **GitHub Actions CI/CD** - Automatic deployment on push
4. **Documentation** - Complete guides created
5. **docker-compose.yml** - Kept but marked as "LOCAL DEVELOPMENT ONLY"

### 📁 File Purpose

| File | Used For |
|------|----------|
| `docker-compose.yml` | ✅ Local development only |
| `captain-definition` | ✅ CapRover backend deployment |
| `multivendor_platform/front_end/nuxt/captain-definition` | ✅ CapRover frontend deployment |
| `Dockerfile` | ✅ Backend (both local & CapRover) |
| `multivendor_platform/front_end/nuxt/Dockerfile` | ✅ Frontend (both local & CapRover) |
| `.github/workflows/deploy-caprover.yml` | ✅ Auto deployment (GitHub → CapRover) |

---

## 🚀 Deployment Steps (Copy & Follow)

### Step 1: CapRover Setup (One-Time)

Login to your CapRover: https://captain.indexo.ir

#### A. Create Database App
```
1. Apps → One-Click Apps/Databases
2. Search "PostgreSQL"
3. App Name: multivendor-db
4. Version: 15
5. Password: <create strong password>
6. Deploy

Note the connection details for later!
```

#### B. Create Redis App
```
1. Apps → One-Click Apps/Databases
2. Search "Redis"
3. App Name: multivendor-redis
4. Deploy
```

#### C. Create Backend App
```
1. Apps → Create New App
2. App Name: multivendor-backend
3. Has Persistent Data: YES
4. Click "Create New App"
5. Enable HTTPS (in HTTP Settings tab)
6. Add custom domain: api.indexo.ir (optional)
```

**Add Environment Variables** (App Configs tab):
```env
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-change-me

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<your-postgres-password-from-step-A>
DB_HOST=srv-captain--multivendor-db
DB_PORT=5432

REDIS_HOST=srv-captain--multivendor-redis
REDIS_PORT=6379

ALLOWED_HOSTS=api.indexo.ir,indexo.ir,www.indexo.ir,multivendor-backend.indexo.ir
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CSRF_TRUSTED_ORIGINS=https://indexo.ir,https://www.indexo.ir,https://api.indexo.ir
```

#### D. Create Frontend App
```
1. Apps → Create New App
2. App Name: multivendor-frontend
3. Has Persistent Data: NO
4. Click "Create New App"
5. Enable HTTPS
6. Add custom domains: indexo.ir and www.indexo.ir
```

**Add Environment Variables**:
```env
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://api.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://indexo.ir
```

### Step 2: GitHub Secrets Setup

Go to your GitHub repo: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 5 secrets:

| Secret Name | Value |
|------------|-------|
| `CAPROVER_SERVER` | `https://captain.indexo.ir` |
| `CAPROVER_APP_BACKEND` | `multivendor-backend` |
| `CAPROVER_APP_FRONTEND` | `multivendor-frontend` |
| `CAPROVER_APP_TOKEN_BACKEND` | Get from CapRover (see below) |
| `CAPROVER_APP_TOKEN_FRONTEND` | Get from CapRover (see below) |

**How to get App Tokens:**
1. CapRover → Apps → multivendor-backend
2. Deployment tab
3. "Enable App Token" button
4. Copy the token
5. Paste into GitHub Secret
6. Repeat for multivendor-frontend

### Step 3: Deploy!

**Option A: Automatic (Recommended)**
```bash
cd /path/to/your/project
git add .
git commit -m "Initial CapRover deployment"
git push origin main
```

→ GitHub Actions will automatically deploy both apps!  
→ Watch progress in: GitHub → Actions tab

**Option B: Manual**
```bash
# Install CapRover CLI (once)
npm install -g caprover

# Deploy backend
caprover deploy -a multivendor-backend

# Deploy frontend
cd multivendor_platform/front_end/nuxt
caprover deploy -a multivendor-frontend
```

### Step 4: Post-Deployment

#### Create Superuser
```
1. CapRover → Apps → multivendor-backend
2. Deployment tab
3. Execute Command section
4. Run: python manage.py createsuperuser
5. Follow prompts
```

#### Test Everything
- [ ] Frontend: https://indexo.ir
- [ ] Backend API: https://api.indexo.ir/api
- [ ] Admin: https://api.indexo.ir/admin
- [ ] Login works
- [ ] Chat works
- [ ] Products display

---

## 🏠 Local Development (Optional)

Want to test locally before deploying?

```bash
# Start everything
docker-compose up -d

# Access
Frontend: http://localhost:3000
Backend: http://localhost:8000
Admin: http://localhost:8000/admin

# Stop
docker-compose down
```

---

## 🔄 Daily Workflow

After initial setup, your workflow is simple:

```
1. Write code
2. Test locally (optional)
3. Git commit
4. Git push to main
5. GitHub Actions deploys automatically
6. Check https://indexo.ir
```

That's it! No manual deployment needed.

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                  Your VPS                        │
│         (185.208.172.76)                         │
│                                                   │
│  ┌───────────────────────────────────────────┐  │
│  │           CapRover                         │  │
│  │                                            │  │
│  │  ┌──────────────┐  ┌──────────────────┐  │  │
│  │  │ PostgreSQL   │  │ Redis            │  │  │
│  │  │ multivendor  │  │ multivendor      │  │  │
│  │  │    -db       │  │    -redis        │  │  │
│  │  └──────────────┘  └──────────────────┘  │  │
│  │                                            │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │ Backend (Django + Daphne)           │  │  │
│  │  │ multivendor-backend                 │  │  │
│  │  │ Domain: api.indexo.ir              │  │  │
│  │  │ • REST API                          │  │  │
│  │  │ • WebSocket Chat                    │  │  │
│  │  │ • Admin Dashboard                   │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  │                                            │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │ Frontend (Nuxt 3 SSR)              │  │  │
│  │  │ multivendor-frontend                │  │  │
│  │  │ Domain: indexo.ir, www.indexo.ir   │  │  │
│  │  │ • User Interface                    │  │  │
│  │  │ • Server-Side Rendering             │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  │                                            │  │
│  │  CapRover handles:                        │  │
│  │  ✓ HTTPS/SSL (automatic)                 │  │
│  │  ✓ Domains                                │  │
│  │  ✓ Container management                   │  │
│  │  ✓ Logging                                │  │
│  │  ✓ Restarts                               │  │
│  └───────────────────────────────────────────┘  │
│                                                   │
└─────────────────────────────────────────────────┘
                    ▲
                    │
            GitHub Actions (CI/CD)
                    │
                    ▼
            Your Git Repository
```

---

## ❓ FAQ

**Q: What happened to docker-compose.yml?**  
A: Still there! But only for local development. CapRover doesn't use it.

**Q: Do I need to manage containers manually?**  
A: No! CapRover manages everything automatically.

**Q: How do I update the website?**  
A: Just `git push`. GitHub Actions deploys automatically.

**Q: How do I see logs?**  
A: CapRover → Apps → Select App → App Logs

**Q: How do I restart an app?**  
A: CapRover → Apps → Select App → Actions → Restart

**Q: Can I still test locally?**  
A: Yes! Use `docker-compose up -d`

**Q: What about SSL certificates?**  
A: CapRover handles it automatically (Let's Encrypt)

**Q: How to rollback if deployment fails?**  
A: CapRover keeps previous versions. You can rollback in the dashboard.

---

## 📚 Documentation Reference

| Topic | File |
|-------|------|
| **Quick Start** | `QUICK_START.md` |
| **CapRover Setup** | `CAPROVER_DEPLOYMENT.md` |
| **GitHub Secrets** | `GITHUB_SECRETS_SETUP.md` |
| **Local vs Production** | `LOCAL_VS_CAPROVER.md` |
| **What Changed** | `CAPROVER_RESTRUCTURE_SUMMARY.md` |
| **Chat System** | `CHAT_SYSTEM_README.md` |

---

## ✅ Checklist

Before you start:
- [ ] CapRover is running on your VPS
- [ ] Domain (indexo.ir) points to your VPS IP
- [ ] You have access to CapRover dashboard
- [ ] You have admin access to GitHub repo

Setup (do once):
- [ ] Create PostgreSQL app in CapRover
- [ ] Create Redis app in CapRover
- [ ] Create backend app in CapRover
- [ ] Create frontend app in CapRover
- [ ] Set environment variables for backend
- [ ] Set environment variables for frontend
- [ ] Add 5 secrets to GitHub
- [ ] Enable App Tokens in CapRover apps

Deploy:
- [ ] Push to GitHub main branch
- [ ] Watch GitHub Actions deploy
- [ ] Create superuser on backend
- [ ] Test website at https://indexo.ir

---

## 🆘 Need Help?

1. Check the documentation files above
2. Check CapRover app logs (Dashboard → Apps → Select App → Logs)
3. Check GitHub Actions logs (GitHub → Actions tab)
4. Check docker-compose logs for local issues: `docker-compose logs -f`

---

**Ready to deploy? Start with Step 1 above! 🚀**


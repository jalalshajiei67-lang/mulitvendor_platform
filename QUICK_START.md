# 🚀 Quick Start Guide

## For Local Development

### Prerequisites
- Docker and Docker Compose installed
- Git

### Steps
```bash
# 1. Clone the repository (if not already)
git clone <your-repo-url>
cd mulitvendor_platform

# 2. Create .env file (optional, has defaults)
cp .env.template .env

# 3. Start all services
docker-compose up -d

# 4. Wait for services to start (~30 seconds)
docker-compose logs -f

# 5. Create superuser
docker-compose exec backend python manage.py createsuperuser

# 6. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api
# Admin: http://localhost:8000/admin
```

## For CapRover Production Deployment

### Prerequisites
- CapRover server running on VPS (185.208.172.76)
- Domain pointed to your server (indexo.ir)
- GitHub repository

### One-Time Setup

#### 1. Setup CapRover Apps

**PostgreSQL Database:**
```
1. CapRover → One-Click Apps → PostgreSQL
2. Name: multivendor-db
3. Password: <strong-password>
4. Deploy
```

**Redis:**
```
1. CapRover → One-Click Apps → Redis
2. Name: multivendor-redis
3. Deploy
```

**Backend App:**
```
1. CapRover → Apps → Create New App
2. Name: multivendor-backend
3. Enable HTTPS
4. Set environment variables (see CAPROVER_DEPLOYMENT.md)
```

**Frontend App:**
```
1. CapRover → Apps → Create New App
2. Name: multivendor-frontend
3. Enable HTTPS
4. Set environment variables (see CAPROVER_DEPLOYMENT.md)
```

#### 2. Setup GitHub Secrets

Go to GitHub repo → Settings → Secrets → Actions

Add these secrets:
- `CAPROVER_SERVER`: https://captain.indexo.ir
- `CAPROVER_APP_BACKEND`: multivendor-backend
- `CAPROVER_APP_FRONTEND`: multivendor-frontend
- `CAPROVER_APP_TOKEN_BACKEND`: <get from CapRover>
- `CAPROVER_APP_TOKEN_FRONTEND`: <get from CapRover>

See `GITHUB_SECRETS_SETUP.md` for details.

#### 3. Deploy

**Option A: Automatic (CI/CD)**
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```
GitHub Actions will automatically deploy!

**Option B: Manual (CapRover CLI)**
```bash
# Install CapRover CLI
npm install -g caprover

# Deploy backend
caprover deploy -a multivendor-backend

# Deploy frontend
cd multivendor_platform/front_end/nuxt
caprover deploy -a multivendor-frontend
```

#### 4. Create Superuser on Production
```
1. CapRover → Apps → multivendor-backend
2. Click "Deployment" tab
3. Open "Execute Command"
4. Run: python manage.py createsuperuser
```

## 📚 Documentation

- **Local Development**: `docker-compose.yml` + `LOCAL_VS_CAPROVER.md`
- **CapRover Deployment**: `CAPROVER_DEPLOYMENT.md`
- **GitHub CI/CD**: `GITHUB_SECRETS_SETUP.md`
- **Chat System**: `CHAT_SYSTEM_README.md`

## 🐛 Troubleshooting

### Local Development Not Working?
```bash
# Reset everything
docker-compose down -v
docker-compose up --build -d
```

### CapRover Deployment Failed?
1. Check GitHub Actions logs
2. Check CapRover app logs
3. Verify all secrets are set
4. Verify environment variables in CapRover

### Database Connection Issues?
- Local: Check `DB_HOST=db` in docker-compose
- CapRover: Check `DB_HOST=srv-captain--multivendor-db`

### Chat Not Working?
- Check Redis is running
- Check WebSocket connection (wss:// not http://)
- Check CORS settings

## 🎯 Next Steps After Deployment

1. ✅ Test login at https://indexo.ir
2. ✅ Access admin at https://indexo.ir/admin
3. ✅ Test chat functionality
4. ✅ Upload products
5. ✅ Configure payment gateway (if needed)
6. ✅ Setup email service (if needed)

## ⚡ Common Commands

### Local Development
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild
docker-compose up --build -d

# Access Django shell
docker-compose exec backend python manage.py shell

# Run migrations
docker-compose exec backend python manage.py migrate
```

### CapRover
```bash
# View app status
caprover list

# View logs
caprover logs -a multivendor-backend -f

# Restart app
# (Do this in CapRover Dashboard)
```

## 🆘 Need Help?

1. Check the relevant documentation file
2. Check GitHub Actions logs for deployment issues
3. Check CapRover app logs for runtime issues
4. Check Docker logs for local issues

---

**Remember**: 
- `docker-compose.yml` = Local development ONLY
- CapRover = Production deployment
- Never commit secrets to Git!

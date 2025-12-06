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

## For VPS Production Deployment

### Prerequisites
- VPS with Docker and Docker Compose installed
- Domain pointed to your server (indexo.ir)
- SSH access to VPS
- GitHub repository

### One-Time Setup

#### 1. Setup VPS

**On your VPS:**
```bash
# Clone repository
git clone <your-repo-url>
cd mulitvendor_platform

# Create .env file
cp .env.template .env
# Edit .env with your production values

# Start services
docker-compose up -d --build
```

#### 2. Setup GitHub Secrets (for CI/CD)

Go to GitHub repo → Settings → Secrets → Actions

Add these secrets:
- `VPS_HOST`: Your VPS IP (e.g., 185.208.172.76)
- `VPS_USER`: SSH username (e.g., root)
- `VPS_SSH_KEY`: Your SSH private key

See `GITHUB_ACTIONS_SETUP.md` for details.

#### 3. Deploy

**Option A: Automatic (CI/CD)**
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```
GitHub Actions will automatically deploy via SSH!

**Option B: Manual (SSH)**
```bash
# SSH to VPS
ssh user@your-vps-ip

# Navigate to project
cd /path/to/mulitvendor_platform

# Pull latest changes
git pull origin main

# Deploy
docker-compose up -d --build
```

#### 4. Create Superuser on Production
```bash
# SSH to VPS
ssh user@your-vps-ip

# Run command
docker-compose exec backend python manage.py createsuperuser
```

## 📚 Documentation

- **Local Development**: `docker-compose.yml` + `README_LOCAL_SETUP.md`
- **VPS Deployment**: `DEPLOYMENT_GUIDE.md`
- **GitHub CI/CD**: `GITHUB_ACTIONS_SETUP.md`
- **Chat System**: `CHAT_SYSTEM_README.md`

## 🐛 Troubleshooting

### Local Development Not Working?
```bash
# Reset everything
docker-compose down -v
docker-compose up --build -d
```

### VPS Deployment Failed?
1. Check GitHub Actions logs
2. SSH to VPS and check Docker logs: `docker-compose logs`
3. Verify all secrets are set in GitHub
4. Verify environment variables in `.env` file

### Database Connection Issues?
- Local: Check `DB_HOST=db` in docker-compose
- VPS: Check `DB_HOST=db` in docker-compose (service name)

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

### VPS Production
```bash
# SSH to VPS
ssh user@your-vps-ip
cd /path/to/mulitvendor_platform

# View container status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart
```

## 🆘 Need Help?

1. Check the relevant documentation file
2. Check GitHub Actions logs for deployment issues
3. SSH to VPS and check Docker logs for runtime issues
4. Check Docker logs for local issues

---

**Remember**: 
- `docker-compose.yml` = Production deployment on VPS
- `docker-compose.local.yml` = Local development
- Never commit secrets to Git!

# GitHub Actions CI/CD & VPS Deployment Checklist

## ✅ GitHub Secrets (Required)

- [ ] `VPS_HOST` = Your VPS IP address (e.g., `185.208.172.76`)
- [ ] `VPS_USER` = SSH username (e.g., `root`)
- [ ] `VPS_SSH_KEY` = Your SSH private key

**How to add:** GitHub Repo → Settings → Secrets and variables → Actions → New repository secret

---

## ✅ VPS Server Setup

### Docker & Docker Compose:
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Docker service running
- [ ] User has Docker permissions

### Network & Firewall:
- [ ] Ports 80, 443 open
- [ ] Port 22 (SSH) open
- [ ] Firewall configured (UFW recommended)

### Project Directory:
- [ ] Project cloned to VPS
- [ ] `.env` file created with production values
- [ ] Git repository configured

---

## ✅ Environment Configuration

### Backend Environment Variables (`.env`):
- [ ] `DB_NAME` = Database name
- [ ] `DB_USER` = Database user
- [ ] `DB_PASSWORD` = Strong database password
- [ ] `DB_HOST` = `db` (Docker service name)
- [ ] `DB_PORT` = `5432`
- [ ] `SECRET_KEY` = Django secret key
- [ ] `DEBUG` = `False`
- [ ] `ALLOWED_HOSTS` = Your domains (comma-separated)
- [ ] `CORS_ALLOWED_ORIGINS` = Your frontend URLs

### Frontend Environment Variables:
- [ ] `NUXT_PUBLIC_API_BASE` = Backend API URL
- [ ] `NODE_ENV` = `production`

---

## ✅ DNS Configuration

- [ ] `indexo.ir` → A record → Your VPS IP
- [ ] `api.indexo.ir` → A record → Your VPS IP
- [ ] `www.indexo.ir` → A record → Your VPS IP (optional)
- [ ] `staging.indexo.ir` → A record → Your VPS IP (for staging)

---

## ✅ Required Files Exist

- [ ] `.github/workflows/docker-deploy.yml` (production)
- [ ] `.github/workflows/deploy-staging.yml` (staging)
- [ ] `docker-compose.yml` (production)
- [ ] `docker-compose.staging.yml` (staging)
- [ ] `Dockerfile` (backend)
- [ ] `multivendor_platform/front_end/nuxt/Dockerfile` (frontend)
- [ ] `requirements.txt`
- [ ] `.env` (on VPS, not in git)

---

## ✅ Test Deployment

1. [ ] Push to `main` branch
2. [ ] Check GitHub Actions workflow status
3. [ ] Verify deployment succeeded
4. [ ] Test backend API: `https://api.indexo.ir/api/`
5. [ ] Test frontend: `https://indexo.ir`
6. [ ] Test admin panel: `https://api.indexo.ir/admin`

---

## 🔧 Quick Commands

### Check VPS Status:
```bash
ssh user@your-vps-ip
docker ps
docker-compose ps
```

### View Logs:
```bash
# On VPS
cd /path/to/project
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Manual Deploy (if needed):
```bash
# SSH to VPS
ssh user@your-vps-ip
cd /path/to/project

# Pull latest
git pull origin main

# Deploy
docker-compose up -d --build
```

---

## 📚 Full Documentation

See `DEPLOYMENT_GUIDE.md` and `TRAEFIK_DUAL_DEPLOYMENT.md` for detailed setup and troubleshooting.

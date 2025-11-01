# GitHub Actions CI/CD & CapRover Quick Checklist

## ✅ GitHub Secrets (Required)
- [ ] `CAPROVER_URL` = `https://captain.indexo.ir`
- [ ] `CAPROVER_PASSWORD` = Your CapRover password
- [ ] `CAPROVER_BACKEND_APP_NAME` = `multivendor-backend`
- [ ] `CAPROVER_FRONTEND_APP_NAME` = `multivendor-frontend`

**How to add:** GitHub Repo → Settings → Secrets and variables → Actions → New repository secret

---

## ✅ CapRover Apps Setup

### Backend App:
- [ ] App Name: `multivendor-backend`
- [ ] Domain: `multivendor-backend.indexo.ir`
- [ ] Environment Variables:
  - `DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover`
  - Database credentials (if not using secrets)
  - `SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`

### Frontend App:
- [ ] App Name: `multivendor-frontend`
- [ ] Domain: `indexo.ir`
- [ ] Environment Variables:
  - `VITE_API_BASE_URL=https://multivendor-backend.indexo.ir/api`

---

## ✅ Database Setup
- [ ] PostgreSQL installed in CapRover (One-Click App)
- [ ] Database created
- [ ] Connection credentials configured in backend app environment variables

---

## ✅ DNS Configuration
- [ ] `indexo.ir` → A record → `185.208.172.76`
- [ ] `multivendor-backend.indexo.ir` → A record → `185.208.172.76`
- [ ] `www.indexo.ir` → A record → `185.208.172.76` (optional)

---

## ✅ Required Files Exist
- [ ] `.github/workflows/ci.yml`
- [ ] `.github/workflows/deploy-caprover.yml`
- [ ] `Dockerfile.backend`
- [ ] `Dockerfile.frontend`
- [ ] `captain-definition-backend`
- [ ] `captain-definition-frontend`
- [ ] `multivendor_platform/multivendor_platform/settings_caprover.py`
- [ ] `requirements.txt`
- [ ] `nginx/frontend.conf`

---

## ✅ VPS Server
- [ ] CapRover installed and accessible at `https://captain.indexo.ir`
- [ ] Ports 80, 443, 3000 open
- [ ] Sufficient disk space
- [ ] Docker running

---

## ✅ Test Deployment
1. [ ] Push to `main` branch
2. [ ] Check GitHub Actions workflow status
3. [ ] Verify backend deployed successfully
4. [ ] Verify frontend deployed successfully
5. [ ] Test backend API: `https://multivendor-backend.indexo.ir/api/`
6. [ ] Test frontend: `https://indexo.ir`
7. [ ] Test admin panel: `https://multivendor-backend.indexo.ir/admin`

---

## 🔧 Quick Commands

### Check CapRover Status:
```bash
ssh root@185.208.172.76
docker ps | grep captain
```

### View App Logs:
```bash
# Via CapRover Dashboard
Apps → multivendor-backend → App Logs
```

### Manual Deploy (if needed):
```bash
npm install -g caprover
caprover deploy \
  --caproverUrl "https://captain.indexo.ir" \
  --caproverPassword "your-password" \
  --appName "multivendor-backend" \
  --tarFile backend-deploy.tar.gz
```

---

## 📚 Full Documentation
See `REQUIREMENTS_CI_CD_CAPROVER.md` for detailed requirements and troubleshooting.


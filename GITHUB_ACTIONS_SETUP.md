# GitHub Actions CI/CD Setup Guide

## Overview
Automated deployment pipeline for the multivendor platform using GitHub Actions and VPS (Docker Compose).

---

## 🎯 What's Included

Two workflows have been created:

1. **`docker-deploy.yml`** - Runs on push to main
   - Deploys to production VPS via SSH
   - Uses Docker Compose for deployment

2. **`deploy-staging.yml`** - Runs on push to staging
   - Deploys to staging VPS via SSH
   - Uses Docker Compose for staging deployment

---

## 📋 Setup Instructions

### Step 1: Configure GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

| Secret Name | Value | Description |
|------------|-------|-------------|
| `VPS_HOST` | `185.208.172.76` | Your VPS IP address |
| `VPS_USER` | `root` or your SSH username | SSH username for VPS |
| `VPS_SSH_KEY` | Your SSH private key | Private key for SSH access |

### Step 2: Generate SSH Key (if needed)

If you don't have an SSH key:

```bash
# Generate SSH key pair
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions

# Copy public key to VPS
ssh-copy-id -i ~/.ssh/github_actions.pub user@your-vps-ip

# Copy private key content for GitHub secret
cat ~/.ssh/github_actions
```

### Step 3: Verify Workflow Files

Check that these files exist:

```
.github/
└── workflows/
    ├── docker-deploy.yml      ✅ Production deployment
    └── deploy-staging.yml     ✅ Staging deployment
```

### Step 4: Configure VPS

#### On Your VPS:

1. **Clone repository** (if not already):
   ```bash
   git clone <your-repo-url> /path/to/project
   cd /path/to/project
   ```

2. **Create `.env` file**:
   ```bash
   cp .env.template .env
   nano .env  # Edit with your production values
   ```

3. **Ensure Docker and Docker Compose are installed**:
   ```bash
   docker --version
   docker-compose --version
   ```

4. **Test deployment manually**:
   ```bash
   docker-compose up -d --build
   ```

### Step 5: Test the Pipeline

```bash
# Make a small change
echo "# Test deployment" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main
```

### Step 6: Monitor Deployment

1. Go to your GitHub repo
2. Click **Actions** tab
3. Watch the workflow run
4. Check logs for any errors

---

## 🔄 Workflow Details

### Production Deployment (`docker-deploy.yml`)

**Triggers:**
- Push to `main` branch
- Manual trigger via GitHub UI

**Steps:**
1. SSH to VPS
2. Navigate to project directory
3. Pull latest changes from `main` branch
4. Run `deploy.sh` script
5. Deploy using Docker Compose

**Duration:** ~5-10 minutes

### Staging Deployment (`deploy-staging.yml`)

**Triggers:**
- Push to `staging` branch
- Manual trigger via GitHub UI

**Steps:**
1. Ensure Traefik network exists
2. SSH to VPS
3. Navigate to staging project directory
4. Pull latest changes from `staging` branch
5. Deploy using `docker-compose.staging.yml`

**Duration:** ~5-10 minutes

---

## 🔧 Customization

### Change Deployment Branch

Edit `.github/workflows/docker-deploy.yml`:

```yaml
on:
  push:
    branches:
      - production  # Change this
```

### Change VPS Project Path

Edit the workflow file:

```yaml
script: |
  cd /custom/path/to/project  # Change this
```

### Add Environment Variables

You can pass environment variables via GitHub secrets and use them in workflows:

```yaml
env:
  DEPLOY_ENV: production
```

---

## 🐛 Troubleshooting

### Deployment Fails: "Permission denied (publickey)"

**Problem:** SSH key not configured correctly

**Solution:**
1. Verify SSH key is added to GitHub secrets
2. Ensure public key is in VPS `~/.ssh/authorized_keys`
3. Test SSH connection manually: `ssh -i ~/.ssh/key user@vps-ip`

### Deployment Fails: "git reset --hard" error

**Problem:** Git repository state issues

**Solution:**
1. SSH to VPS and check git status
2. Ensure working directory is clean
3. Check git permissions

### Deployment Fails: "docker-compose: command not found"

**Problem:** Docker Compose not installed on VPS

**Solution:**
1. Install Docker Compose on VPS
2. Or use `docker compose` (v2) instead of `docker-compose`

### Services Not Starting

**Problem:** Docker containers fail to start

**Solution:**
1. SSH to VPS
2. Check logs: `docker-compose logs`
3. Verify `.env` file is configured correctly
4. Check disk space: `df -h`
5. Check Docker status: `docker ps -a`

---

## 📊 Monitoring Deployments

### View Logs

**In GitHub:**
1. Go to Actions tab
2. Click on workflow run
3. Click on job name
4. Expand steps to see logs

**On VPS:**
```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Deployment Status Badge

Add to your README.md:

```markdown
![Deploy Status](https://github.com/your-username/mulitvendor_platform/workflows/CI%2FCD%20Pipeline/badge.svg)
```

---

## 🚀 Best Practices

### 1. Test Before Deploy

Always test locally before pushing:
```bash
docker-compose up -d --build
# Test your changes
docker-compose down
```

### 2. Use Environment-Specific Configs

- Production: `docker-compose.yml` with production `.env`
- Staging: `docker-compose.staging.yml` with staging `.env`

### 3. Implement Rollback Strategy

```bash
# On VPS, if deployment fails:
cd /path/to/project
git checkout <previous-commit>
docker-compose up -d --build
```

### 4. Monitor Resources

```bash
# Check container status
docker-compose ps

# Check resource usage
docker stats

# Check disk space
df -h
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] GitHub secrets configured (`VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`)
- [ ] SSH access works from local machine
- [ ] Project cloned on VPS
- [ ] `.env` file created on VPS
- [ ] Docker and Docker Compose installed on VPS
- [ ] Workflow files committed to repository
- [ ] Test deployment succeeds
- [ ] Frontend loads correctly
- [ ] API calls work
- [ ] No console errors

---

## 🎉 Success!

Your CI/CD pipeline is now configured! Every push to main will automatically:
1. SSH to VPS
2. Pull latest code
3. Deploy using Docker Compose
4. Update your production site

**Deployment Time:** ~5-10 minutes from push to live

**Next Steps:**
- Add more tests
- Configure monitoring
- Add performance checks
- Setup automated backups

---

## 📚 Related Documentation

- `DEPLOYMENT_GUIDE.md` - Detailed deployment guide
- `TRAEFIK_DUAL_DEPLOYMENT.md` - Production + Staging setup
- `CI_CD_CHECKLIST.md` - Deployment checklist

# GitHub Actions CI/CD Setup Guide

## Overview
Automated deployment pipeline for the Nuxt multivendor platform using GitHub Actions and CapRover.

---

## 🎯 What's Included

Two workflows have been created:

1. **`test.yml`** - Runs on every push/PR
   - Tests Django backend
   - Builds Nuxt frontend
   - Validates code quality

2. **`deploy.yml`** - Runs on push to main/master
   - Deploys backend to CapRover
   - Deploys frontend to CapRover
   - Sequential deployment (backend first, then frontend)

---

## 📋 Setup Instructions

### Step 1: Get CapRover App Token

1. Login to CapRover: https://captain.indexo.ir
2. Go to **Settings** → **Deployment**
3. Copy your **App Token** (or generate new one)
4. Save it securely - you'll need it for GitHub

### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

| Secret Name | Value | Description |
|------------|-------|-------------|
| `CAPROVER_SERVER` | `https://captain.indexo.ir` | Your CapRover URL |
| `CAPROVER_APP_TOKEN` | `your-app-token-here` | From Step 1 |
| `CAPROVER_BACKEND_APP` | `multivendor-backend` | Backend app name |
| `CAPROVER_FRONTEND_APP` | `multivendor-frontend` | Frontend app name |

### Step 3: Verify Workflow Files

Check that these files exist:

```
.github/
└── workflows/
    ├── deploy.yml    ✅ Created
    └── test.yml      ✅ Created
```

### Step 4: Configure CapRover Apps

#### Backend App Configuration

1. Go to CapRover dashboard
2. Select `multivendor-backend` app
3. Go to **App Configs** tab
4. Add environment variables:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir
   CORS_ALLOWED_ORIGINS=https://indexo.ir
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=multivendor_db
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   DB_HOST=srv-captain--postgres
   DB_PORT=5432
   ```

#### Frontend App Configuration

1. Select `multivendor-frontend` app
2. Go to **App Configs** tab
3. Add environment variable:
   ```
   NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
   ```
4. **Important**: Set this BEFORE first deployment

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

### Test Workflow (`test.yml`)

**Triggers:**
- Push to `main`, `master`, or `develop`
- Pull requests to these branches

**Jobs:**

1. **test-backend**
   - Sets up PostgreSQL
   - Installs Python dependencies
   - Runs Django tests

2. **test-frontend**
   - Sets up Node.js 20
   - Installs npm dependencies
   - Builds Nuxt app
   - Validates build output

**Duration:** ~5-10 minutes

### Deploy Workflow (`deploy.yml`)

**Triggers:**
- Push to `main` or `master`
- Manual trigger via GitHub UI

**Jobs:**

1. **deploy-backend**
   - Deploys Django backend to CapRover
   - Uses `captain-definition-backend`

2. **deploy-frontend** (runs after backend)
   - Deploys Nuxt frontend to CapRover
   - Uses Nuxt Dockerfile
   - Sets correct build context

**Duration:** ~10-15 minutes

---

## 🔧 Customization

### Change Deployment Branch

Edit `.github/workflows/deploy.yml`:

```yaml
on:
  push:
    branches:
      - production  # Change this
```

### Add Staging Environment

Create `.github/workflows/deploy-staging.yml`:

```yaml
name: Deploy to Staging

on:
  push:
    branches:
      - develop

jobs:
  deploy-frontend-staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: caprover/deploy-from-github@v1.1.2
        with:
          server: '${{ secrets.CAPROVER_SERVER }}'
          app: 'multivendor-frontend-staging'
          token: '${{ secrets.CAPROVER_APP_TOKEN }}'
          dockerfile: './multivendor_platform/front_end/nuxt/Dockerfile'
          context: './multivendor_platform/front_end/nuxt'
```

### Add Slack Notifications

Add to end of deploy job:

```yaml
      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Add Build Caching

For faster builds, add caching:

```yaml
      - name: Cache Node modules
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

---

## 🐛 Troubleshooting

### Deployment Fails: "App not found"

**Problem:** CapRover app doesn't exist

**Solution:**
1. Create app in CapRover dashboard
2. Verify app name matches GitHub secret
3. Check spelling (case-sensitive)

### Deployment Fails: "Invalid token"

**Problem:** App token is wrong or expired

**Solution:**
1. Generate new token in CapRover
2. Update `CAPROVER_APP_TOKEN` secret in GitHub
3. Retry deployment

### Frontend Build Fails: "NUXT_PUBLIC_API_BASE not set"

**Problem:** Environment variable missing

**Solution:**
1. Add `NUXT_PUBLIC_API_BASE` in CapRover app config
2. Redeploy from GitHub Actions
3. Or add to workflow:
   ```yaml
   env:
     NUXT_PUBLIC_API_BASE: https://multivendor-backend.indexo.ir/api
   ```

### Tests Fail: "Database connection error"

**Problem:** PostgreSQL service not starting

**Solution:**
- Check `test.yml` service configuration
- Verify PostgreSQL version compatibility
- Check database credentials in workflow

### Deploy Hangs or Times Out

**Problem:** Large build or slow network

**Solution:**
1. Increase timeout in workflow:
   ```yaml
   timeout-minutes: 30
   ```
2. Check CapRover server resources
3. Optimize Docker build (use cache)

---

## 📊 Monitoring Deployments

### View Logs

**In GitHub:**
1. Go to Actions tab
2. Click on workflow run
3. Click on job name
4. Expand steps to see logs

**In CapRover:**
1. Go to app page
2. Click **App Logs** tab
3. View real-time logs

### Deployment Status Badge

Add to your README.md:

```markdown
![Deploy Status](https://github.com/your-username/mulitvendor_platform/workflows/Deploy%20to%20CapRover/badge.svg)
```

### Email Notifications

GitHub automatically sends emails on:
- Workflow failures
- First successful run after failure

Configure in: Settings → Notifications

---

## 🚀 Best Practices

### 1. Test Before Deploy

Always run tests before deploying:
```yaml
deploy-frontend:
  needs: [test-backend, test-frontend]
```

### 2. Use Environment-Specific Configs

```yaml
- name: Set production config
  run: |
    echo "NUXT_PUBLIC_API_BASE=${{ secrets.PROD_API_URL }}" >> $GITHUB_ENV
```

### 3. Implement Rollback Strategy

```yaml
- name: Save deployment info
  run: |
    echo "DEPLOYED_AT=$(date)" >> deployment.txt
    git tag "deploy-$(date +%Y%m%d-%H%M%S)"
```

### 4. Add Manual Approval

For production deployments:
```yaml
deploy-production:
  environment:
    name: production
    url: https://indexo.ir
  # Requires manual approval in GitHub
```

### 5. Separate Secrets per Environment

- `PROD_CAPROVER_TOKEN`
- `STAGING_CAPROVER_TOKEN`
- `DEV_CAPROVER_TOKEN`

---

## 📝 Workflow Files Reference

### deploy.yml
```yaml
name: Deploy to CapRover
on:
  push:
    branches: [main, master]
  workflow_dispatch:

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: caprover/deploy-from-github@v1.1.2
        with:
          server: '${{ secrets.CAPROVER_SERVER }}'
          app: '${{ secrets.CAPROVER_BACKEND_APP }}'
          token: '${{ secrets.CAPROVER_APP_TOKEN }}'

  deploy-frontend:
    needs: deploy-backend
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: caprover/deploy-from-github@v1.1.2
        with:
          server: '${{ secrets.CAPROVER_SERVER }}'
          app: '${{ secrets.CAPROVER_FRONTEND_APP }}'
          token: '${{ secrets.CAPROVER_APP_TOKEN }}'
          dockerfile: './multivendor_platform/front_end/nuxt/Dockerfile'
          context: './multivendor_platform/front_end/nuxt'
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] GitHub secrets configured
- [ ] CapRover apps created
- [ ] Environment variables set in CapRover
- [ ] Workflow files committed
- [ ] Test workflow passes
- [ ] Deploy workflow succeeds
- [ ] Frontend loads correctly
- [ ] API calls work
- [ ] No console errors

---

## 🎉 Success!

Your CI/CD pipeline is now configured! Every push to main will automatically:
1. Run tests
2. Deploy backend
3. Deploy frontend
4. Update your production site

**Deployment Time:** ~10-15 minutes from push to live

**Next Steps:**
- Add more tests
- Setup staging environment
- Configure monitoring
- Add performance checks






















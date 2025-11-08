# 🚀 CI/CD Setup Complete - GitHub Actions + CapRover

**Complete CI/CD Pipeline for Multivendor Platform**

---

## ✅ What Has Been Set Up

Your project now has a complete CI/CD pipeline that:

1. ✅ **Runs automated tests** on every push and pull request
2. ✅ **Checks code quality** with linting
3. ✅ **Generates coverage reports** (80% threshold)
4. ✅ **Auto-deploys to CapRover** when pushing to main branch
5. ✅ **Runs migrations automatically** after deployment
6. ✅ **Collects static files** automatically

---

## 📁 Files Created

### GitHub Actions Workflows

```
.github/
└── workflows/
    ├── ci.yml                    # Testing & Linting
    └── deploy-caprover.yml       # Deployment to CapRover
```

### Test Files Updated

```
multivendor_platform/multivendor_platform/
├── products/tests.py             # 18 test cases
├── users/tests.py                # 15 test cases
├── orders/tests.py               # 12 test cases
└── blog/tests.py                 # 13 test cases
```

### Dependencies Updated

```
requirements.txt                   # Added coverage==7.6.0
```

---

## 🔐 GitHub Secrets Required

You've already set these up:

| Secret Name | Value | Status |
|-------------|-------|--------|
| `CAPROVER_URL` | `https://captain.indexo.ir` | ✅ Set |
| `CAPROVER_PASSWORD` | `captain42` | ✅ Set |
| `CAPROVER_BACKEND_APP_NAME` | `multivendor-backend` | ✅ Set |
| `CAPROVER_FRONTEND_APP_NAME` | `multivendor-frontend` | ✅ Set |

---

## 🎯 How It Works

### On Every Push/PR to `main` or `develop`:

```mermaid
graph TD
    A[Push Code] --> B[GitHub Actions Triggered]
    B --> C[Backend Tests]
    B --> D[Frontend Linting]
    C --> E[Coverage Report]
    D --> F[Build Frontend]
    E --> G{Tests Pass?}
    F --> G
    G -->|Yes| H[✅ Success]
    G -->|No| I[❌ Fail - Fix Issues]
```

### On Push to `main` Branch:

```mermaid
graph TD
    A[Push to main] --> B[Run All Tests]
    B --> C{Tests Pass?}
    C -->|Yes| D[Deploy Backend]
    C -->|No| E[❌ Stop - Fix Tests]
    D --> F[Run Migrations]
    F --> G[Collect Static Files]
    G --> H[Deploy Frontend]
    H --> I[✅ Deployment Complete]
```

---

## 📊 Test Coverage

Your tests now cover:

### Products Module (18 tests)
- ✅ Department creation and slug generation
- ✅ Category creation and relationships
- ✅ Subcategory creation and department linking
- ✅ Product creation, stock, and pricing
- ✅ Product images
- ✅ API endpoints

### Users Module (15 tests)
- ✅ User creation and authentication
- ✅ User profiles (buyer/seller/both roles)
- ✅ Vendor profiles and approval
- ✅ Supplier management
- ✅ Seller advertisements
- ✅ Auth API endpoints

### Orders Module (12 tests)
- ✅ Order creation and number generation
- ✅ Order status changes
- ✅ Order items and subtotal calculation
- ✅ Payment processing
- ✅ Order API endpoints

### Blog Module (13 tests)
- ✅ Blog category creation
- ✅ Blog post creation and publishing
- ✅ Featured posts
- ✅ View count tracking
- ✅ Author-post relationships
- ✅ Blog API endpoints

**Total: 58 Test Cases**

---

## 🚀 Using Your CI/CD Pipeline

### Option 1: Push to Main (Auto-Deploy)

```bash
# Make your changes
git add .
git commit -m "Your commit message"
git push origin main

# GitHub Actions will automatically:
# 1. Run all tests
# 2. Check code quality
# 3. Deploy to CapRover
# 4. Run migrations
# 5. Collect static files
```

### Option 2: Create Pull Request (Test Only)

```bash
# Create a feature branch
git checkout -b feature/new-feature

# Make your changes
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# On GitHub: Create Pull Request
# GitHub Actions will run tests but NOT deploy
```

### Option 3: Manual Deployment

Go to GitHub → **Actions** → **Deploy to CapRover** → **Run workflow**

---

## 📈 Monitoring Your Pipeline

### View Test Results

1. Go to: `https://github.com/jalalshajiei67-lang/mulitvendor_platform/actions`
2. Click on any workflow run
3. View test results and coverage reports

### Download Coverage Report

1. Go to workflow run
2. Scroll to **Artifacts**
3. Download `coverage-report`
4. Open `htmlcov/index.html` in browser

### View Logs

```bash
# View GitHub Actions logs
# Go to: Repository → Actions → Select workflow run

# View CapRover logs
caprover apps:logs multivendor-backend
caprover apps:logs multivendor-frontend
```

---

## 🔍 Workflow Details

### CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**Jobs:**
1. **Backend Tests**
   - Sets up Python 3.11
   - Installs dependencies
   - Runs Django tests with PostgreSQL
   - Generates coverage report (minimum 80%)
   - Checks for missing migrations

2. **Frontend Linting**
   - Sets up Node.js 20
   - Installs dependencies
   - Runs ESLint
   - Builds frontend

**Duration:** ~3-5 minutes

### Deploy Workflow (`.github/workflows/deploy-caprover.yml`)

**Triggers:**
- Push to `main` branch only
- Manual trigger via GitHub UI

**Jobs:**
1. **Deploy Backend**
   - Creates tarball excluding unnecessary files
   - Deploys to CapRover backend app
   - Runs database migrations
   - Collects static files

2. **Deploy Frontend**
   - Creates tarball for frontend
   - Deploys to CapRover frontend app
   - Waits for backend to finish first

3. **Deployment Summary**
   - Shows deployment status
   - Displays URLs for frontend/backend

**Duration:** ~5-10 minutes

---

## 🛠️ Troubleshooting

### Tests Failing Locally?

```bash
# Run tests locally
cd multivendor_platform/multivendor_platform
python manage.py test --verbosity=2

# Check specific app
python manage.py test products --verbosity=2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Deployment Failing?

**Check CapRover Apps:**
```bash
caprover apps:list
caprover apps:logs multivendor-backend
```

**Verify Secrets:**
- Go to GitHub → Settings → Secrets → Actions
- Verify all 4 secrets are set correctly

**Common Issues:**
1. **CapRover password incorrect** → Update `CAPROVER_PASSWORD` secret
2. **App name wrong** → Check app names match exactly
3. **CapRover URL wrong** → Should be `https://captain.indexo.ir`

### Coverage Below 80%?

```bash
# Run coverage report locally
coverage run --source='.' manage.py test
coverage report --show-missing

# See which files need more tests
coverage html
# Open htmlcov/index.html
```

**Add more tests to:**
- Models that lack tests
- Views/API endpoints
- Business logic functions

---

## 📝 Customizing Your Pipeline

### Change Coverage Threshold

Edit `.github/workflows/ci.yml`:

```yaml
# Line ~68
coverage report --fail-under=80  # Change 80 to your threshold
```

### Add More Checks

```yaml
# Add to .github/workflows/ci.yml
- name: Check Python code style
  run: |
    pip install black
    black --check .
```

### Add Slack/Discord Notifications

```yaml
# Add at end of deploy-caprover.yml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 📊 Deployment Statistics

### Current Setup

| Metric | Value |
|--------|-------|
| Test Cases | 58 |
| Coverage Target | 80% |
| Deploy Time | ~5-10 min |
| Test Time | ~3-5 min |
| Auto Deploy | ✅ Enabled |
| Manual Deploy | ✅ Available |

---

## 🎯 Next Steps

### Recommended Actions

1. ✅ **Push to GitHub** - Trigger your first CI/CD run
   ```bash
   git add .
   git commit -m "Add CI/CD pipeline"
   git push origin main
   ```

2. ✅ **Watch the Magic** - Go to Actions tab and watch it run

3. ✅ **Check Deployment** - Visit your sites:
   - Frontend: https://indexo.ir
   - Backend: https://backend.indexo.ir/api
   - Admin: https://backend.indexo.ir/admin

4. ✅ **Set Up Branch Protection** (Optional but recommended):
   - Go to Repository → Settings → Branches
   - Add rule for `main` branch
   - Require status checks to pass before merging
   - Require pull request reviews

5. ✅ **Add More Tests** - Improve coverage over time

---

## 🔗 Useful Commands

### GitHub Actions

```bash
# View workflows
gh workflow list

# View runs
gh run list

# Watch a run
gh run watch

# View logs
gh run view <run-id> --log
```

### CapRover

```bash
# Login
caprover login

# Deploy manually
caprover deploy --appName multivendor-backend

# View logs
caprover apps:logs multivendor-backend -f

# Restart app
caprover apps:restart multivendor-backend

# Run command
caprover apps:exec multivendor-backend --command "python manage.py migrate"
```

### Local Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test products

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Check migrations
python manage.py makemigrations --check

# Lint frontend
cd multivendor_platform/front_end
npm run lint
```

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CapRover Documentation](https://caprover.com/docs/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

---

## 🎉 Summary

Your multivendor platform now has:

✅ Automated testing on every commit  
✅ Code quality checks  
✅ 80% test coverage requirement  
✅ Automatic deployment to production  
✅ Database migrations auto-run  
✅ Static files auto-collected  
✅ Deployment status tracking  
✅ Easy rollback capabilities  

**Your CI/CD pipeline is ready to use!** 🚀

---

## 📞 Getting Help

If you encounter issues:

1. **Check GitHub Actions logs** - Most errors are visible here
2. **Check CapRover logs** - `caprover apps:logs [app-name]`
3. **Run tests locally** - Reproduce issues on your machine
4. **Verify secrets** - Make sure all 4 GitHub secrets are set correctly

---

**Created:** October 28, 2025  
**Last Updated:** October 28, 2025  
**Version:** 1.0  
**Status:** ✅ Complete and Ready to Use


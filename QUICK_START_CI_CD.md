# 🚀 Quick Start - CI/CD Pipeline

**Get Your CI/CD Running in 5 Minutes**

---

## ✅ Setup Complete!

Your CI/CD pipeline is fully configured and ready to use!

---

## 🎯 What You Need to Do Now

### Step 1: Commit and Push (2 minutes)

```bash
# Add all the new files
git add .

# Commit with a descriptive message
git commit -m "Add CI/CD pipeline with GitHub Actions and CapRover deployment"

# Push to GitHub
git push origin main
```

### Step 2: Watch It Run (3 minutes)

1. Go to: https://github.com/jalalshajiei67-lang/mulitvendor_platform/actions
2. You'll see two workflows running:
   - ✅ **CI - Tests & Linting** (3-5 min)
   - ✅ **Deploy to CapRover** (5-10 min)

### Step 3: Verify Deployment

After workflows complete, check your sites:

- **Frontend:** https://indexo.ir
- **Backend API:** https://backend.indexo.ir/api
- **Admin Panel:** https://backend.indexo.ir/admin

---

## 📋 What Was Created

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Runs tests & linting |
| `.github/workflows/deploy-caprover.yml` | Deploys to CapRover |
| `products/tests.py` | 18 test cases |
| `users/tests.py` | 15 test cases |
| `orders/tests.py` | 12 test cases |
| `blog/tests.py` | 13 test cases |
| `CI_CD_SETUP_COMPLETE.md` | Full documentation |

**Total: 58 test cases with 80% coverage requirement**

---

## 🎯 From Now On

### Every Time You Push to `main`:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

**GitHub Actions will automatically:**
1. ✅ Run all 58 tests
2. ✅ Check code quality
3. ✅ Generate coverage report
4. ✅ Deploy backend to CapRover
5. ✅ Run database migrations
6. ✅ Collect static files
7. ✅ Deploy frontend to CapRover

**No manual deployment needed!** 🎉

---

## 🛠️ Common Commands

### Run Tests Locally

```bash
cd multivendor_platform/multivendor_platform
python manage.py test --verbosity=2
```

### Check Coverage Locally

```bash
coverage run --source='.' manage.py test
coverage report
```

### Manually Deploy to CapRover

```bash
# Login
caprover login

# Deploy backend
caprover deploy --appName multivendor-backend

# Deploy frontend
caprover deploy --appName multivendor-frontend
```

### View CapRover Logs

```bash
caprover apps:logs multivendor-backend -f
caprover apps:logs multivendor-frontend -f
```

---

## 🎉 Success Indicators

After your first push, you should see:

✅ Green checkmarks in GitHub Actions  
✅ All tests passing  
✅ Coverage above 80%  
✅ Backend deployed successfully  
✅ Frontend deployed successfully  
✅ Sites accessible at indexo.ir  

---

## 📚 Need More Info?

See `CI_CD_SETUP_COMPLETE.md` for:
- Detailed workflow explanations
- Troubleshooting guide
- Customization options
- Advanced features

---

## 🔗 Important Links

- **GitHub Actions:** https://github.com/jalalshajiei67-lang/mulitvendor_platform/actions
- **CapRover Dashboard:** https://captain.indexo.ir
- **Frontend:** https://indexo.ir
- **Backend:** https://backend.indexo.ir
- **Admin:** https://backend.indexo.ir/admin

---

## 🎯 Next Push Command

```bash
git add .
git commit -m "Add CI/CD pipeline"
git push origin main
```

**That's it! Your CI/CD is ready!** 🚀


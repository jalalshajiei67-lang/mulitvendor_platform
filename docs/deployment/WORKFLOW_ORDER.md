# 📋 GitHub Actions Workflow Order

## Current Workflows

When you push to the `staging` branch, **3 workflows run**:

1. **Run Tests** (`test.yml`)
   - ✅ Runs tests on backend
   - ✅ Runs in parallel with other workflows
   - ⏱️ Duration: ~2-5 minutes

2. **Build and Push Docker Images** (`build-and-push-images.yml`)
   - ✅ Builds backend and frontend Docker images
   - ✅ Pushes images to GitHub Container Registry
   - ⏱️ Duration: ~5-10 minutes (depends on cache)

3. **Deploy Staging** (`deploy-staging.yml`)
   - ✅ Waits for "Build and Push Docker Images" to complete
   - ✅ Pulls pre-built images from registry
   - ✅ Deploys to VPS
   - ⏱️ Duration: ~2-3 minutes

## 🔄 Execution Order

```
Push to staging
  ↓
┌─────────────────────────────────────┐
│  Run Tests (parallel)               │
│  ⏱️ ~2-5 min                        │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  Build and Push Docker Images       │
│  ⏱️ ~5-10 min                       │
│  ✅ Must complete before deploy     │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│  Deploy Staging                      │
│  ⏱️ ~2-3 min                        │
│  ⏳ Waits for build to finish       │
└─────────────────────────────────────┘
```

## ✅ Is This OK?

**Yes, this is correct!** Here's why:

1. **Tests run in parallel** - They don't block deployment
2. **Build runs first** - Images must exist before deployment
3. **Deploy waits for build** - Uses `workflow_run` trigger to wait
4. **All workflows are independent** - Each can succeed/fail independently

## 🔍 How to Monitor

### GitHub Actions Dashboard

1. Go to **GitHub** → **Actions** tab
2. You'll see all 3 workflows running
3. **Run Tests** - Should complete first (or in parallel)
4. **Build and Push Docker Images** - Must complete successfully
5. **Deploy Staging** - Will start automatically after build completes

### Expected Timeline

```
Time 0:00  → Push to staging
Time 0:00  → All 3 workflows start
Time 2:00  → Run Tests completes ✅
Time 5:00  → Build and Push completes ✅
Time 5:00  → Deploy Staging starts automatically
Time 7:00  → Deploy Staging completes ✅
```

## ⚠️ Troubleshooting

### Issue: Deploy starts before build finishes

**Solution:** This shouldn't happen with `workflow_run` trigger, but if it does:
- The deploy workflow will wait/poll for images (up to 10 retries)
- If images aren't available, deploy will fail with a clear error

### Issue: Deploy fails with "images not found"

**Possible causes:**
1. Build workflow failed - Check build workflow logs
2. Images not pushed - Check GitHub Packages
3. Wrong image names - Verify `DOCKER_REGISTRY`, `DOCKER_REPO`, `IMAGE_TAG`

**Solution:**
1. Check "Build and Push Docker Images" workflow status
2. Verify images exist: Go to **GitHub** → **Packages**
3. Check image names match in `docker-compose.staging.yml`

### Issue: Tests fail but deploy still runs

**This is expected behavior:**
- Tests are informational (don't block deployment)
- If you want tests to block deployment, we can add that requirement

## 🎯 Best Practices

1. **Monitor build workflow first** - Make sure it succeeds
2. **Check images in Packages** - Verify they were pushed
3. **Then check deploy** - Should start automatically after build

## 📝 Manual Deployment

If you need to deploy manually (without waiting for build):

1. Go to **Actions** → **Deploy Staging**
2. Click **Run workflow**
3. Check **Skip build check** (only if images already exist)
4. Click **Run workflow**

## 🔧 Workflow Dependencies

Current setup:
- ✅ **Deploy** waits for **Build** (via `workflow_run`)
- ✅ **Tests** runs independently (doesn't block anything)
- ✅ All workflows can be triggered manually

If you want **Tests** to block deployment:
- We can add a requirement that deploy waits for tests
- This would prevent deployment if tests fail

## ✅ Summary

**Your current setup is correct!** The 3 workflows are:
1. ✅ **Run Tests** - Runs in parallel (doesn't block)
2. ✅ **Build and Push** - Must complete first
3. ✅ **Deploy** - Waits for build, then deploys

This is the standard and recommended approach for CI/CD pipelines.


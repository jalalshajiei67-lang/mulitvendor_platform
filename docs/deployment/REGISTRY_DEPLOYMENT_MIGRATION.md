# 🚀 Migration to Registry-Based Deployment

## What Changed

We've migrated from **building on VPS** to **building on GitHub Actions** and pulling pre-built images. This solves the memory issues on your 2GB RAM VPS.

## 📝 Files Modified

### 1. `.github/workflows/build-and-push-images.yml` (NEW)
- **Purpose**: Builds Docker images on GitHub Actions and pushes to GHCR
- **Triggers**: Push to `staging` or `main` branches
- **What it does**:
  - Builds backend image: `ghcr.io/<repo>-backend:staging`
  - Builds frontend image: `ghcr.io/<repo>-frontend:staging`
  - Uses GitHub Actions cache for faster builds
  - No memory constraints (runs on GitHub's infrastructure)

### 2. `.github/workflows/deploy-staging.yml` (UPDATED)
- **Before**: Built images on VPS using `docker compose up -d --build`
- **After**: Pulls pre-built images using `docker compose up -d`
- **Changes**:
  - Added GHCR authentication
  - Removed `--build` flag
  - Added image pull step
  - Sets `DOCKER_REGISTRY`, `DOCKER_REPO`, and `IMAGE_TAG` in `.env.staging`

### 3. `docker-compose.staging.yml` (UPDATED)
- **Before**: 
  ```yaml
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
  ```
- **After**:
  ```yaml
  backend:
    image: ${DOCKER_REGISTRY:-ghcr.io}/${DOCKER_REPO:-damirco}-backend:${IMAGE_TAG:-staging}
  ```
- **Same change for frontend**

## 🔄 Deployment Flow

### Before (Old Way)
```
Push to staging
  ↓
Copy files to VPS
  ↓
SSH into VPS
  ↓
docker compose build (❌ Fails - Out of Memory)
```

### After (New Way)
```
Push to staging
  ↓
GitHub Actions: Build Images (✅ Success - More Resources)
  ↓
Push to GHCR
  ↓
GitHub Actions: Deploy
  ↓
SSH into VPS
  ↓
docker login ghcr.io
  ↓
docker compose pull (✅ Fast - Just Downloads)
  ↓
docker compose up -d (✅ Success - No Build!)
```

## ✅ Benefits

1. **No Memory Issues**: Build happens on GitHub Actions (7GB RAM available)
2. **Faster Deployments**: Pulling images is much faster than building
3. **Consistent Builds**: Same environment every time
4. **Better Caching**: GitHub Actions caches Docker layers efficiently
5. **No VPS Load**: VPS only runs containers, doesn't build them

## 🔐 Authentication

### Public Repository
- ✅ Works automatically with `GITHUB_TOKEN`
- ✅ No additional setup needed

### Private Repository
- ⚠️ Requires Personal Access Token (PAT)
- Add `GHCR_TOKEN` secret with `read:packages` permission
- See [REGISTRY_DEPLOYMENT_SETUP.md](./REGISTRY_DEPLOYMENT_SETUP.md) for details

## 📋 Next Steps

1. **Verify workflows exist**:
   ```bash
   ls -la .github/workflows/
   # Should see:
   # - build-and-push-images.yml
   # - deploy-staging.yml
   ```

2. **Push to staging**:
   ```bash
   git checkout staging
   git push origin staging
   ```

3. **Monitor workflows**:
   - Go to GitHub → Actions
   - Watch "Build and Push Docker Images"
   - Then watch "Deploy Staging"

4. **Verify deployment**:
   ```bash
   ssh root@185.208.172.76
   cd /root/indexo-staging
   docker compose -f docker-compose.staging.yml ps
   ```

## 🐛 Troubleshooting

### Build workflow fails
- Check GitHub Actions logs
- Verify Dockerfile paths are correct
- Check build args are set correctly

### Deploy workflow fails to pull images
- Verify images exist in GitHub Packages
- Check authentication (GHCR_TOKEN secret)
- Verify image names match in docker-compose.staging.yml

### Images not found
- Make sure build workflow completed first
- Check image tags match (should be `staging` for staging branch)
- Verify `DOCKER_REGISTRY`, `DOCKER_REPO`, and `IMAGE_TAG` in `.env.staging`

## 📚 Documentation

- [Registry Deployment Setup](./REGISTRY_DEPLOYMENT_SETUP.md) - Complete setup guide
- [Low Memory Build Fix](./LOW_MEMORY_BUILD_FIX.md) - Original memory optimization (now obsolete)

## 🎉 Result

Your VPS no longer needs to build Docker images! All builds happen on GitHub Actions, and your VPS just pulls and runs the pre-built images. This completely eliminates the memory issues you were experiencing.


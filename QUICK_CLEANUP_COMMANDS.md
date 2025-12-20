# 🧹 Quick Docker Cleanup Commands

## Safe Cleanup (Recommended)

### 1. Remove Stopped Containers
```bash
# See what will be removed
docker ps -a --filter "status=exited"

# Remove stopped containers
docker container prune -f
```

### 2. Remove Dangling Images
```bash
# See dangling images
docker images -f "dangling=true"

# Remove them
docker image prune -f
```

### 3. Remove Unused Volumes (⚠️ Be Careful!)
```bash
# See unused volumes
docker volume ls -f "dangling=true"

# Remove unused volumes (ONLY if you're sure!)
docker volume prune -f
```

### 4. Remove All Unused Resources
```bash
# This removes: stopped containers, dangling images, unused volumes, unused networks
docker system prune -a --volumes -f
```

## Check Disk Usage First

```bash
# See how much space Docker is using
docker system df

# Detailed breakdown
docker system df -v
```

## Identify Old Containers

### Find containers not in use:
```bash
# All containers
docker ps -a

# Containers older than 24 hours
docker ps -a --filter "status=exited" --format "{{.ID}}\t{{.Names}}\t{{.Status}}"
```

### Find old images:
```bash
# All images sorted by date
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"

# Images not used by any container
docker images --filter "dangling=true"
```

## Your Current Containers

Based on your `docker ps` output:

**Production (keep these):**
- `multivendor_backend` - Current backend
- `multivendor_db` - Current database
- `multivendor_frontend` - Current frontend
- `multivendor_nginx` - Current nginx
- `traefik` - Reverse proxy
- `multivendor_redis` - Current redis

**Staging (keep if you use staging):**
- `indexo_db_staging` - Staging database
- `multivendor_redis_staging` - Staging redis
- `multivendor_nginx_staging` - Staging nginx

**To find and remove:**
- Any stopped containers from old deployments
- Old images with different tags
- Unused volumes

## Recommended Cleanup Sequence

```bash
# 1. Check what's using space
docker system df

# 2. Remove stopped containers (safe)
docker container prune -f

# 3. Remove dangling images (safe)
docker image prune -f

# 4. Check again
docker system df

# 5. If you want to be more aggressive (removes unused images too)
docker image prune -a -f
```

## ⚠️ WARNING

**DO NOT run these if you're unsure:**
- `docker system prune -a --volumes` - Removes ALL unused resources including images
- `docker volume prune` - Removes volumes not attached to containers (could lose data!)

**Safe commands:**
- `docker container prune` - Only removes stopped containers
- `docker image prune` - Only removes dangling images (untagged)



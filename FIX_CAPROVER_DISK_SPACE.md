# Fix CapRover Disk Space Issue

## Problem
Deployment is failing with error: `no space left on device`

This means your CapRover server (185.208.172.76) has run out of disk space.

## Solution: Free Up Disk Space

### Step 1: SSH into your VPS
```bash
ssh root@185.208.172.76
```

### Step 2: Check Disk Usage
```bash
# Check overall disk usage
df -h

# Check Docker disk usage
docker system df
```

### Step 3: Clean Up Docker Resources

#### Remove unused Docker images (this usually frees the most space):
```bash
# Remove all unused images (dangling and unreferenced)
docker image prune -a -f

# Or remove images older than 24 hours
docker image prune -a --filter "until=24h" -f
```

#### Remove stopped containers:
```bash
docker container prune -f
```

#### Remove unused volumes (⚠️ Be careful - only if you're sure):
```bash
# List volumes first to see what will be deleted
docker volume ls

# Remove unused volumes
docker volume prune -f
```

#### Remove unused networks:
```bash
docker network prune -f
```

#### Clean everything at once (⚠️ Use with caution):
```bash
# This will remove:
# - All stopped containers
# - All networks not used by at least one container
# - All dangling images
# - All build cache
docker system prune -a -f --volumes
```

### Step 4: Clean CapRover Build Cache

CapRover stores build cache that can accumulate over time:

```bash
# Find CapRover data directory
docker ps | grep captain

# Clean CapRover build cache (you may need to adjust path)
# CapRover typically stores data in /captain
du -sh /captain

# Check for old build files
du -sh /captain/apps/*/builds/*
```

### Step 5: Clean Old Logs (if needed)

```bash
# Check log sizes
journalctl --disk-usage

# Clean logs older than 7 days
journalctl --vacuum-time=7d

# Or limit log size to 500MB
journalctl --vacuum-size=500M
```

### Step 6: Check for Large Files

```bash
# Find large files (top 20 largest files/directories)
du -h / | sort -rh | head -20

# Or check specific directories
du -sh /var/* | sort -rh | head -10
du -sh /opt/* | sort -rh | head -10
```

### Step 7: Verify Space is Freed

```bash
# Check disk usage again
df -h

# Check Docker disk usage
docker system df
```

### Step 8: Retry Deployment

Once you've freed up space, you can retry the deployment either:
- Push a new commit to trigger the GitHub Actions workflow
- Or manually trigger the workflow from GitHub Actions page

## Prevention Tips

1. **Regular Cleanup**: Set up a cron job to clean Docker resources weekly:
   ```bash
   # Add to crontab (crontab -e)
   0 2 * * 0 docker system prune -a -f --volumes
   ```

2. **Monitor Disk Usage**: Set up alerts when disk usage exceeds 80%

3. **Use .dockerignore**: Ensure your Dockerfile excludes unnecessary files

4. **Multi-stage Builds**: Already using these, which helps reduce image size

5. **Limit Build Cache**: CapRover builds can accumulate - clean old builds periodically

## Quick Fix Command (Run on VPS)

If you're in a hurry, run this single command (be careful - it removes ALL unused Docker resources):

```bash
docker system prune -a -f --volumes && docker image prune -a -f
```

Then check:
```bash
df -h
```

## Contact

If you continue to have issues, you may need to:
- Increase your VPS disk size
- Move Docker data to a larger partition
- Consider using an external storage solution







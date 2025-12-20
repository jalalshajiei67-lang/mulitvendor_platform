# Low Memory Build Fix for 2GB RAM VPS

## Problem
The Nuxt.js build process is failing with "JavaScript heap out of memory" errors on a 2GB RAM VPS.

## Solution Applied

### 1. Memory Optimizations in Dockerfile
- Reduced Node.js heap size from 2048MB to 1024MB
- Added npm install optimizations (`--prefer-offline --no-audit --no-fund`)
- Split npm operations into separate steps to free memory
- Disabled source maps in production builds
- Switched from terser to esbuild for minification (more memory efficient)
- Disabled devtools in production

### 2. Build Script Optimizations
- Added `build:low-memory` script with explicit memory limit
- Configured Vite to use esbuild instead of terser
- Disabled source maps to reduce memory usage

## Required: Add Swap Space on VPS

Even with these optimizations, a 2GB RAM VPS may still struggle. **You MUST add swap space** to your VPS.

### Steps to Add 2GB Swap Space

1. **SSH into your VPS:**
   ```bash
   ssh root@185.208.172.76
   ```

2. **Check current swap:**
   ```bash
   free -h
   swapon --show
   ```

3. **Create swap file (2GB):**
   ```bash
   sudo fallocate -l 2G /swapfile
   # Or if fallocate doesn't work:
   # sudo dd if=/dev/zero of=/swapfile bs=1024 count=2097152
   ```

4. **Set correct permissions:**
   ```bash
   sudo chmod 600 /swapfile
   ```

5. **Format as swap:**
   ```bash
   sudo mkswap /swapfile
   ```

6. **Enable swap:**
   ```bash
   sudo swapon /swapfile
   ```

7. **Make it permanent (add to /etc/fstab):**
   ```bash
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```

8. **Verify swap is active:**
   ```bash
   free -h
   swapon --show
   ```

9. **Optional: Adjust swappiness (how aggressively to use swap):**
   ```bash
   # Check current value (default is usually 60)
   cat /proc/sys/vm/swappiness
   
   # Set to 10 (less aggressive, prefer RAM)
   sudo sysctl vm.swappiness=10
   
   # Make permanent
   echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
   ```

### Verify After Adding Swap

After adding swap, you should see output like:
```
              total        used        free      shared  buff/cache   available
Mem:           2.0G        500M        200M         50M        1.3G        1.2G
Swap:          2.0G          0B        2.0G
```

## Alternative: Build on CI/CD

If adding swap doesn't work or you prefer not to modify the VPS, you can:

1. **Build on GitHub Actions** (which has more memory)
2. **Push the built artifacts** to your VPS
3. **Skip the build step** in Docker

This would require modifying your deployment pipeline to build in CI/CD and only copy the `.output` directory to the VPS.

## Current Configuration

- **Build heap size:** 1024MB
- **Runtime heap size:** 1024MB
- **Minifier:** esbuild (memory efficient)
- **Source maps:** Disabled in production
- **Devtools:** Disabled in production

## Monitoring

After deployment, monitor memory usage:
```bash
# On VPS
docker stats
free -h
```

If you still see memory issues, consider:
- Further reducing heap size to 768MB
- Building on a machine with more RAM and copying artifacts
- Upgrading VPS to 4GB RAM


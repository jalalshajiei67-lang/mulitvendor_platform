# 🔧 Fix: Port 80 Already Allocated Error

## Problem
```
Error: Bind for 0.0.0.0:80 failed: port is already allocated
```

This happens because **production and staging both use ports 80/443**, and they cannot run simultaneously.

## Solution Options

### Option 1: Stop Production, Run Staging (Recommended)

If you want to test staging, stop production first:

```bash
# Stop production
cd /path/to/project
docker-compose down

# Start staging
docker-compose -f docker-compose.staging.yml up -d --build
```

### Option 2: Run Both Simultaneously (Different Ports)

If you need both running at the same time, staging needs different ports. However, this breaks the "mirror production" requirement.

**To use different ports for staging**, modify `docker-compose.staging.yml`:

```yaml
traefik:
  ports:
    - "8080:80"    # Changed from 80:80
    - "8443:443"   # Changed from 443:443
```

But then you'd need to access staging via:
- `http://staging.indexo.ir:8080` (not standard)
- Or configure a reverse proxy

**This is NOT recommended** as it breaks standard HTTPS routing.

## Recommended Approach

**Stop production when testing staging:**

```bash
# 1. Stop production
docker-compose down

# 2. Clean up any leftover containers
docker ps -a | grep multivendor | grep -v staging | awk '{print $1}' | xargs docker rm -f

# 3. Start staging
docker-compose -f docker-compose.staging.yml up -d --build

# 4. Check logs
docker-compose -f docker-compose.staging.yml logs -f
```

## When You're Done Testing Staging

```bash
# Stop staging
docker-compose -f docker-compose.staging.yml down

# Start production again
docker-compose up -d
```


# Staging Data Loss & Connection Issues - Root Cause Analysis

## 🔍 Problems Identified

### Problem 1: Container Name Mismatch ⚠️ **CRITICAL**

**Issue:**
- `docker-compose.staging.yml` defines: `container_name: indexo_db_staging`
- Deployment script tries to stop: `multivendor_db_staging`
- Actual running container: `multivendor_db_staging` (from your `docker ps`)

**Why this causes data loss:**
1. Deployment script can't find `indexo_db_staging` to stop it
2. Old container keeps running with old volume
3. New container `indexo_db_staging` is created with **NEW empty volume**
4. Result: Data is in old container, but backend connects to new empty container

**Evidence:**
```bash
# Your docker ps shows:
multivendor_db_staging  # ← Old container (has data)
# But compose file creates:
indexo_db_staging       # ← New container (empty)
```

### Problem 2: Network Isolation 🔌

**Issue:**
- Database is on: `internal_staging` network only
- Backend is on: `docker-deploy_multivendor_network` AND `internal_staging`
- Backend uses: `DB_HOST=db` (service name)

**Why connection is lost:**
- If containers are on different networks, they can't communicate
- Service name `db` only works within the same Docker Compose network
- When containers restart, network membership might change

**Current config:**
```yaml
db:
  networks:
    - internal_staging  # ← Only on internal network

backend:
  networks:
    - docker-deploy_multivendor_network  # ← Different network
    - internal_staging  # ← Should work, but...
```

### Problem 3: Missing Health Checks & Dependencies ⏱️

**Issue:**
- Backend starts immediately and runs migrations
- No `depends_on` with health check
- Database might not be ready when backend tries to connect

**Current backend command:**
```yaml
command: sh -c "python manage.py migrate && gunicorn ..."
# ↑ Runs immediately, no wait for database
```

### Problem 4: Volume Naming Inconsistency 📦

**Issue:**
- Volume name: `postgres_data_staging`
- But Docker Compose creates volumes with project prefix: `indexo-staging_postgres_data_staging`
- If project name changes, new volume is created

**Why data doesn't persist:**
- Each deployment might use different project name
- New volume = fresh database
- Old volume with data is orphaned

## 🔧 Root Causes Summary

1. **Container name mismatch** → Old container not stopped → New empty container created
2. **Network issues** → Backend can't reach database
3. **No startup ordering** → Backend starts before database is ready
4. **Volume naming** → New volumes created instead of reusing existing

## ✅ Solutions

### Fix 1: Standardize Container Names

**Update `docker-compose.staging.yml`:**
```yaml
services:
  db:
    container_name: multivendor_db_staging  # ← Match deployment script
    # ... rest of config
```

**OR update deployment script:**
```yaml
# In deploy-staging.yml, change line 69:
docker stop indexo_db_staging ...  # ← Match compose file
```

### Fix 2: Fix Network Configuration

**Ensure database and backend are on same network:**
```yaml
db:
  networks:
    - internal_staging  # ← Keep this

backend:
  networks:
    - internal_staging  # ← Must be on same network as db
    - docker-deploy_multivendor_network  # ← For external access
```

### Fix 3: Add Health Checks & Dependencies

**Add to `docker-compose.staging.yml`:**
```yaml
db:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 5s
    timeout: 3s
    retries: 5

backend:
  depends_on:
    db:
      condition: service_healthy  # ← Wait for database to be ready
```

### Fix 4: Use Explicit Volume Names

**Ensure consistent volume naming:**
```yaml
volumes:
  postgres_data_staging:
    name: postgres_data_staging  # ← Explicit name, not project-prefixed
```

## 🎯 Recommended Fix

Update `docker-compose.staging.yml` to match what's actually running:

```yaml
services:
  db:
    container_name: multivendor_db_staging  # ← Match running container
    image: postgres:15-alpine
    volumes:
      - postgres_data_staging:/var/lib/postgresql/data
    networks:
      - internal_staging
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: always

  backend:
    container_name: multivendor_backend_staging
    depends_on:
      db:
        condition: service_healthy
    networks:
      - internal_staging  # ← Same network as db
      - docker-deploy_multivendor_network
    # ... rest of config

volumes:
  postgres_data_staging:
    name: postgres_data_staging  # ← Explicit name
```

## 🔄 Why Data "Automatically Binds"

**What's happening:**
1. First deployment: Creates `multivendor_db_staging` container + volume
2. Data is stored in volume: `indexo-staging_postgres_data_staging`
3. Second deployment: 
   - Tries to stop `multivendor_db_staging` (might fail)
   - Creates new container (maybe with different name)
   - **New container gets NEW volume** (because name doesn't match)
4. Result: Old data is in old volume, new container has empty volume

**The "binding" is actually:**
- Docker Compose matching volume name to container
- If container name changes → new volume is created
- Old volume becomes orphaned (data still there, but unused)

## 🔌 Why Connection is Lost

**Timing issues:**
1. Backend starts immediately
2. Database might still be initializing
3. Backend tries to connect → fails
4. Backend crashes or gives up

**Network issues:**
1. Containers on different networks can't communicate
2. Service name `db` only resolves within same network
3. If network membership changes → connection fails

## 📊 Current State

Based on your `docker ps` output:
- ✅ `multivendor_db_staging` is running (has data)
- ✅ `multivendor_backend_staging` is running
- ❌ But they might be on different networks
- ❌ Backend might be connecting to wrong database
- ❌ Or database might be empty (fresh volume)

## 🧪 Diagnostic Commands

Run these to diagnose:

```bash
# 1. Check which network database is on
docker inspect multivendor_db_staging | grep -A 10 Networks

# 2. Check which network backend is on
docker inspect multivendor_backend_staging | grep -A 10 Networks

# 3. Check if backend can reach database
docker exec multivendor_backend_staging ping -c 2 db

# 4. Check database volume
docker volume inspect indexo-staging_postgres_data_staging

# 5. Check backend environment
docker exec multivendor_backend_staging env | grep DB_
```

## 🎯 Quick Fix (Immediate)

To fix right now without changing code:

```bash
# 1. Stop everything
docker compose -f docker-compose.staging.yml down

# 2. Find the actual volume with data
docker volume ls | grep postgres

# 3. Update docker-compose.staging.yml to use correct container names
# (Match what's in your docker ps output)

# 4. Restart
docker compose -f docker-compose.staging.yml up -d
```


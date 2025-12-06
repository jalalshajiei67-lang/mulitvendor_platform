# ✅ Simple Staging Deployment (Traefik-Based)

## 🎯 The Right Way: Use Existing Traefik

Since you already have **Traefik** in production, we use it for staging too! No nginx needed.

## 🚀 Deployment (CI/CD Ready)

### Step 1: Ensure Traefik Network Exists

**Option A: Start Production First (Recommended)**
```bash
docker-compose up -d
```

**Option B: Create Network Manually**
```bash
./ensure-traefik-network.sh
# OR
docker network create multivendor_network --driver bridge
```

### Step 2: Start Staging
```bash
docker-compose -f docker-compose.staging.yml up -d --build
```

**That's it!** Traefik automatically:
- Discovers staging services
- Gets SSL certificates for staging domains
- Routes traffic based on domain names

## 📋 How It Works

1. **Production Traefik** (ports 80/443) handles all domains
2. **Staging services** connect to production's Traefik network
3. **Traefik routes** based on Host header:
   - `indexo.ir` → Production
   - `staging.indexo.ir` → Staging

## ✅ Benefits

- ✅ No nginx setup needed
- ✅ No port conflicts
- ✅ Automatic SSL certificates
- ✅ CI/CD ready (just docker-compose commands)
- ✅ Both run simultaneously

## 📝 CI/CD Example

```yaml
# GitHub Actions / GitLab CI
- name: Deploy Production
  run: docker-compose up -d --build

- name: Deploy Staging  
  run: docker-compose -f docker-compose.staging.yml up -d --build
```

See `TRAEFIK_DUAL_DEPLOYMENT.md` for complete details.


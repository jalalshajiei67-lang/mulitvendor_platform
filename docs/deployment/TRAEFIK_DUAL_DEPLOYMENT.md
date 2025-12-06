# 🚀 Traefik-Based Dual Deployment (No Nginx Needed!)

## ✅ Perfect Solution: Single Traefik for Both Production + Staging

You're absolutely right! Since you already have **Traefik**, we don't need nginx at all. Traefik can handle **both production and staging** domains simultaneously.

## 🎯 How It Works

```
Single Traefik (ports 80/443)
    ↓
Routes based on Host header:
    ├─ indexo.ir → Production services
    ├─ api.indexo.ir → Production backend
    ├─ staging.indexo.ir → Staging frontend
    └─ api.staging.indexo.ir → Staging backend
```

## 📋 Architecture

1. **Production Traefik** (from `docker-compose.yml`):
   - Listens on ports 80/443
   - Handles SSL certificates automatically
   - Routes `indexo.ir` and `api.indexo.ir` to production services

2. **Staging Services** (from `docker-compose.staging.yml`):
   - Connect to **production's Traefik network** (`multivendor_network`)
   - Have Traefik labels for `staging.indexo.ir` domains
   - Traefik automatically discovers and routes them

3. **No Nginx Needed!** ✅
   - Traefik handles everything
   - SSL certificates managed by Traefik
   - Single point of entry

## 🚀 Deployment (CI/CD Ready!)

### Step 1: Ensure Traefik Network Exists

**Option A: Start Production First (Recommended)**
```bash
docker-compose up -d
```
This creates the `multivendor_network` that staging will use.

**Option B: Create Network Manually (if production not running)**
```bash
./ensure-traefik-network.sh
```
Or manually:
```bash
docker network create multivendor_network --driver bridge
```

### Step 2: Start Staging

```bash
docker-compose -f docker-compose.staging.yml up -d --build
```

That's it! Traefik automatically discovers staging services and routes them.

## 🔧 Key Changes

1. **Removed staging Traefik** - We use production's Traefik
2. **Staging services connect to production network** - `multivendor_network` (external)
3. **Traefik labels** - Staging services have labels for `staging.indexo.ir` domains
4. **No nginx** - Traefik handles everything

## 📝 CI/CD Integration

Your CI/CD should:

```yaml
# Step 1: Ensure Traefik network exists
- name: Ensure Traefik network
  run: |
    docker network create multivendor_network --driver bridge || true

# Step 2: Deploy Production (if needed)
- name: Deploy Production
  run: docker-compose up -d --build

# Step 3: Deploy Staging
- name: Deploy Staging
  run: docker-compose -f docker-compose.staging.yml up -d --build
```

**Or use the helper script:**
```yaml
- name: Deploy Staging
  run: ./deploy-staging.sh
```

**No special setup needed!** Traefik automatically:
- Discovers new services
- Gets SSL certificates for staging domains
- Routes traffic correctly

## 🌐 Domain Routing

| Domain | Route | Service |
|--------|-------|---------|
| `indexo.ir` | → Production Frontend | `multivendor_frontend` |
| `api.indexo.ir` | → Production Backend | `multivendor_backend` |
| `staging.indexo.ir` | → Staging Frontend | `multivendor_frontend_staging` |
| `api.staging.indexo.ir` | → Staging Backend | `multivendor_backend_staging` |

## ✅ Benefits

- ✅ **No nginx setup** - Traefik handles everything
- ✅ **No port conflicts** - Single Traefik on 80/443
- ✅ **Automatic SSL** - Traefik gets certificates for staging domains
- ✅ **CI/CD ready** - Just run docker-compose commands
- ✅ **Simple** - No host-level configuration needed
- ✅ **Both run simultaneously** - Zero downtime

## 🧪 Testing

```bash
# Check production
curl -I https://indexo.ir
curl -I https://api.indexo.ir/api/

# Check staging
curl -I https://staging.indexo.ir
curl -I https://api.staging.indexo.ir/api/
```

## ⚠️ Important Notes

1. **Production must be running first** - It creates the `multivendor_network` that staging uses
2. **DNS** - Make sure `staging.indexo.ir` and `api.staging.indexo.ir` point to your VPS
3. **SSL Certificates** - Traefik will automatically request Let's Encrypt certificates for staging domains on first access
4. **Network** - Staging services are on both networks:
   - `multivendor_network_staging` - For internal communication (db, redis)
   - `multivendor_network` - For Traefik routing

## 🐛 Troubleshooting

### Staging not accessible

1. **Check production Traefik is running**:
   ```bash
   docker-compose ps traefik
   ```

2. **Check staging services are on Traefik network**:
   ```bash
   docker network inspect multivendor_network | grep staging
   ```

3. **Check Traefik logs**:
   ```bash
   docker-compose logs traefik | grep staging
   ```

4. **Verify Traefik discovered staging services**:
   ```bash
   docker exec traefik wget -qO- http://localhost:8080/api/http/routers | grep staging
   ```

---

**That's it!** Much simpler than nginx setup. Just deploy via CI/CD and Traefik handles the rest! 🎉


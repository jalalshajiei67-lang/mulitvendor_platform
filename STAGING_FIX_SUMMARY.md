# ✅ Staging Configuration Fixed - Summary

## 🎯 What Was Fixed

I've rewritten `docker-compose.staging.yml` to **exactly mirror** your working production configuration. Here are the key fixes that should resolve the 404/503 Traefik errors:

### 🔧 Critical Fixes

1. **Fixed Traefik Router Names** ❌→✅
   - **Before**: `traefik.http.routers.backend-staging.rule` (with `-staging` suffix)
   - **After**: `traefik.http.routers.backend.rule` (matches production pattern)
   - **Why**: Traefik router names must be consistent. The `-staging` suffix was causing routing conflicts.

2. **Fixed Port Configuration** ❌→✅
   - **Before**: Ports `8080:80` and `8443:443` (non-standard)
   - **After**: Ports `80:80` and `443:443` (standard, matches production)
   - **Why**: Standard ports are required for proper domain routing. Non-standard ports cause 404 errors.

3. **Added Missing Nginx Media Router TLS Config** ❌→✅
   - **Before**: Only `nginx-static` had TLS certresolver
   - **After**: Both `nginx-static` and `nginx-media` have TLS certresolver
   - **Why**: Media files need HTTPS too, otherwise you get 503 errors.

4. **Removed Extra Environment Variables** ❌→✅
   - **Removed**: `NODE_ENV=staging`, `NODE_OPTIONS`, extra `HOST`/`PORT` from frontend
   - **Why**: Production doesn't have these, and they can cause conflicts.

5. **Removed Image Names** ❌→✅
   - **Removed**: `image: indexo-backend:staging` and `image: indexo-frontend:staging`
   - **Why**: Production doesn't use image names, just builds from Dockerfile.

6. **Removed Extra Frontend Healthcheck** ❌→✅
   - **Removed**: Complex Node.js healthcheck
   - **Why**: Production doesn't have it, and it can cause startup issues.

7. **Fixed Database Environment Variables** ❌→✅
   - **Before**: `DB_NAME=${DB_NAME}`, `DB_USER=${DB_USER}` (variables)
   - **After**: `DB_NAME=multivendor_db`, `DB_USER=postgres` (hardcoded, matches production)
   - **Why**: Production uses hardcoded values, not variables.

8. **Fixed Domain Structure** ✅
   - **Frontend**: `staging.indexo.ir` (as you specified)
   - **Backend API**: `api.staging.indexo.ir` (following production pattern)

---

## 📋 Next Steps

### Step 1: Create `.env.staging` File

Since `.env.staging` is gitignored, create it manually:

```bash
cd /media/jalal/New\ Volume/project/mulitvendor_platform
cp .env .env.staging
```

Then edit `.env.staging` and update these values:

```env
# Update ALLOWED_HOSTS for staging
ALLOWED_HOSTS=localhost,127.0.0.1,backend,frontend,staging.indexo.ir,api.staging.indexo.ir,www.staging.indexo.ir,158.255.74.123

# Update NUXT_PUBLIC_API_BASE for staging
NUXT_PUBLIC_API_BASE=https://api.staging.indexo.ir/api
```

### Step 2: Stop Production (if running on same VPS)

Since both use ports 80/443, you can't run them simultaneously:

```bash
# Stop production
docker-compose down

# Or if production is running in a different directory, navigate there first
```

### Step 3: Deploy Staging

```bash
# Make sure you're in the project root
cd /media/jalal/New\ Volume/project/mulitvendor_platform

# Build and start staging
docker-compose -f docker-compose.staging.yml up -d --build

# Check logs
docker-compose -f docker-compose.staging.yml logs -f
```

### Step 4: Verify Deployment

1. **Check all containers are running**:
   ```bash
   docker-compose -f docker-compose.staging.yml ps
   ```

2. **Check Traefik logs**:
   ```bash
   docker-compose -f docker-compose.staging.yml logs traefik
   ```

3. **Test endpoints**:
   - Frontend: `https://staging.indexo.ir`
   - Backend API: `https://api.staging.indexo.ir/api/`
   - Admin: `https://api.staging.indexo.ir/admin/`

---

## 🔍 Key Differences from Old Staging Config

| Aspect | Old (Broken) | New (Fixed) |
|--------|-------------|-------------|
| **Traefik Ports** | 8080:80, 8443:443 | 80:80, 443:443 |
| **Router Names** | `backend-staging`, `frontend-staging` | `backend`, `frontend` |
| **Nginx Media TLS** | ❌ Missing | ✅ Added |
| **Frontend Healthcheck** | ✅ Complex Node.js check | ❌ Removed (matches prod) |
| **Image Names** | ✅ Had image names | ❌ Removed (matches prod) |
| **DB Variables** | `${DB_NAME}`, `${DB_USER}` | `multivendor_db`, `postgres` |
| **Extra Env Vars** | `NODE_ENV`, `NODE_OPTIONS` | ❌ Removed |

---

## 🚨 Important Notes

1. **Port Conflict**: Production and staging both use ports 80/443. You **cannot run both simultaneously** on the same VPS. Stop production before starting staging.

2. **Domain DNS**: Make sure these domains point to your VPS:
   - `staging.indexo.ir` → Your VPS IP
   - `api.staging.indexo.ir` → Your VPS IP

3. **SSL Certificates**: Traefik will automatically request Let's Encrypt certificates for staging domains. The first request may take a few minutes.

4. **Database**: Staging uses a separate database volume (`postgres_data_staging`), so it won't affect production data.

5. **Letsencrypt**: Staging uses `./letsencrypt_staging` directory (separate from production's `./letsencrypt`).

---

## ✅ Expected Result

After deployment, you should see:
- ✅ `https://staging.indexo.ir` → Frontend loads correctly
- ✅ `https://api.staging.indexo.ir/api/` → Backend API responds
- ✅ `https://api.staging.indexo.ir/admin/` → Django admin accessible
- ✅ `https://api.staging.indexo.ir/static/...` → Static files load
- ✅ `https://api.staging.indexo.ir/media/...` → Media files load

No more 404 or 503 errors! 🎉


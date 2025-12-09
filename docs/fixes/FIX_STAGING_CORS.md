# Fix CORS Error for Staging Deployment

## 🔴 Problem

After deployment, you're getting CORS errors:
```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at https://api-staging.indexo.ir/api/products/slug/test/. (Reason: CORS request did not succeed).
```

## 🔍 Root Cause

The backend at `api-staging.indexo.ir` is not configured to allow requests from your frontend domain. The `CORS_ALLOWED_ORIGINS` environment variable in your Docker Compose deployment is either:
1. Not set in `.env.staging` file
2. Missing the frontend domain
3. Set incorrectly
4. Not being passed to the Docker container correctly

## ✅ Solution

### Step 1: Identify Your Frontend Domain

Your frontend is at: `https://staging.indexo.ir` (based on your deployment configuration)

### Step 2: Update `.env.staging` File on Your VPS

SSH into your VPS and update the `.env.staging` file:

```bash
ssh root@your-vps-ip
cd /root/indexo-staging
nano .env.staging
```

Make sure these variables are set correctly:

```env
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir,https://api-staging.indexo.ir
CORS_ALLOW_CREDENTIALS=True
CSRF_TRUSTED_ORIGINS=https://staging.indexo.ir,https://api-staging.indexo.ir
ALLOWED_HOSTS=localhost,127.0.0.1,backend,staging.indexo.ir,api-staging.indexo.ir
```

**Important Notes:**
- No spaces between origins in the comma-separated list
- Include the `https://` protocol
- Make sure there are no trailing spaces

### Step 3: Verify Docker Compose Configuration

Check that `docker-compose.staging.yml` is reading environment variables from `.env` file. The workflow automatically copies `.env.staging` to `.env`, but verify the backend service is using them:

```yaml
backend:
  environment:
    - CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}
    - CORS_ALLOW_ALL_ORIGINS=${CORS_ALLOW_ALL_ORIGINS}
    # ... other env vars
```

Or if using `env_file`:
```yaml
backend:
  env_file:
    - .env
```

### Step 4: Restart Docker Containers

After updating `.env.staging`, restart the containers:

```bash
cd /root/indexo-staging
cp .env.staging .env
docker compose -f docker-compose.staging.yml down
docker compose -f docker-compose.staging.yml up -d --build
```

### Step 5: Verify Environment Variables in Container

Check if the environment variables are actually set in the running container:

```bash
docker exec multivendor_backend_staging printenv | grep CORS
```

You should see:
```
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir,https://api-staging.indexo.ir
CORS_ALLOW_CREDENTIALS=True
```

### Step 6: Test

1. Open your frontend in a browser: `https://staging.indexo.ir`
2. Open browser DevTools (F12) → Console tab
3. Try to access a product page
4. Check if CORS errors are gone

## 🔧 Complete `.env.staging` File Template

Here's a complete `.env.staging` file with all necessary variables:

```env
# Database
DB_NAME=multivendor_db_staging
DB_USER=postgres
DB_PASSWORD=MySecurePassword123!
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=False

# Security & CORS
ALLOWED_HOSTS=localhost,127.0.0.1,backend,staging.indexo.ir,api-staging.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir,https://api-staging.indexo.ir
CORS_ALLOW_CREDENTIALS=True
CSRF_TRUSTED_ORIGINS=https://staging.indexo.ir,https://api-staging.indexo.ir

# Domains
MAIN_DOMAIN=staging.indexo.ir
API_DOMAIN=api-staging.indexo.ir

# Frontend
NODE_ENV=production
NUXT_HOST=0.0.0.0
NUXT_PORT=3000
NUXT_PUBLIC_API_BASE=https://api-staging.indexo.ir/api
```

## 🐛 Troubleshooting

### Still Getting CORS Errors?

1. **Check environment variables in container:**
   ```bash
   docker exec multivendor_backend_staging printenv | grep CORS
   ```
   If variables are missing, check `docker-compose.staging.yml` configuration.

2. **Check backend logs:**
   ```bash
   docker logs multivendor_backend_staging --tail 100
   ```
   Look for CORS-related errors or warnings.

3. **Check browser console:**
   - Look for the exact error message
   - Check the **Network** tab → Find the failed request
   - Look at the **Response Headers** - is `Access-Control-Allow-Origin` present?

4. **Verify `.env.staging` file exists and is correct:**
   ```bash
   cat /root/indexo-staging/.env.staging | grep CORS
   ```

5. **Test with curl:**
   ```bash
   curl -H "Origin: https://staging.indexo.ir" \
        -H "Access-Control-Request-Method: GET" \
        -H "Access-Control-Request-Headers: content-type" \
        -X OPTIONS \
        https://api-staging.indexo.ir/api/products/slug/test/ \
        -v
   ```
   Look for `Access-Control-Allow-Origin: https://staging.indexo.ir` in the response headers.

6. **Check if `.env` file is being used:**
   ```bash
   cd /root/indexo-staging
   ls -la .env .env.staging
   ```
   The workflow should copy `.env.staging` to `.env` automatically.

5. **Test with curl:**
   ```bash
   curl -H "Origin: https://staging.indexo.ir" \
        -H "Access-Control-Request-Method: GET" \
        -H "Access-Control-Request-Headers: content-type" \
        -X OPTIONS \
        https://api-staging.indexo.ir/api/products/slug/test/ \
        -v
   ```
   Look for `Access-Control-Allow-Origin: https://staging.indexo.ir` in the response headers.

### Common Mistakes

❌ **Wrong:** `CORS_ALLOWED_ORIGINS=https://staging.indexo.ir , https://api-staging.indexo.ir` (spaces)
✅ **Correct:** `CORS_ALLOWED_ORIGINS=https://staging.indexo.ir,https://api-staging.indexo.ir` (no spaces)

❌ **Wrong:** `CORS_ALLOWED_ORIGINS=staging.indexo.ir` (missing protocol)
✅ **Correct:** `CORS_ALLOWED_ORIGINS=https://staging.indexo.ir` (with protocol)

❌ **Wrong:** `CORS_ALLOW_ALL_ORIGINS=True` (security risk, and might conflict)
✅ **Correct:** `CORS_ALLOW_ALL_ORIGINS=False` (with specific origins)

### Quick Fix via GitHub Actions

If you want to update the `.env.staging` file automatically via the deployment workflow, the workflow already sets these values (see `.github/workflows/deploy-staging.yml` line 52). However, if the file already exists, it won't be overwritten.

To force an update, you can:

1. **Option A: Delete `.env.staging` on the server** (workflow will recreate it):
   ```bash
   ssh root@your-vps-ip
   rm /root/indexo-staging/.env.staging
   ```
   Then push to `staging` branch to trigger deployment.

2. **Option B: Manually update on server** (as described in Step 2 above)

3. **Option C: Update the workflow** to always overwrite CORS settings (not recommended if you have other custom settings)

## 📝 Notes

- The CORS configuration was improved in the code to handle edge cases better
- The middleware is correctly positioned at the top of the middleware stack
- Preflight requests (OPTIONS) are now cached for 1 hour to improve performance
- Additional headers are exposed for frontend use
- Docker Compose reads `.env.staging` file automatically via `env_file` directive
- The backend service explicitly passes CORS variables in the `environment` section

---

**Last Updated:** 2025-12-09
**Deployment Method:** Docker Compose
**Status:** Ready to apply


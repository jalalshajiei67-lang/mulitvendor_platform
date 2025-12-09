# Fix Staging CORS Errors

## 🔴 Problem

Frontend at `https://staging.indexo.ir` is getting CORS errors when trying to access `https://api-staging.indexo.ir/api/...`:

```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at https://api-staging.indexo.ir/api/...
(Reason: CORS request did not succeed). Status code: (null).
```

## ✅ Solution

### Step 1: Verify Environment Variables

Check your `.env.staging` file or environment variables in docker-compose. Make sure these are set:

```env
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True
```

**Important**: `CORS_ALLOWED_ORIGINS` should include the **frontend domain** (`https://staging.indexo.ir`), not the backend API domain.

### Step 2: Check Current CORS Configuration

Run this command in your backend container:

```bash
docker exec multivendor_backend_staging python manage.py check_cors
```

This will show you the current CORS configuration.

### Step 3: Update .env.staging File

If you're using a `.env.staging` file, make sure it includes:

```env
# CORS Configuration
CORS_ALLOWED_ORIGINS=https://staging.indexo.ir
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True

# Other required variables
ALLOWED_HOSTS=localhost,127.0.0.1,backend,staging.indexo.ir,api-staging.indexo.ir
CSRF_TRUSTED_ORIGINS=https://staging.indexo.ir,https://api-staging.indexo.ir
```

### Step 4: Restart Backend Container

After updating environment variables:

```bash
docker-compose -f docker-compose.staging.yml restart backend
```

Or rebuild:

```bash
docker-compose -f docker-compose.staging.yml up -d --build backend
```

### Step 5: Test CORS

Test the CORS configuration:

```bash
# Test preflight OPTIONS request
curl -X OPTIONS https://api-staging.indexo.ir/api/categories/ \
  -H "Origin: https://staging.indexo.ir" \
  -H "Access-Control-Request-Method: GET" \
  -v
```

You should see:
- Status: `200 OK`
- Headers include: `Access-Control-Allow-Origin: https://staging.indexo.ir`

## 🔍 Troubleshooting

### If CORS still doesn't work:

1. **Check if CORS middleware is enabled**:
   - CORS middleware should be at the **top** of `MIDDLEWARE` list in `settings.py`
   - It should be: `'corsheaders.middleware.CorsMiddleware'`

2. **Check backend logs**:
   ```bash
   docker logs multivendor_backend_staging --tail 100
   ```
   Look for any CORS-related errors.

3. **Temporarily enable CORS_ALLOW_ALL_ORIGINS** (for testing only):
   ```env
   CORS_ALLOW_ALL_ORIGINS=True
   ```
   **⚠️ Remember to disable this after testing!**

4. **Verify the frontend is using the correct API URL**:
   - Frontend should be calling `https://api-staging.indexo.ir/api/...`
   - Check `NUXT_PUBLIC_API_BASE` environment variable in frontend

## 📋 Quick Fix Command

If you need to quickly fix CORS for staging, you can set it in docker-compose.staging.yml:

```yaml
environment:
  - CORS_ALLOWED_ORIGINS=https://staging.indexo.ir
  - CORS_ALLOW_ALL_ORIGINS=False
  - CORS_ALLOW_CREDENTIALS=True
```

Then restart:
```bash
docker-compose -f docker-compose.staging.yml up -d --force-recreate backend
```


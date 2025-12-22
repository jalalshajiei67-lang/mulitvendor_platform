# 🚀 Deploy SSR API Fix

## ✅ Problem Solved

The frontend was getting 404 errors during **server-side rendering (SSR)** because:
- Frontend container tried to reach `https://api.indexo.ir` from inside Docker
- This caused network/SSL issues during SSR
- Client-side requests worked fine (browser → api.indexo.ir)

## 🔧 Solution Applied

Updated the code to:
1. **Client-side**: Use `https://api.indexo.ir/api` (external URL)
2. **Server-side (SSR)**: Use `http://multivendor_backend:8000/api` (internal Docker network)

## 📝 Changes Made

### 1. Updated `useApiFetch.ts`
- Detects server-side rendering
- Uses internal Docker hostname for SSR requests
- Uses external URL for client-side requests

### 2. Updated `docker-compose.production.yml`
- Added `NUXT_API_BASE=http://multivendor_backend:8000/api` environment variable
- This is used for SSR (not exposed to client)

## 🚀 Deployment Steps

### Step 1: Transfer Updated Files to VPS

```bash
# From your local machine
scp multivendor_platform/front_end/nuxt/composables/useApiFetch.ts root@91.107.172.234:/root/indexo-production/multivendor_platform/front_end/nuxt/composables/
scp docker-compose.production.yml root@91.107.172.234:/root/indexo-production/
```

### Step 2: Rebuild Frontend Container

```bash
# SSH to VPS
ssh root@91.107.172.234
cd /root/indexo-production

# Rebuild frontend with new code
docker-compose build --no-cache frontend

# Restart frontend
docker-compose up -d frontend

# Check logs
docker-compose logs -f frontend
```

### Step 3: Verify Fix

```bash
# Check frontend logs for errors
docker logs multivendor_frontend --tail 50 | grep -i "error\|404\|categories"

# Should see no more 404 errors for categories
```

### Step 4: Test in Browser

1. Open `https://indexo.ir` in browser
2. Open browser console (F12)
3. Check Network tab - should see successful API calls
4. No more "Error fetching categories for filters" errors

## 🔍 Verification

After deployment, verify:

1. **Frontend logs are clean:**
   ```bash
   docker logs multivendor_frontend --tail 100 | grep -i "error\|404"
   ```
   Should show no errors related to categories API.

2. **Backend is receiving requests:**
   ```bash
   docker logs multivendor_backend --tail 50 | grep "categories"
   ```
   Should show successful requests.

3. **Browser console is clean:**
   - Open `https://indexo.ir`
   - Check browser console (F12)
   - No 404 errors for `/api/categories/`

## 📋 Quick Deploy Command

All-in-one command:

```bash
# On VPS
cd /root/indexo-production && \
docker-compose build --no-cache frontend && \
docker-compose up -d frontend && \
docker-compose logs -f frontend
```

## 🎯 Expected Result

- ✅ No more 404 errors in frontend logs
- ✅ Categories load successfully on homepage
- ✅ SSR works correctly using internal Docker network
- ✅ Client-side requests still use external URL

## 🔄 If Issues Persist

1. **Check frontend can reach backend internally:**
   ```bash
   docker exec multivendor_frontend curl -s http://multivendor_backend:8000/api/categories/ | head -5
   ```
   Should return JSON data.

2. **Check environment variables:**
   ```bash
   docker exec multivendor_frontend env | grep NUXT
   ```
   Should show:
   - `NUXT_PUBLIC_API_BASE=https://api.indexo.ir/api`
   - `NUXT_API_BASE=http://multivendor_backend:8000/api`

3. **Restart all services:**
   ```bash
   docker-compose restart
   ```

## ✅ Success Indicators

- Frontend logs show no 404 errors
- Homepage loads categories successfully
- Browser console shows no API errors
- Network tab shows successful API calls


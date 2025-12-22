# Set API Domain to api.indexo.ir

## ✅ Quick Fix

You need to set `API_DOMAIN=api.indexo.ir` in your `.env` file.

### Step 1: Update .env File

Add or update these variables in your `.env` file (in project root):

```bash
API_DOMAIN=api.indexo.ir
MAIN_DOMAIN=indexo.ir
```

### Step 2: Rebuild Frontend Container

Since Nuxt embeds environment variables at build time, you need to rebuild:

```bash
# Stop containers
docker-compose -f docker-compose.production.yml down

# Rebuild frontend with new API_DOMAIN
docker-compose -f docker-compose.production.yml build --no-cache frontend

# Start all services
docker-compose -f docker-compose.production.yml up -d

# Check logs
docker-compose -f docker-compose.production.yml logs -f frontend
```

### Step 3: Verify

1. Check frontend logs - should show no API errors
2. Test in browser - open `https://indexo.ir`
3. Check browser console - API calls should go to `https://api.indexo.ir/api/`

## 📝 What Changed

- Updated `env.template` to include `API_DOMAIN=api.indexo.ir`
- Updated `imageUtils.ts` to use `api.indexo.ir` as fallback
- Docker compose files already use `${API_DOMAIN}` variable

## 🔍 Current Configuration

Your docker-compose.production.yml uses:
- `${API_DOMAIN}` for backend API URL
- `${MAIN_DOMAIN}` for frontend domain

So setting `API_DOMAIN=api.indexo.ir` in `.env` will make frontend use `https://api.indexo.ir/api/`


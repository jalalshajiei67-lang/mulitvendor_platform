# Environment Variables Configuration

This document lists all environment variables needed for deployment.

## 🎯 Backend Environment Variables (CapRover)

Set these in **CapRover → Apps → multivendor-backend → App Configs**

### Django Core Settings
```env
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-minimum-50-characters
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Database Configuration
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=<your-postgresql-password-from-caprover>
DB_HOST=srv-captain--postgres-db
DB_PORT=5432
```

### Redis Configuration (for Chat WebSocket)
```env
REDIS_HOST=srv-captain--multivendor-redis
REDIS_PORT=6379
REDIS_PASSWORD=<your-redis-password-from-caprover>
```

### Django Settings Module (CRITICAL)
```env
DJANGO_SETTINGS_MODULE=multivendor_platform.settings_caprover
```

### Security & CORS Settings
```env
ALLOWED_HOSTS=multivendor-backend.indexo.ir,indexo.ir,www.indexo.ir
CORS_ALLOWED_ORIGINS=https://multivendor-frontend.indexo.ir,https://indexo.ir,https://www.indexo.ir
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_ALL_ORIGINS=False
CSRF_TRUSTED_ORIGINS=https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir
USE_TLS=True
SITE_URL=https://indexo.ir
```

### Optional - OTP Settings
```env
OTP_SENDER_CLASS=users.services.otp_senders.LocalOTPSender
OTP_EXPIRATION_MINUTES=5
OTP_RATE_LIMIT_REQUESTS=3
OTP_RATE_LIMIT_WINDOW_MINUTES=15
```

---

## 🎨 Frontend Environment Variables (CapRover)

Set these in **CapRover → Apps → multivendor-frontend → App Configs**

```env
NODE_ENV=production
NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api
NUXT_PUBLIC_SITE_URL=https://indexo.ir
NUXT_HOST=0.0.0.0
NUXT_PORT=3000
```

---

## 🔐 GitHub Secrets

Set these in **GitHub → Settings → Secrets and variables → Actions**

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `CAPROVER_SERVER` | `https://captain.indexo.ir` | Your CapRover dashboard URL |
| `CAPROVER_PASSWORD` | `<your-password>` | CapRover dashboard password |
| `CAPROVER_BACKEND_APP_NAME` | `multivendor-backend` | Backend app name in CapRover |
| `CAPROVER_FRONTEND_APP_NAME` | `multivendor-frontend` | Frontend app name in CapRover |

**Note:** The workflow uses password-based authentication. App tokens are not required.

---

## 🏠 Local Development (docker-compose)

For local development with `docker-compose`, create a `.env` file in the project root:

```env
# Django
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
ALLOWED_HOSTS=localhost,127.0.0.1,backend
CORS_ALLOW_ALL_ORIGINS=True

# Nuxt
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
NODE_ENV=development
```

---

## ⚙️ Environment Variable Details

### Required Variables

**Must be set for chat system to work:**
- `REDIS_HOST` - Redis server for WebSocket channels
- `REDIS_PORT` - Redis port (default 6379)
- `DB_*` - Database connection (PostgreSQL recommended)
- `ALLOWED_HOSTS` - Domains that can access Django
- `CORS_ALLOWED_ORIGINS` - Frontend domains for API access

### Security Variables

**Critical for production:**
- `SECRET_KEY` - Must be long, random, and kept secret
- `DEBUG=False` - Never use DEBUG=True in production
- `USE_TLS=True` - When using HTTPS
- `CSRF_TRUSTED_ORIGINS` - Domains trusted for CSRF

### Optional Variables

**Can use defaults:**
- `OTP_*` - OTP/SMS configuration
- `SITE_URL` - For SEO and sitemaps

---

## 🧪 Testing Environment Variables

### Check Backend Variables
```bash
# In CapRover → Backend → Execute Command
python manage.py shell
>>> from django.conf import settings
>>> print(settings.REDIS_HOST)
>>> print(settings.DATABASES)
>>> print(settings.CHANNEL_LAYERS)
```

### Check Frontend Variables
```bash
# In CapRover → Frontend → Execute Command  
node -e "console.log(process.env.NUXT_PUBLIC_API_BASE)"
```

### Check Redis Connection
```bash
# In CapRover → Backend → Execute Command
python manage.py shell
>>> import redis
>>> r = redis.Redis(host='srv-captain--multivendor-redis', port=6379)
>>> r.ping()
True
```

---

## 🔍 Troubleshooting

### Variable Not Loading

**Problem:** Environment variable not being read

**Solutions:**
1. Check spelling matches exactly
2. Restart app after changing variables
3. Check CapRover logs for startup errors
4. Verify no typos in variable names

### Redis Connection Failed

**Problem:** `Error connecting to Redis`

**Check:**
- Redis app is running in CapRover
- `REDIS_HOST=srv-captain--multivendor-redis`
- `REDIS_PORT=6379`
- No extra spaces in values

### Database Connection Failed

**Problem:** `could not connect to database`

**Check:**
- PostgreSQL app is running
- `DB_HOST=srv-captain--multivendor-db`
- `DB_PORT=5432` (not 6379!)
- Password matches PostgreSQL setup
- Database name is `postgres` (default)

### CORS Errors

**Problem:** Frontend can't access API

**Check:**
- `CORS_ALLOWED_ORIGINS` includes frontend domain
- Use `https://` not `http://` in production
- No trailing slashes
- `CSRF_TRUSTED_ORIGINS` also includes frontend

---

## 📝 Best Practices

1. **Never commit `.env` files** - They contain secrets
2. **Use strong SECRET_KEY** - Generate with Django command
3. **Keep credentials secure** - Don't share or expose
4. **Different values for dev/prod** - Don't use dev settings in production
5. **Document all variables** - Update this file when adding new ones
6. **Test after changes** - Restart apps and verify functionality

---

## 🎯 Quick Reference

| Component | Where to Set | Priority |
|-----------|--------------|----------|
| Backend Django | CapRover App Configs | **Critical** |
| Frontend Nuxt | CapRover App Configs | **Critical** |
| GitHub Secrets | GitHub Settings | **Required for CI/CD** |
| Local Dev | `.env` file in root | Optional |

---

**Last Updated:** 2024-11-21  
**Version:** 1.0.0



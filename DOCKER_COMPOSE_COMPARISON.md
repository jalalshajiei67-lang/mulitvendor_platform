# Docker Compose: Production vs Staging Comparison

## Critical Differences That Could Cause Production Errors

### 1. **pgBouncer Connection Pooling** ⚠️ CRITICAL
**Staging:** ✅ Has pgbouncer service for connection pooling
**Production:** ❌ Missing pgbouncer - connects directly to PostgreSQL

**Impact:**
- Production may experience database connection exhaustion under load
- Staging handles connections more efficiently with pooling
- Production backend uses `DB_HOST=db` (direct connection)
- Staging backend uses `DB_HOST=pgbouncer` (pooled connection)

**Production Configuration:**
```yaml
backend:
  environment:
    - DB_HOST=db  # Direct connection
```

**Staging Configuration:**
```yaml
pgbouncer:
  # Connection pooling service
  
backend:
  environment:
    - DB_HOST=pgbouncer  # Pooled connection
  depends_on:
    pgbouncer:
      condition: service_healthy
```

---

### 2. **Traefik SSL Certificate Challenge Method**
**Staging:** Uses HTTP challenge (`httpchallenge=true`)
**Production:** Uses TLS challenge (`tlschallenge=true`)

**Impact:**
- Different certificate acquisition methods
- HTTP challenge may be more reliable in some network configurations
- Production uses production Let's Encrypt endpoint (rate limits apply)
- Staging uses staging endpoint (no rate limits)

**Production:**
```yaml
- "--certificatesresolvers.myresolver.acme.tlschallenge=true"
```

**Staging:**
```yaml
- "--certificatesresolvers.myresolver.acme.httpchallenge=true"
- "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web"
- "--certificatesresolvers.myresolver.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"
```

---

### 3. **Frontend Environment Variables**
**Staging:** Missing `NUXT_API_BASE` environment variable
**Production:** Has `NUXT_API_BASE=http://multivendor_backend:8000/api`

**Impact:**
- Production frontend can make internal API calls to backend
- Staging may not have this capability (if needed for SSR)

**Production:**
```yaml
frontend:
  environment:
    - NUXT_PUBLIC_API_BASE=https://${API_DOMAIN}/api
    - NUXT_API_BASE=http://multivendor_backend:8000/api  # Internal API
    - NUXT_PUBLIC_SITE_URL=https://${MAIN_DOMAIN}
```

**Staging:**
```yaml
frontend:
  environment:
    - NUXT_PUBLIC_API_BASE=https://${API_DOMAIN}/api
    - NUXT_PUBLIC_SITE_URL=https://${MAIN_DOMAIN}
    # Missing NUXT_API_BASE
```

---

### 4. **Frontend Traefik Router Rule**
**Staging:** Only handles main domain
**Production:** Handles both main domain and www subdomain

**Production:**
```yaml
- "traefik.http.routers.frontend.rule=Host(`${MAIN_DOMAIN}`) || Host(`www.${MAIN_DOMAIN}`)"
```

**Staging:**
```yaml
- "traefik.http.routers.frontend.rule=Host(`${MAIN_DOMAIN}`)"
```

---

### 5. **CORS Configuration**
**Staging:** Has `CORS_ALLOW_CREDENTIALS` environment variable
**Production:** Missing this variable

**Staging:**
```yaml
backend:
  environment:
    - CORS_ALLOW_CREDENTIALS=${CORS_ALLOW_CREDENTIALS:-True}
```

---

### 6. **Volume Configuration**
**Staging:** Uses external named volumes (some with external references)
**Production:** Uses default Docker volumes

**Staging:**
```yaml
volumes:
  postgres_data_staging:
    external: true
    name: indexo-staging_postgres_data_staging
  redis_data_staging:
    name: redis_data_staging
  static_files_staging:
    name: static_files_staging
  media_files_staging:
    name: media_files_staging
```

**Production:**
```yaml
volumes:
  postgres_data:
  redis_data:
  static_files:
  media_files:
```

---

### 7. **Container Names**
**Staging:** All containers have `_staging` suffix
**Production:** Standard names without suffix

---

## Recommended Fixes for Production

### Priority 1: Add pgbouncer (Most Critical)
This is likely the main cause of production errors, especially under load:

```yaml
# Add after db service
pgbouncer:
  image: edoburu/pgbouncer:latest
  container_name: multivendor_pgbouncer
  env_file:
    - .env
  environment:
    - DATABASES_HOST=db
    - DATABASES_PORT=5432
    - DATABASES_USER=${DB_USER}
    - DATABASES_PASSWORD=${DB_PASSWORD}
    - DATABASES_DBNAME=${DB_NAME}
    - PGBOUNCER_POOL_MODE=transaction
    - PGBOUNCER_MAX_CLIENT_CONN=1000
    - PGBOUNCER_DEFAULT_POOL_SIZE=25
    - PGBOUNCER_MIN_POOL_SIZE=5
    - PGBOUNCER_RESERVE_POOL_SIZE=5
    - PGBOUNCER_RESERVE_POOL_TIMEOUT=3
    - PGBOUNCER_MAX_DB_CONNECTIONS=100
  networks:
    - multivendor_network
  depends_on:
    db:
      condition: service_healthy
  healthcheck:
    test: ["CMD-SHELL", "psql -h localhost -U pgbouncer -d pgbouncer -c 'SHOW POOLS;' || exit 1"]
    interval: 30s
    timeout: 10s
    retries: 3
  restart: always

# Update backend service
backend:
  environment:
    - DB_HOST=pgbouncer  # Change from 'db' to 'pgbouncer'
  depends_on:
    db:
      condition: service_healthy
    redis:
      condition: service_healthy
    pgbouncer:  # Add this
      condition: service_healthy
```

### Priority 2: Add CORS_ALLOW_CREDENTIALS
If your frontend needs to send credentials with CORS requests:

```yaml
backend:
  environment:
    - CORS_ALLOW_CREDENTIALS=${CORS_ALLOW_CREDENTIALS:-True}
```

### Priority 3: Consider HTTP Challenge for SSL
If you're having SSL certificate issues, consider switching to HTTP challenge like staging:

```yaml
traefik:
  command:
    - "--certificatesresolvers.myresolver.acme.httpchallenge=true"
    - "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web"
    # Remove tlschallenge line
```

---

## Summary

The **most critical difference** is the missing **pgBouncer** in production. This connection pooler:
- Prevents database connection exhaustion
- Improves performance under load
- Reduces database overhead
- Is essential for production environments

Without pgbouncer, production likely experiences:
- Database connection errors
- Timeout issues
- Performance degradation under load
- Potential "too many connections" errors

Staging works because it has proper connection pooling, which is why it handles traffic better.


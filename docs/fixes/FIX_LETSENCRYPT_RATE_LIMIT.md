# Fix Let's Encrypt Rate Limit Error

## 🔴 Problem

Traefik logs show:
```
acme: error: 429 :: POST :: https://acme-v02.api.letsencrypt.org/acme/new-order :: 
urn:ietf:params:acme:error:rateLimited :: too many certificates (5) already issued 
for this exact set of identifiers in the last 168h0m0s
```

## 🔍 Root Cause

Let's Encrypt has rate limits:
- **5 certificates per exact set of domains per week** (168 hours)
- You've requested too many certificates for `api-staging.indexo.ir` in the last 7 days
- Rate limit resets after the time shown in the error message

## ✅ Solutions

### Option 1: Use Let's Encrypt Staging Endpoint (Recommended for Testing)

**Pros:**
- ✅ No rate limits
- ✅ Immediate certificate generation
- ✅ Good for testing

**Cons:**
- ⚠️ Certificates won't be trusted by browsers (you'll see security warnings)
- ⚠️ Not suitable for production

**Quick Fix:**
```bash
cd /root/indexo-staging

# Run the automated fix script
bash fix-letsencrypt-rate-limit.sh
```

Or manually:
```bash
# Update docker-compose.staging.yml
sed -i 's|https://acme-v02.api.letsencrypt.org/directory|https://acme-staging-v02.api.letsencrypt.org/directory|g' docker-compose.staging.yml

# Restart Traefik
docker compose -f docker-compose.staging.yml restart traefik
```

**Note:** The configuration has been updated to use staging endpoint by default. You can switch back later.

### Option 2: Wait for Rate Limit to Reset

1. **Check the retry time** in Traefik logs:
   ```bash
   docker logs traefik_staging | grep "retry after"
   ```

2. **Wait until that time** (usually 7 days from first request)

3. **Switch back to production endpoint**:
   ```bash
   sed -i 's|https://acme-staging-v02.api.letsencrypt.org/directory|https://acme-v02.api.letsencrypt.org/directory|g' docker-compose.staging.yml
   docker compose -f docker-compose.staging.yml restart traefik
   ```

### Option 3: Reuse Existing Certificate

If a certificate was already generated, you can reuse it:

```bash
# Check if certificate exists
ls -la /root/indexo-staging/letsencrypt/acme.json

# If it exists and has content, Traefik should reuse it automatically
# Just make sure the file has correct permissions
chmod 600 /root/indexo-staging/letsencrypt/acme.json
```

## 🔄 Switching Between Staging and Production Endpoints

### Current Configuration (Staging Endpoint)

The `docker-compose.staging.yml` is currently configured to use the **staging endpoint** to avoid rate limits. This means:
- Certificates will be generated immediately
- Browsers will show security warnings (this is normal and safe for testing)
- No rate limit restrictions

### When to Switch to Production

Switch back to production endpoint when:
1. Rate limit has reset (check logs for retry time)
2. You're ready for production deployment
3. You need browser-trusted certificates

**To switch to production:**
```bash
cd /root/indexo-staging
sed -i 's|https://acme-staging-v02.api.letsencrypt.org/directory|https://acme-v02.api.letsencrypt.org/directory|g' docker-compose.staging.yml
docker compose -f docker-compose.staging.yml restart traefik
```

## 📋 Let's Encrypt Rate Limits

| Limit | Value | Period |
|-------|-------|--------|
| Certificates per domain | 5 | 7 days (168 hours) |
| Duplicate certificates | 5 | 7 days |
| Failed validations | 5 | 1 hour |
| Registrations per IP | 10 | 3 hours |

**Source:** https://letsencrypt.org/docs/rate-limits/

## 🐛 Troubleshooting

### Still Getting Rate Limit Errors?

1. **Check if you're using staging endpoint**:
   ```bash
   grep "caserver" docker-compose.staging.yml
   ```
   Should show `acme-staging-v02` if using staging

2. **Clear old certificate attempts** (if needed):
   ```bash
   # Backup first
   cp letsencrypt/acme.json letsencrypt/acme.json.backup
   
   # Remove and let Traefik start fresh
   rm letsencrypt/acme.json
   docker compose -f docker-compose.staging.yml restart traefik
   ```

3. **Check for multiple certificate requests**:
   ```bash
   docker logs traefik_staging | grep -i "acme\|certificate" | tail -20
   ```

### Browser Shows Security Warning (Staging Certificates)

This is **normal and expected** when using Let's Encrypt staging endpoint. The certificate is valid but not trusted by browsers because it's for testing.

**To proceed:**
- Click "Advanced" → "Proceed to site" (or similar)
- The site will work normally, just with a warning

**To fix:**
- Switch to production endpoint after rate limit resets
- Or use a self-signed certificate for local testing

## 📝 Notes

- Staging endpoint is perfect for development/testing
- Production endpoint should be used for live sites
- Rate limits reset automatically after the time period
- Certificates auto-renew before expiration (90 days)

---

**Last Updated:** 2025-12-09
**Status:** Rate limit hit - using staging endpoint


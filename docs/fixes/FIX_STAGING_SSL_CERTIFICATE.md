# Fix SSL Certificate Error (ERR_CERT_AUTHORITY_INVALID)

## 🔴 Problem

After deployment, you're getting SSL certificate errors:
```
GET https://api-staging.indexo.ir/api/blog/categories/ net::ERR_CERT_AUTHORITY_INVALID
```

This means the browser doesn't trust the SSL certificate for your staging domains.

## 🔍 Root Cause

Traefik is trying to get SSL certificates from Let's Encrypt, but:
1. Certificate generation failed
2. DNS not properly configured
3. ACME challenge (TLS/HTTP) not completing
4. Certificate hasn't been generated yet

## ✅ Solution

### Step 1: Run Diagnostic Script

```bash
cd /root/indexo-staging
bash fix-ssl-staging.sh
```

This will check:
- Traefik logs for certificate errors
- DNS configuration
- Let's Encrypt directory permissions
- Certificate status

### Step 2: Verify DNS Configuration

Make sure your DNS records point to your VPS:

```bash
# Check if domains resolve to your server IP
nslookup api-staging.indexo.ir
nslookup staging.indexo.ir

# Your server IP should be:
curl -s ifconfig.me
```

**DNS Records Needed:**
```
A Record: api-staging.indexo.ir → YOUR_VPS_IP
A Record: staging.indexo.ir → YOUR_VPS_IP
```

### Step 3: Check Traefik Logs

```bash
docker logs traefik_staging --tail 100 | grep -i "acme\|certificate\|error"
```

Look for errors like:
- `acme: error`
- `certificate`
- `challenge`
- `timeout`

### Step 4: Fix Let's Encrypt Directory Permissions

```bash
cd /root/indexo-staging
mkdir -p letsencrypt
chmod 755 letsencrypt
chmod 600 letsencrypt/acme.json 2>/dev/null || touch letsencrypt/acme.json && chmod 600 letsencrypt/acme.json
```

### Step 5: Restart Traefik to Retry Certificate Generation

```bash
docker compose -f docker-compose.staging.yml restart traefik
```

Wait 1-2 minutes, then check logs:
```bash
docker logs traefik_staging --tail 50
```

### Step 6: Verify Certificate Generation

```bash
# Check if certificate file exists
ls -la /root/indexo-staging/letsencrypt/acme.json

# Check certificate details (if exists)
docker exec traefik_staging cat /letsencrypt/acme.json | grep -i "api-staging" || echo "Certificate not found yet"
```

## 🔧 Alternative: Use HTTP Challenge (More Reliable)

The configuration has been updated to use **HTTP challenge** instead of TLS challenge, which is more reliable. If you still have issues:

1. **Make sure port 80 is accessible** (required for HTTP challenge):
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

2. **Restart Traefik**:
   ```bash
   docker compose -f docker-compose.staging.yml restart traefik
   ```

3. **Wait for certificate generation** (can take 1-5 minutes):
   ```bash
   # Watch Traefik logs
   docker logs -f traefik_staging
   ```

## 🐛 Troubleshooting

### Certificate Still Not Working?

1. **Check if domains are accessible via HTTP**:
   ```bash
   curl -I http://api-staging.indexo.ir
   ```
   Should return 200 or 301 (redirect to HTTPS)

2. **Check Let's Encrypt rate limits**:
   - Let's Encrypt has rate limits (50 certificates per domain per week)
   - If you hit the limit, wait or use staging endpoint (see below)

3. **Use Let's Encrypt Staging for Testing** (optional):
   Edit `docker-compose.staging.yml` and change:
   ```yaml
   - "--certificatesresolvers.myresolver.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"
   ```
   **Note:** Staging certificates won't be trusted by browsers, but useful for testing the process.

4. **Check firewall**:
   ```bash
   sudo ufw status
   # Make sure ports 80 and 443 are open
   ```

5. **Verify Traefik can access port 80**:
   ```bash
   # From inside Traefik container
   docker exec traefik_staging wget -O- http://localhost:80 2>&1 | head -5
   ```

### Still Having Issues?

1. **Check DNS propagation**:
   ```bash
   dig api-staging.indexo.ir
   dig staging.indexo.ir
   ```
   Both should return your VPS IP

2. **Test from outside**:
   ```bash
   # From your local machine
   curl -I http://api-staging.indexo.ir
   curl -I https://api-staging.indexo.ir -k
   ```

3. **Check if another service is using port 80/443**:
   ```bash
   sudo netstat -tulpn | grep -E ':80|:443'
   ```

4. **Review full Traefik logs**:
   ```bash
   docker logs traefik_staging --tail 200
   ```

## 📝 Notes

- Certificate generation can take 1-5 minutes
- Let's Encrypt certificates are valid for 90 days and auto-renew
- HTTP challenge requires port 80 to be accessible from the internet
- Make sure your domains are publicly accessible (not behind a firewall that blocks Let's Encrypt)

---

**Last Updated:** 2025-12-09
**Status:** Ready to apply


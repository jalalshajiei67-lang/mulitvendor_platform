# 🚀 Dual Deployment Setup: Production + Staging Simultaneously

## Overview

This setup allows **both production and staging to run simultaneously** on the same VPS by:
1. Production Traefik: Ports 80/443 → `indexo.ir`, `api.indexo.ir`
2. Staging Traefik: Ports 8080/8443 → `staging.indexo.ir`, `api.staging.indexo.ir`
3. Host Nginx: Routes staging domains to staging Traefik

---

## 📋 Setup Steps

### Step 1: Install Nginx on Host (if not already installed)

```bash
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx
```

### Step 2: Get SSL Certificates for Staging Domains

```bash
sudo certbot certonly --standalone -d staging.indexo.ir -d www.staging.indexo.ir -d api.staging.indexo.ir
```

### Step 3: Configure Nginx Reverse Proxy

```bash
# Copy the staging proxy config
sudo cp nginx-staging-proxy.conf /etc/nginx/sites-available/staging-proxy

# Create symlink to enable it
sudo ln -s /etc/nginx/sites-available/staging-proxy /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### Step 4: Start Both Production and Staging

```bash
# Start production (ports 80/443)
docker-compose up -d

# Start staging (ports 8080/8443)
docker-compose -f docker-compose.staging.yml up -d --build
```

### Step 5: Verify Both Are Running

```bash
# Check production
docker-compose ps

# Check staging
docker-compose -f docker-compose.staging.yml ps

# Check nginx
sudo systemctl status nginx
```

---

## 🌐 Domain Routing

| Domain | Route | Port |
|--------|-------|------|
| `indexo.ir` | → Production Traefik | 80/443 |
| `api.indexo.ir` | → Production Traefik | 80/443 |
| `staging.indexo.ir` | → Host Nginx → Staging Traefik | 8080/8443 |
| `api.staging.indexo.ir` | → Host Nginx → Staging Traefik | 8080/8443 |

---

## 🔧 How It Works

1. **Production domains** (`indexo.ir`, `api.indexo.ir`):
   - DNS → VPS IP → Production Traefik (ports 80/443)
   - Production Traefik handles SSL and routes to services

2. **Staging domains** (`staging.indexo.ir`, `api.staging.indexo.ir`):
   - DNS → VPS IP → Host Nginx (port 443)
   - Host Nginx terminates SSL and proxies to Staging Traefik (port 8443)
   - Staging Traefik routes to staging services

---

## ⚠️ Important Notes

### SSL Certificates

- **Production**: Traefik handles SSL automatically via Let's Encrypt
- **Staging**: Host Nginx needs SSL certificates (obtained via certbot in Step 2)

### Port Configuration

- **Production Traefik**: Listens on ports 80/443 (standard)
- **Staging Traefik**: Listens on ports 8080/8443 (internal)
- **Host Nginx**: Listens on port 443 for staging domains, proxies to 8443

### Firewall

Make sure these ports are open:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp  # Optional, only if you want direct access
sudo ufw allow 8443/tcp  # Optional, only if you want direct access
```

---

## 🧪 Testing

### Test Production
```bash
curl -I https://indexo.ir
curl -I https://api.indexo.ir/api/
```

### Test Staging
```bash
curl -I https://staging.indexo.ir
curl -I https://api.staging.indexo.ir/api/
```

### Test Direct Staging Access (bypass nginx)
```bash
curl -I http://your-vps-ip:8080 -H "Host: staging.indexo.ir"
curl -I https://your-vps-ip:8443 -H "Host: staging.indexo.ir" -k
```

---

## 🔄 Alternative: Simpler Setup (Direct Port Access)

If you don't want to set up host nginx, you can access staging directly via ports:

- `http://staging.indexo.ir:8080` (HTTP)
- `https://staging.indexo.ir:8443` (HTTPS, self-signed cert)

**But this is not recommended** as it requires users to specify ports.

---

## 🐛 Troubleshooting

### Staging not accessible

1. **Check nginx is running**:
   ```bash
   sudo systemctl status nginx
   ```

2. **Check nginx config**:
   ```bash
   sudo nginx -t
   ```

3. **Check staging Traefik logs**:
   ```bash
   docker-compose -f docker-compose.staging.yml logs traefik
   ```

4. **Check port 8443 is accessible**:
   ```bash
   curl -I https://127.0.0.1:8443 -H "Host: staging.indexo.ir" -k
   ```

### SSL Certificate Issues

If staging SSL fails:
```bash
# Renew certificates
sudo certbot renew

# Or get new ones
sudo certbot certonly --standalone -d staging.indexo.ir -d www.staging.indexo.ir -d api.staging.indexo.ir
```

---

## ✅ Benefits

- ✅ Both production and staging run simultaneously
- ✅ No downtime when testing staging
- ✅ Production remains unaffected
- ✅ Standard HTTPS ports for both (via nginx proxy)
- ✅ Separate databases and data volumes
- ✅ Easy to scale and maintain


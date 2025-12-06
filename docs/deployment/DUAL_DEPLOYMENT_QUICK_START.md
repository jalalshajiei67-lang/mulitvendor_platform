# 🚀 Quick Start: Production + Staging Simultaneously

## ✅ What Changed

I've modified the staging configuration so **both production and staging can run at the same time**:

1. **Staging Traefik** now uses port **8080** (instead of 80) to avoid conflicts
2. **Host Nginx** will proxy staging domains to staging Traefik
3. **Production** continues using ports 80/443 as before

## 🎯 Architecture

```
Production:
  indexo.ir → Production Traefik (port 80/443) → Services

Staging:
  staging.indexo.ir → Host Nginx (port 443) → Staging Traefik (port 8080) → Services
```

## ⚡ Quick Setup (3 Steps)

### Step 1: Setup Host Nginx (One-time)

```bash
# Run the automated setup script
./setup-dual-deployment.sh
```

Or manually:
```bash
# Install nginx (if not installed)
sudo apt install -y nginx certbot python3-certbot-nginx

# Get SSL certificates for staging
sudo certbot certonly --standalone -d staging.indexo.ir -d www.staging.indexo.ir -d api.staging.indexo.ir

# Configure nginx
sudo cp nginx-staging-proxy.conf /etc/nginx/sites-available/staging-proxy
sudo ln -s /etc/nginx/sites-available/staging-proxy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 2: Start Both Services

```bash
# Start production (ports 80/443)
docker-compose up -d

# Start staging (port 8080)
docker-compose -f docker-compose.staging.yml up -d --build
```

### Step 3: Verify

```bash
# Check both are running
docker-compose ps
docker-compose -f docker-compose.staging.yml ps

# Test URLs
curl -I https://indexo.ir          # Production
curl -I https://staging.indexo.ir  # Staging
```

## 📋 Files Changed

1. **docker-compose.staging.yml**:
   - Traefik now uses port 8080 (instead of 80)
   - Removed HTTPS entrypoint (nginx handles SSL)
   - Updated Traefik labels to use HTTP entrypoint

2. **nginx-staging-proxy.conf** (NEW):
   - Host nginx config that routes staging domains to staging Traefik

3. **setup-dual-deployment.sh** (NEW):
   - Automated setup script

## 🌐 Domain Access

| Domain | Port | Route |
|--------|------|-------|
| `indexo.ir` | 443 | → Production Traefik |
| `api.indexo.ir` | 443 | → Production Traefik |
| `staging.indexo.ir` | 443 | → Host Nginx → Staging Traefik (8080) |
| `api.staging.indexo.ir` | 443 | → Host Nginx → Staging Traefik (8080) |

## ⚠️ Important Notes

1. **DNS**: Make sure `staging.indexo.ir` and `api.staging.indexo.ir` point to your VPS IP
2. **SSL**: Host nginx handles SSL for staging domains (via certbot)
3. **Ports**: 
   - Production: 80/443 (standard)
   - Staging: 8080 (internal, nginx proxies to it)
4. **No Conflicts**: Both can run simultaneously now! ✅

## 🐛 Troubleshooting

### Staging not accessible

```bash
# Check nginx
sudo systemctl status nginx
sudo nginx -t

# Check staging Traefik
docker-compose -f docker-compose.staging.yml logs traefik

# Test direct access
curl -I http://localhost:8080 -H "Host: staging.indexo.ir"
```

### Port 80 still in use

```bash
# Check what's using port 80
sudo lsof -i :80
sudo netstat -tlnp | grep :80

# Stop any conflicting services
sudo systemctl stop nginx  # If old nginx is running
docker-compose down        # If old production is running
```

## ✅ Benefits

- ✅ **Both run simultaneously** - No need to stop production
- ✅ **Zero downtime** - Test staging without affecting production
- ✅ **Standard HTTPS** - Both use port 443 (via nginx proxy)
- ✅ **Separate databases** - Complete isolation
- ✅ **Easy maintenance** - Start/stop independently

---

**Ready to deploy?** Run `./setup-dual-deployment.sh` and you're done! 🎉


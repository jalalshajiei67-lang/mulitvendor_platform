# Quick Setup: CapRover Volume + Nginx Caching

## 🚀 Quick Steps

### 1. Backend App Configuration

In CapRover Dashboard → `multivendor-backend` → App Configs:

**Persistent Directories:**
- `/app/staticfiles` → `/captain/data/backend-static` (Label: `static-files`)
- `/app/media` → `/captain/data/backend-media` (Label: `media-files`)

Click **"Save & Restart"**

### 2. Create Nginx Static Server App

1. CapRover Dashboard → **One-Click Apps/Databases** → **Custom App**
2. App Name: `nginx-static-server`
3. **Build Method:** Dockerfile
4. **Dockerfile Path:** `./Dockerfile.nginx-static`
5. **Repository:** Your GitHub repo URL

**Persistent Directories:**
- `/captain/data/backend-static` → `/captain/data/backend-static` (Label: `static`)
- `/captain/data/backend-media` → `/captain/data/backend-media` (Label: `media`)

Click **"Save & Restart"**

### 3. Configure Routing

In your **Backend App** → **HTTP Settings** → **Custom Nginx Configuration**:

```nginx
location /static/ {
    proxy_pass http://nginx-static-server;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /media/ {
    proxy_pass http://nginx-static-server;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Save and restart.

### 4. Deploy

1. Push code to GitHub
2. CapRover will auto-deploy (if CI/CD is set up)
3. Or manually trigger deployment

### 5. Verify

```bash
# Test static files
curl -I https://your-domain.com/static/admin/css/base.css

# Should see:
# Cache-Control: public, immutable
# Expires: (1 year from now)
# HTTP/1.1 200 OK
```

## 📋 Checklist

- [ ] Backend app has persistent directories configured
- [ ] Nginx static server app created
- [ ] Nginx static server has persistent directories configured
- [ ] Routing configured in backend app HTTP settings
- [ ] Both apps deployed and running
- [ ] Static files accessible via `/static/` endpoint
- [ ] Media files accessible via `/media/` endpoint
- [ ] Cache working (check X-Cache-Status header)

## 🔍 Troubleshooting

**404 Errors:**
- Check if `collectstatic` ran: Backend app logs should show it
- Verify persistent directories are mounted correctly
- Check file permissions in volumes

**Cache Not Working:**
- Check response headers for `Cache-Control` and `Expires`
- Verify routing configuration
- Check if files exist in `/captain/data/backend-static`
- Check Nginx static server logs for errors

## 📚 Full Documentation

See `NGINX_STATIC_SETUP.md` for detailed configuration and troubleshooting.


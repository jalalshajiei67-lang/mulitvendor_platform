# 🚀 Axios to Django - Quick Reference Card

## 📍 Where Axios Finds Django Backend

### **Local Development** (npm run dev)
```
Frontend: localhost:5173
   ↓ Vite Proxy
   ↓ /api → 127.0.0.1:8000
   ↓
Django: 127.0.0.1:8000
```

**Configuration:**
- File: `vite.config.js`
- Proxy: `/api` → `http://127.0.0.1:8000`
- No CORS issues (proxy handles it)

---

### **Docker Production** (docker-compose up)
```
Browser: localhost:80
   ↓
Nginx: Port 80
   ├─ /api/*    → backend:80 (Django)
   ├─ /admin/*  → backend:80 (Django)
   ├─ /media/*  → Volume
   └─ /*        → frontend:80 (Vue)
```

**Configuration:**
- File: `nginx/conf.d/default.conf`
- All traffic goes through Nginx
- Containers communicate via Docker network

---

## 🔑 Key Files

### 1. **Axios Configuration**
📁 `multivendor_platform/front_end/src/services/api.js`
```javascript
// Development: http://127.0.0.1:8000/api
// Production: /api (relative, handled by Nginx)
```

### 2. **Vite Proxy** (NEW! ✨)
📁 `multivendor_platform/front_end/vite.config.js`
```javascript
proxy: {
  '/api': { target: 'http://127.0.0.1:8000' }
}
```

### 3. **Nginx Routing**
📁 `nginx/conf.d/default.conf`
```nginx
location /api/ {
  proxy_pass http://backend;
}
```

---

## 🧪 Test Commands

### **Check Backend is Running**
```bash
# Local
curl http://127.0.0.1:8000/api/

# Docker
curl http://localhost/api/
docker logs multivendor_backend
```

### **Check Nginx Routing**
```bash
docker exec multivendor_nginx nginx -t
docker logs multivendor_nginx
```

### **Check Frontend Build**
```bash
# Development
cd multivendor_platform/front_end
npm run dev

# Production build
npm run build
```

---

## 🐛 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| CORS error in development | ✅ Fixed! Vite proxy now handles it |
| 404 in Docker | Check Nginx config & backend health |
| Connection refused | Ensure backend is running on port 8000 |
| Timeout errors | Check backend logs for errors |

---

## 📊 Request Flow Examples

### **Fetch Products**
```javascript
// In your store
api.getProducts()
  ↓
// Axios request
GET /api/products/
  ↓
// Development: Vite proxy → Django
// Production: Nginx → backend:80 → Django
```

### **Login**
```javascript
api.login({ username, password })
  ↓
POST /api/auth/login/
  ↓
// Token saved in localStorage
// Interceptor adds it to future requests
```

---

## 🎯 Environment Variables

Create these files (optional):

### `.env.local` (Development)
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### `.env.production` (Production)
```env
# Leave empty or use:
VITE_API_BASE_URL=
# Nginx will handle routing
```

---

## ✅ Current Status

- ✅ Axios installed and configured
- ✅ All stores using centralized API service
- ✅ Request/response interceptors active
- ✅ Authentication token auto-attached
- ✅ Vite proxy configured (eliminates CORS)
- ✅ Production uses relative URLs
- ✅ Docker Nginx routing configured

---

## 🔄 What Changed Today

1. **Fixed syntax error** in products.js
2. **Removed duplicate** axios.js file
3. **Added Vite proxy** for better local development
4. **Updated API_BASE_URL** logic for Docker compatibility

---

## 📚 Related Files

- `AXIOS_TO_DJANGO_CONNECTION_GUIDE.md` - Full detailed guide
- `docker-compose.yml` - Container orchestration
- `nginx/conf.d/default.conf` - Nginx routing rules

---

**Need help?** Check the logs:
```bash
# Backend
docker logs multivendor_backend -f

# Nginx
docker logs multivendor_nginx -f

# Frontend (during build)
docker logs multivendor_frontend -f
```



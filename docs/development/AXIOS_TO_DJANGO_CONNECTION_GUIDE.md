# 🔌 How Axios Finds Django Backend - Complete Flow

## 📊 Overview

Your frontend Vue.js application uses **axios** to communicate with the Django backend. The connection path differs based on your environment (local development vs Docker production).

---

## 🎯 The Connection Flow

### 1️⃣ **Axios Configuration** (`services/api.js`)

```javascript
// Line 5-9 in services/api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (
  import.meta.env.MODE === 'production'
    ? 'https://multivendor-backend.indexo.ir'
    : 'http://127.0.0.1:8000'
);

// Line 11-12
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  // ... other config
});
```

**How it works:**
- Checks for `VITE_API_BASE_URL` environment variable
- If not found, uses **MODE**:
  - Production → `https://multivendor-backend.indexo.ir`
  - Development → `http://127.0.0.1:8000`

---

## 🌐 Architecture Diagrams

### **Scenario 1: Local Development** (Without Docker)

```
┌─────────────────────┐
│   Your Browser      │
│   localhost:5173    │
└──────────┬──────────┘
           │
           │ HTTP Request
           │ GET http://127.0.0.1:8000/api/products/
           │
           ▼
┌─────────────────────┐
│  Django Backend     │
│  127.0.0.1:8000     │
│  (python manage.py) │
└─────────────────────┘
```

**Steps:**
1. Vue dev server runs on `localhost:5173`
2. Axios calls: `http://127.0.0.1:8000/api/products/`
3. Django responds directly from port 8000
4. **CORS** must be configured to allow `localhost:5173`

---

### **Scenario 2: Docker Compose** (Production/Testing)

```
┌────────────────────────────────────────────────────────────┐
│                      Your Browser                          │
│                  http://localhost:80                       │
└───────────────────────────┬────────────────────────────────┘
                            │
                            │ HTTP Request
                            │ GET /api/products/
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    Nginx Container                         │
│                   Port 80 (external)                       │
│                                                            │
│  Routing Rules (nginx/conf.d/default.conf):               │
│  ┌──────────────────────────────────────────────┐        │
│  │ /api/*      → proxy_pass to backend:80       │        │
│  │ /admin/*    → proxy_pass to backend:80       │        │
│  │ /static/*   → serve from volume              │        │
│  │ /media/*    → serve from volume              │        │
│  │ /*          → proxy_pass to frontend:80      │        │
│  └──────────────────────────────────────────────┘        │
└────────┬────────────────────────────┬────────────────────┘
         │                            │
         │ /api/ requests             │ Other requests
         │                            │
         ▼                            ▼
┌──────────────────────┐    ┌──────────────────────┐
│  Backend Container   │    │  Frontend Container  │
│  backend:80          │    │  frontend:80         │
│  (Django + Gunicorn) │    │  (Nginx serving      │
│                      │    │   Vue dist files)    │
│  Internal network    │    │                      │
│  multivendor_network │    │  Internal network    │
└──────────────────────┘    └──────────────────────┘
         │
         │
         ▼
┌──────────────────────┐
│   Database (db)      │
│   PostgreSQL:5432    │
│   multivendor_network│
└──────────────────────┘
```

**Steps:**
1. Browser requests `http://localhost/`
2. Nginx receives request on port 80
3. Nginx routes based on URL path:
   - `/api/*` → Forwards to `backend:80` container
   - `/admin/*` → Forwards to `backend:80` container
   - `/static/*` → Serves from volume directly
   - `/media/*` → Serves from volume directly
   - `/*` → Forwards to `frontend:80` container
4. Frontend Vue app is served from `frontend` container
5. When Vue app makes axios call to `/api/products/`:
   - Request goes through Nginx again
   - Nginx proxies to `backend:80`
   - Django processes and responds

---

## 🔧 Configuration Files Breakdown

### **1. Frontend Axios Configuration** 📝

File: `multivendor_platform/front_end/src/services/api.js`

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (
  import.meta.env.MODE === 'production'
    ? 'https://multivendor-backend.indexo.ir'    // Production URL
    : 'http://127.0.0.1:8000'        // Local development
);
```

### **2. Docker Compose** 🐳

File: `docker-compose.yml`

```yaml
backend:
  expose:
    - "8000"           # Exposed internally to Docker network
  networks:
    - multivendor_network

frontend:
  expose:
    - "80"             # Exposed internally to Docker network
  networks:
    - multivendor_network

nginx:
  ports:
    - "80:80"          # Exposed to host machine
  networks:
    - multivendor_network
```

**Key Points:**
- Backend and Frontend are **NOT** directly accessible from your browser
- Only **Nginx** is exposed to the outside world (port 80)
- All services communicate on the **same Docker network**

### **3. Nginx Routing** 🌐

File: `nginx/conf.d/default.conf`

```nginx
# Backend upstream (Docker service name)
upstream backend {
    server backend:80;    # 'backend' is the container name
}

# Frontend upstream
upstream frontend {
    server frontend:80;   # 'frontend' is the container name
}

# Route API requests to Django
location /api/ {
    proxy_pass http://backend;
    # ... headers
}

# Route everything else to Vue.js
location / {
    proxy_pass http://frontend;
    # ... headers
}
```

---

## 🔑 Environment Variables

### **For Local Development**

Create: `multivendor_platform/front_end/.env.local`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_DJANGO_ADMIN_URL=http://127.0.0.1:8000/admin/
```

### **For Docker Production**

The frontend **doesn't need** `VITE_API_BASE_URL` because:
- Frontend is served from Nginx at `http://localhost/`
- Axios makes requests to `/api/` (relative path)
- Nginx intercepts and proxies to `backend:80`

**Build-time environment** (optional):
```env
# In frontend Dockerfile or build args
VITE_API_BASE_URL=/api
```

This makes axios use **relative URLs**, which Nginx then routes correctly.

---

## 🧪 How Each Request Works

### **Example: Fetch Products**

#### Local Development:
```javascript
// In products.js store
api.getProducts(params)
↓
// In services/api.js
apiClient.get('/products/', { params })
↓
// Axios makes request to:
http://127.0.0.1:8000/api/products/?page=1
↓
// Django receives directly
Django REST Framework responds
```

#### Docker Production:
```javascript
// In products.js store
api.getProducts(params)
↓
// In services/api.js
apiClient.get('/products/', { params })
↓
// Axios makes request to:
/api/products/?page=1  (relative URL if baseURL is '/api')
// OR
http://localhost/api/products/ (if baseURL includes domain)
↓
// Nginx receives request
location /api/ matches → proxy_pass to backend:80
↓
// Django container receives
Django REST Framework processes and responds
↓
// Nginx forwards response back
Response → Browser
```

---

## 🐛 Troubleshooting

### **Issue 1: CORS Errors (Local Development)**

**Problem:** Browser blocks request from `localhost:5173` to `127.0.0.1:8000`

**Solution:** Configure Django CORS

File: `multivendor_platform/multivendor_platform/settings.py`
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### **Issue 2: 404 Not Found in Docker**

**Problem:** Axios requests return 404 in Docker

**Checklist:**
1. ✅ Is Nginx running? `docker-compose ps`
2. ✅ Check Nginx logs: `docker logs multivendor_nginx`
3. ✅ Check backend logs: `docker logs multivendor_backend`
4. ✅ Verify Nginx config: `docker exec multivendor_nginx nginx -t`
5. ✅ Check if backend is healthy: `docker-compose ps backend`

### **Issue 3: Cannot connect to backend from frontend container**

**Problem:** Frontend build fails or can't reach backend

**Cause:** Using wrong baseURL at build time

**Solution:** 
- For production Docker builds, use **relative paths** (`/api`)
- OR set `VITE_API_BASE_URL=/api` as build arg in frontend Dockerfile

---

## 📝 Current Configuration Summary

### ✅ **What's Working:**

1. **Axios Client**: Properly configured with interceptors
2. **Authentication**: Token automatically added via interceptor
3. **Error Handling**: Response/request interceptors for logging
4. **Store Integration**: All stores (products, auth, blog) use centralized API
5. **Docker Setup**: Nginx properly routes traffic

### 🔧 **Recommended Optimizations:**

#### 1. **Add Vite Proxy for Local Development**

Update `multivendor_platform/front_end/vite.config.js`:

```javascript
export default defineConfig({
  // ... existing config
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/admin': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
```

**Benefit:** Eliminates CORS issues in local development

#### 2. **Use Relative URLs in Docker**

Update `services/api.js` for better Docker compatibility:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.MODE === 'production' ? '' : 'http://127.0.0.1:8000');

const apiClient = axios.create({
  baseURL: API_BASE_URL ? `${API_BASE_URL}/api` : '/api',
  // ... rest of config
});
```

This makes Docker deployment simpler (no need to hardcode domains).

---

## 🎉 Summary

**Local Development:**
```
Browser → http://127.0.0.1:8000/api/ → Django
```

**Docker Production:**
```
Browser → http://localhost/api/ → Nginx → backend:80 → Django
```

The key is understanding that:
- **Axios** uses environment variables or fallback values
- **Nginx** acts as a reverse proxy in Docker
- **Docker network** allows containers to communicate using service names
- **CORS** is only needed for local development (cross-origin requests)

Your current setup is well-structured and production-ready! 🚀



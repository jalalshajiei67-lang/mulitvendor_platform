# Multivendor Platform - Docker Deployment

This is a complete Docker-based deployment setup for your Django + Vue.js multivendor platform.

## 📁 Deployment Files Structure

```
damirco/
├── docker-compose.yml           # Docker orchestration
├── .env                         # Environment variables (create from env.template)
├── env.template                 # Environment template
├── .dockerignore                # Docker ignore patterns
│
├── nginx/                       # Nginx configuration
│   ├── nginx.conf              # Main nginx config
│   └── conf.d/
│       ├── default.conf        # HTTP configuration
│       └── ssl.conf.example    # HTTPS configuration (optional)
│
├── Deployment Scripts:
├── deploy.sh                    # Local deployment script (Linux/Mac)
├── deploy-windows.bat           # Local deployment script (Windows)
├── server-deploy.sh             # Server setup script (run on VPS)
├── setup-ssl.sh                 # SSL certificate setup
├── manage-deployment.sh         # Interactive management menu
├── test-connection.sh           # Test VPS connection
├── monitor.sh                   # Health monitoring
│
└── Documentation:
    ├── QUICK_START.md           # 5-minute deployment guide
    ├── DEPLOYMENT_GUIDE.md      # Comprehensive guide
    └── README_DEPLOYMENT.md     # This file
```

## 🎯 What Gets Deployed

### Services

1. **PostgreSQL Database** (port 5432, internal)
   - Persistent data volume
   - Health checks enabled

2. **Django Backend** (internal port 80)
   - Gunicorn WSGI server
   - Automatic migrations
   - Static file serving via WhiteNoise

3. **Vue.js Frontend** (internal port 80)
   - Production build
   - Nginx static file server
   - Optimized assets

4. **Nginx Reverse Proxy** (port 80, 443)
   - Routes requests to backend/frontend
   - Serves static and media files
   - SSL/TLS ready

5. **Certbot** (for SSL certificates)
   - Automatic certificate renewal
   - Let's Encrypt integration

### Volumes

- `postgres_data`: Database persistence
- `media_files`: User uploaded files
- `static_files`: Django static files

### Network

- `multivendor_network`: Bridge network for container communication

## 🚀 Deployment Options

### Option 1: Quick Deploy (Recommended)

See `QUICK_START.md` for 5-minute deployment.

### Option 2: Detailed Deploy

See `DEPLOYMENT_GUIDE.md` for comprehensive instructions.

### Option 3: Manual Deploy

1. Create `.env` from `env.template`
2. Run `deploy.sh` or `deploy-windows.bat`
3. SSH to VPS and run `./server-deploy.sh`

## 🔑 Environment Variables

Required in `.env` file:

```env
# Database
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=YOUR_SECURE_PASSWORD

# Django
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=158.255.74.123,yourdomain.com
CORS_ALLOWED_ORIGINS=http://yourdomain.com,https://yourdomain.com

# Optional (for SSL)
DOMAIN=yourdomain.com
EMAIL=admin@yourdomain.com
```

## 🌐 URL Structure

After deployment:

- `/` → Vue.js Frontend
- `/api/` → Django REST API
- `/admin/` → Django Admin Panel
- `/static/` → Django Static Files
- `/media/` → User Uploaded Files
- `/sitemap.xml` → SEO Sitemap
- `/robots.txt` → SEO Robots

## 🛠️ Management

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Interactive Management
```bash
./manage-deployment.sh
```

### Monitor Health
```bash
./monitor.sh
```

## 🔒 Security Features

✅ Firewall configuration (UFW)  
✅ Environment variable isolation  
✅ PostgreSQL password protection  
✅ CSRF protection  
✅ CORS configuration  
✅ SSL/HTTPS ready  
✅ Security headers in Nginx  

## 📊 Resource Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 2 GB
- Disk: 20 GB
- OS: Ubuntu 20.04+

**Recommended:**
- CPU: 4 cores
- RAM: 4 GB
- Disk: 50 GB
- OS: Ubuntu 22.04 LTS

## 🔄 Update Workflow

1. Make code changes locally
2. Run deployment script: `./deploy.sh`
3. SSH to VPS: `ssh root@158.255.74.123`
4. Rebuild: `docker-compose up -d --build`
5. Migrate: `docker-compose exec backend python manage.py migrate`

## 🐛 Troubleshooting

### Containers won't start
```bash
docker-compose logs
docker-compose down
docker-compose up -d --build --force-recreate
```

### Database connection error
```bash
docker-compose logs db
docker-compose restart db
```

### 502 Bad Gateway
```bash
docker-compose logs backend nginx
docker-compose restart backend nginx
```

See `DEPLOYMENT_GUIDE.md` for more troubleshooting.

## 📞 Support Resources

- **Full Documentation**: `DEPLOYMENT_GUIDE.md`
- **Quick Start**: `QUICK_START.md`
- **Django Docs**: https://docs.djangoproject.com
- **Vue.js Docs**: https://vuejs.org
- **Docker Docs**: https://docs.docker.com

## 🎓 Tips

1. Always backup before updates:
   ```bash
   docker-compose exec db pg_dump -U postgres multivendor_db > backup.sql
   ```

2. Monitor resource usage:
   ```bash
   docker stats
   ```

3. Keep system updated:
   ```bash
   apt-get update && apt-get upgrade
   ```

4. Use the management interface for common tasks:
   ```bash
   ./manage-deployment.sh
   ```

## 📝 Your VPS Details

- **IP**: 158.255.74.123
- **User**: root
- **Project Path**: /opt/multivendor_platform
- **SSH Command**: `ssh root@158.255.74.123`

## ✅ Deployment Checklist

- [ ] Create `.env` file from template
- [ ] Set secure DB_PASSWORD
- [ ] Generate and set SECRET_KEY
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Test SSH connection
- [ ] Run deployment script
- [ ] Start services on VPS
- [ ] Run migrations
- [ ] Create superuser
- [ ] Test frontend access
- [ ] Test admin panel access
- [ ] Test API endpoints
- [ ] Set up SSL (if using domain)
- [ ] Configure regular backups
- [ ] Set up monitoring

---

**Ready to deploy?** Start with `QUICK_START.md`!




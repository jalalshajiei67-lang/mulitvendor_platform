# 🚀 Multivendor Platform - Production Deployment

A complete dockerized deployment solution for your Django + Vue.js multivendor e-commerce platform.

## 📋 Quick Info

- **VPS IP**: 158.255.74.123
- **SSH Access**: `ssh root@158.255.74.123`
- **Platform**: Django REST API + Vue.js SPA
- **Database**: PostgreSQL
- **Web Server**: Nginx (Reverse Proxy)
- **Containerization**: Docker + Docker Compose

---

## 🎯 Getting Started

### **👉 [START DEPLOYMENT HERE](docs/deployment/START_DEPLOYMENT_HERE.md)** 👈

Choose your deployment path:

1. **5-Minute Deploy**: See [QUICK_START.md](docs/development/QUICK_START.md)
2. **Detailed Guide**: See [DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md)
3. **One Command**: Run `./deploy-one-command.sh` (Linux/Mac)

---

## ✨ What's Included

### 🐳 Docker Services
- PostgreSQL 15 (Database)
- Django Backend (Gunicorn + WhiteNoise)
- Vue.js Frontend (Production Build)
- Nginx (Reverse Proxy + Static Files)
- Certbot (SSL/HTTPS)

### 📜 Deployment Scripts
- `deploy-windows.bat` - Windows deployment
- `deploy.sh` - Linux/Mac deployment
- `deploy-one-command.sh` - Automated deployment
- `server-deploy.sh` - VPS setup
- `setup-ssl.sh` - SSL certificate setup

### 🛠️ Management Tools
- `manage-deployment.sh` - Interactive menu interface
- `monitor.sh` - Health monitoring
- `health-check.sh` - Quick health check
- `backup-database.sh` - Database backup
- `restore-database.sh` - Database restore
- `update-app.sh` - Application updates
- `setup-cron-backup.sh` - Automated backups
- `verify-setup.sh` - Pre-deployment verification

### 📚 Documentation
- [START_DEPLOYMENT_HERE.md](docs/deployment/START_DEPLOYMENT_HERE.md) - Complete getting started
- [QUICK_START.md](docs/development/QUICK_START.md) - 5-minute deployment
- [DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md) - Comprehensive guide
- [README_DEPLOYMENT.md](docs/deployment/README_DEPLOYMENT.md) - Technical overview
- [DEPLOYMENT_SUMMARY.md](docs/deployment/DEPLOYMENT_SUMMARY.md) - What was created

#### Documentation Categories
- 📦 **[Deployment](docs/deployment/)** - Deployment guides, CI/CD, infrastructure
- 🐛 **[Fixes](docs/fixes/)** - Troubleshooting and bug fixes
- ✨ **[Features](docs/features/)** - Feature documentation and guides
- ⚙️ **[Setup](docs/setup/)** - Configuration and setup guides
- 💻 **[Development](docs/development/)** - Development and testing guides
- 🔄 **[Migration](docs/migration/)** - Migration guides and notes

---

## 🚀 Quick Deploy

### Windows
```cmd
REM 1. Create environment file
copy .env.production .env

REM 2. Deploy
deploy-windows.bat

REM 3. SSH and start services
ssh root@158.255.74.123
cd /opt/multivendor_platform
./server-deploy.sh
```

### Linux/Mac
```bash
# One command deployment
./deploy-one-command.sh

# Or step by step
cp .env.production .env
chmod +x *.sh
./deploy.sh
ssh root@158.255.74.123
cd /opt/multivendor_platform
./server-deploy.sh
```

---

## 🌐 After Deployment

Your application will be available at:

- **Frontend**: http://158.255.74.123
- **Admin Panel**: http://158.255.74.123/admin
- **API**: http://158.255.74.123/api
- **Media Files**: http://158.255.74.123/media
- **Static Files**: http://158.255.74.123/static

---

## 🔑 First Steps After Deployment

### 1. Create Superuser
```bash
ssh root@158.255.74.123
cd /opt/multivendor_platform
docker-compose exec backend python manage.py createsuperuser
```

### 2. Test Application
- Visit http://158.255.74.123
- Login to admin panel
- Test API endpoints

### 3. Configure Domain (Optional)
```bash
# Update .env with your domain
nano .env

# Setup SSL
./setup-ssl.sh yourdomain.com
```

### 4. Setup Automated Backups
```bash
./setup-cron-backup.sh
```

---

## 🛠️ Management Commands

### Interactive Interface
```bash
./manage-deployment.sh
```

### Common Tasks
```bash
# Check health
./health-check.sh

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Backup database
./backup-database.sh

# Monitor
./monitor.sh

# Update application
./update-app.sh
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│              Internet                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │  Nginx :80/443 │  ← Reverse Proxy
        │   (SSL Ready)  │
        └───┬────────┬───┘
            │        │
    ┌───────┘        └────────┐
    │                         │
    ▼                         ▼
┌─────────┐            ┌──────────┐
│ Django  │            │ Vue.js   │
│ Backend │            │ Frontend │
│ :80     │            │ :80      │
└────┬────┘            └──────────┘
     │
     ▼
┌──────────────┐
│ PostgreSQL   │
│ :5432        │
└──────────────┘
```

---

## 🔐 Security Features

✅ **Environment Variable Isolation**: Sensitive data in .env  
✅ **PostgreSQL Password Protection**: Secured database access  
✅ **Django SECRET_KEY**: Auto-generated secure key  
✅ **Firewall Configuration**: UFW enabled (ports 22, 80, 443)  
✅ **CORS Protection**: Configured for your domain  
✅ **CSRF Protection**: Django built-in  
✅ **SSL/HTTPS Ready**: Let's Encrypt integration  
✅ **Security Headers**: Nginx configuration  

---

## 📦 Project Structure

```
damirco/
├── docker-compose.yml          # Service orchestration
├── .env.production            # Environment template
├── .dockerignore              # Docker ignore
├── Dockerfile                 # Backend container
│
├── nginx/                     # Nginx configuration
│   ├── nginx.conf
│   └── conf.d/
│       ├── default.conf
│       └── ssl.conf.example
│
├── Deployment Scripts/
├── deploy.sh
├── deploy-windows.bat
├── deploy-one-command.sh
├── server-deploy.sh
├── setup-ssl.sh
│
├── Management Scripts/
├── manage-deployment.sh
├── monitor.sh
├── health-check.sh
├── backup-database.sh
├── restore-database.sh
├── update-app.sh
├── setup-cron-backup.sh
├── test-connection.sh
├── verify-setup.sh
│
├── docs/                      # All documentation organized by category
│   ├── deployment/            # Deployment guides, CI/CD, infrastructure
│   ├── fixes/                 # Troubleshooting and bug fixes
│   ├── features/              # Feature documentation
│   ├── setup/                 # Configuration and setup
│   ├── development/           # Development and testing
│   └── migration/             # Migration guides
└── README.md                  # This file (main entry point)
```

---

## 🆘 Troubleshooting

### Deployment Issues
```bash
# Verify setup before deploying
./verify-setup.sh

# Test VPS connection
./test-connection.sh
```

### Runtime Issues
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Health check
./health-check.sh

# Restart everything
docker-compose down
docker-compose up -d --build
```

### Database Issues
```bash
# Check database
docker-compose exec db psql -U postgres -d multivendor_db

# Backup before fixing
./backup-database.sh
```

See [DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md) for detailed troubleshooting.

---

## 📈 Monitoring & Maintenance

### Regular Tasks
- **Daily**: Check logs and health
- **Weekly**: Review backups
- **Monthly**: Update system packages
- **Quarterly**: Security audit

### Monitoring
```bash
# Quick health check
./health-check.sh

# Detailed monitoring
./monitor.sh

# Resource usage
docker stats

# Disk usage
df -h
```

### Backups
```bash
# Manual backup
./backup-database.sh

# Automated daily backups
./setup-cron-backup.sh

# Restore from backup
./restore-database.sh
```

---

## 🔄 Updating Your Application

### Method 1: Using Update Script
```bash
# On local machine
./deploy.sh

# On VPS
ssh root@158.255.74.123
cd /opt/multivendor_platform
./update-app.sh
```

### Method 2: Manual Update
```bash
docker-compose down
docker-compose pull
docker-compose up -d --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```

---

## 📞 Support & Documentation

### Essential Documents
1. **Getting Started**: [START_DEPLOYMENT_HERE.md](docs/deployment/START_DEPLOYMENT_HERE.md)
2. **Quick Deploy**: [QUICK_START.md](docs/development/QUICK_START.md)
3. **Full Guide**: [DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md)
4. **Tech Details**: [README_DEPLOYMENT.md](docs/deployment/README_DEPLOYMENT.md)

### External Resources
- [Docker Documentation](https://docs.docker.com)
- [Django Documentation](https://docs.djangoproject.com)
- [Vue.js Documentation](https://vuejs.org)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## ✅ Pre-Deployment Checklist

- [ ] Run `./verify-setup.sh`
- [ ] Create `.env` from `.env.production`
- [ ] Review and update `DB_PASSWORD` in `.env`
- [ ] Verify `SECRET_KEY` is set in `.env`
- [ ] Test SSH connection to VPS
- [ ] Ensure VPS has minimum 2GB RAM
- [ ] Backup existing data (if any)

---

## 🎯 Post-Deployment Checklist

- [ ] All containers running (`docker-compose ps`)
- [ ] Frontend accessible (http://158.255.74.123)
- [ ] Admin panel accessible (http://158.255.74.123/admin)
- [ ] API endpoints responding (http://158.255.74.123/api)
- [ ] Superuser created
- [ ] SSL configured (if using domain)
- [ ] Automated backups enabled
- [ ] Firewall configured
- [ ] Health monitoring working

---

## 💡 Pro Tips

1. **Use the Interactive Manager**: `./manage-deployment.sh` for easy management
2. **Regular Backups**: Set up automated backups with `./setup-cron-backup.sh`
3. **Monitor Regularly**: Run `./health-check.sh` daily
4. **Keep Updated**: Update system packages monthly
5. **Review Logs**: Check `docker-compose logs` for issues
6. **Test Backups**: Regularly test backup restoration
7. **Document Changes**: Keep notes on configuration changes
8. **Security First**: Always use HTTPS in production

---

## 🎉 Ready to Deploy?

### Choose Your Path:

**🚀 Fastest**: `./deploy-one-command.sh`  
**📖 Guided**: [START_DEPLOYMENT_HERE.md](docs/deployment/START_DEPLOYMENT_HERE.md)  
**⚡ Quick**: [QUICK_START.md](docs/development/QUICK_START.md)  
**📚 Detailed**: [DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md)

---

## 📝 License

This deployment configuration is part of your multivendor platform project.

---

**Questions?** Check the documentation files or review the deployment scripts for details.

**Ready to start?** → [Click here to begin deployment](docs/deployment/START_DEPLOYMENT_HERE.md)




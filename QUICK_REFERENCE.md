# 🚀 Quick Reference Card

## 📍 VPS Information
```
IP Address: 158.255.74.123
Username:   root
Password:   e<c6w:1EDupHjf4*
SSH:        ssh root@158.255.74.123
Project:    /opt/multivendor_platform
```

## 🌐 Application URLs
```
Frontend:     http://158.255.74.123
Admin Panel:  http://158.255.74.123/admin
API:          http://158.255.74.123/api
Media:        http://158.255.74.123/media
Static:       http://158.255.74.123/static
```

## 🚀 Deploy Commands

### Windows
```cmd
copy .env.production .env
deploy-windows.bat
```

### Linux/Mac
```bash
./deploy-one-command.sh
```

## 🛠️ Management Commands

### Interactive Menu
```bash
./manage-deployment.sh
```

### Common Tasks
| Task | Command |
|------|---------|
| **Start services** | `docker-compose up -d` |
| **Stop services** | `docker-compose down` |
| **Restart services** | `docker-compose restart` |
| **View logs** | `docker-compose logs -f` |
| **Check status** | `docker-compose ps` |
| **Health check** | `./health-check.sh` |
| **Monitor** | `./monitor.sh` |

### Database
| Task | Command |
|------|---------|
| **Backup** | `./backup-database.sh` |
| **Restore** | `./restore-database.sh` |
| **Access DB** | `docker-compose exec db psql -U postgres -d multivendor_db` |

### Django
| Task | Command |
|------|---------|
| **Create superuser** | `docker-compose exec backend python manage.py createsuperuser` |
| **Migrations** | `docker-compose exec backend python manage.py migrate` |
| **Collect static** | `docker-compose exec backend python manage.py collectstatic` |
| **Django shell** | `docker-compose exec backend python manage.py shell` |

### Container Management
| Task | Command |
|------|---------|
| **View logs (all)** | `docker-compose logs -f` |
| **View logs (backend)** | `docker-compose logs -f backend` |
| **View logs (frontend)** | `docker-compose logs -f frontend` |
| **View logs (nginx)** | `docker-compose logs -f nginx` |
| **Restart backend** | `docker-compose restart backend` |
| **Rebuild all** | `docker-compose down && docker-compose up -d --build` |

### System
| Task | Command |
|------|---------|
| **Resource usage** | `docker stats` |
| **Disk usage** | `df -h` |
| **Memory usage** | `free -h` |
| **Firewall status** | `ufw status` |

## 🔧 Troubleshooting

### Application Not Loading
```bash
docker-compose ps              # Check if containers running
docker-compose logs nginx      # Check nginx logs
docker-compose restart nginx   # Restart nginx
```

### 502 Bad Gateway
```bash
docker-compose logs backend    # Check backend logs
docker-compose restart backend # Restart backend
docker-compose restart nginx   # Restart nginx
```

### Database Errors
```bash
docker-compose logs db         # Check database logs
docker-compose restart db      # Restart database
```

### Containers Won't Start
```bash
docker-compose down
docker-compose up -d --build --force-recreate
```

### Check Health
```bash
./health-check.sh
./monitor.sh
```

## 📊 File Locations

```
VPS:
  Project:        /opt/multivendor_platform
  Backups:        /opt/multivendor_platform/backups
  Logs:           docker-compose logs
  
Docker Volumes:
  Database:       postgres_data
  Media:          media_files
  Static:         static_files
```

## 🔐 Security Checklist

- [x] SECRET_KEY configured
- [ ] DB_PASSWORD changed from default
- [ ] Firewall enabled (UFW)
- [ ] SSL certificate (if using domain)
- [ ] Regular backups enabled
- [ ] Monitoring configured

## 📞 Emergency Commands

### Quick Restart
```bash
cd /opt/multivendor_platform
docker-compose restart
```

### Full Rebuild
```bash
cd /opt/multivendor_platform
docker-compose down
docker-compose up -d --build
```

### Emergency Backup
```bash
cd /opt/multivendor_platform
./backup-database.sh
```

### Restore Last Backup
```bash
cd /opt/multivendor_platform
./restore-database.sh
# Then type: latest
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `START_DEPLOYMENT_HERE.md` | Complete deployment guide |
| `QUICK_START.md` | 5-minute deployment |
| `DEPLOYMENT_GUIDE.md` | Comprehensive reference |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step checklist |
| `README.md` | Project overview |
| `QUICK_REFERENCE.md` | This file |

## 🔄 Update Procedure

```bash
# Local machine
./deploy.sh

# VPS
ssh root@158.255.74.123
cd /opt/multivendor_platform
./update-app.sh
```

## 💾 Backup Schedule

Setup automated backups:
```bash
./setup-cron-backup.sh
```

Manual backup:
```bash
./backup-database.sh
```

## 🎯 Most Used Commands

```bash
# SSH to server
ssh root@158.255.74.123

# Go to project
cd /opt/multivendor_platform

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Backup
./backup-database.sh

# Health check
./health-check.sh
```

---

**Print this for quick reference!**




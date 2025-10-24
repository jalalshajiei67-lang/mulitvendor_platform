# ✅ Deployment Checklist

Use this checklist to ensure a smooth deployment.

## 📋 Pre-Deployment

### Local Machine Setup
- [ ] Project files are ready
- [ ] All changes committed (if using git)
- [ ] Run `./verify-setup.sh` to check files
- [ ] Environment file created: `copy .env.production .env` (Windows) or `cp .env.production .env` (Linux/Mac)
- [ ] Review `.env` file settings
- [ ] Update `DB_PASSWORD` to a secure password
- [ ] Verify `SECRET_KEY` is set (auto-generated)
- [ ] Update `ALLOWED_HOSTS` if using domain
- [ ] Test SSH connection: `./test-connection.sh`

### VPS Requirements
- [ ] VPS is accessible via SSH
- [ ] VPS has Ubuntu 20.04+ or compatible Linux
- [ ] Minimum 2GB RAM available
- [ ] Minimum 20GB disk space available
- [ ] Ports 22, 80, 443 available
- [ ] Root or sudo access available

### DNS Configuration (Optional)
- [ ] Domain purchased
- [ ] DNS A record pointing to VPS IP (158.255.74.123)
- [ ] DNS propagation completed (test with `nslookup yourdomain.com`)

---

## 🚀 Deployment

### Step 1: Upload Files to VPS
- [ ] **Windows**: Run `deploy-windows.bat`
- [ ] **Linux/Mac**: Run `./deploy.sh`
- [ ] **Or**: Run `./deploy-one-command.sh` for automated deployment
- [ ] Files uploaded successfully
- [ ] No errors during upload

### Step 2: VPS Setup
- [ ] SSH to VPS: `ssh root@158.255.74.123`
- [ ] Navigate to project: `cd /opt/multivendor_platform`
- [ ] Make scripts executable: `chmod +x *.sh`
- [ ] Run server setup: `./server-deploy.sh`
- [ ] Docker installed successfully
- [ ] Docker Compose installed successfully
- [ ] Firewall configured (UFW)
- [ ] Containers built successfully
- [ ] All containers started

### Step 3: Verify Containers
- [ ] Run `docker-compose ps` - all containers show "Up"
- [ ] Database container healthy
- [ ] Backend container running
- [ ] Frontend container running
- [ ] Nginx container running
- [ ] No error messages in `docker-compose logs`

---

## ⚙️ Initial Configuration

### Database Setup
- [ ] Migrations completed automatically
- [ ] Static files collected
- [ ] No database errors

### Create Admin User
- [ ] Run: `docker-compose exec backend python manage.py createsuperuser`
- [ ] Username created
- [ ] Email set
- [ ] Password set (remember this!)
- [ ] Superuser created successfully

### Test Application
- [ ] Frontend loads: http://158.255.74.123
- [ ] No console errors in browser
- [ ] Admin panel accessible: http://158.255.74.123/admin
- [ ] Can login to admin panel
- [ ] API responding: http://158.255.74.123/api
- [ ] Media files accessible: http://158.255.74.123/media
- [ ] Static files loading correctly

---

## 🔒 Security Configuration

### Basic Security
- [ ] Database password changed from default
- [ ] SECRET_KEY is secure (auto-generated)
- [ ] Firewall enabled and configured
- [ ] Only necessary ports open (22, 80, 443)
- [ ] DEBUG=False in .env

### SSL/HTTPS (If Using Domain)
- [ ] Domain DNS configured
- [ ] Run: `./setup-ssl.sh yourdomain.com`
- [ ] SSL certificate obtained
- [ ] HTTPS working: https://yourdomain.com
- [ ] HTTP redirects to HTTPS
- [ ] SSL auto-renewal configured

---

## 📊 Monitoring & Maintenance

### Setup Monitoring
- [ ] Test health check: `./health-check.sh`
- [ ] Test monitoring: `./monitor.sh`
- [ ] Review logs: `docker-compose logs`
- [ ] No critical errors in logs

### Setup Backups
- [ ] Test manual backup: `./backup-database.sh`
- [ ] Backup created successfully
- [ ] Backup file exists in `/opt/multivendor_platform/backups/`
- [ ] Setup automated backups: `./setup-cron-backup.sh`
- [ ] Cron job configured
- [ ] Test backup restoration (optional but recommended)

### Resource Monitoring
- [ ] Check CPU usage: `docker stats`
- [ ] Check memory usage: `free -h`
- [ ] Check disk space: `df -h`
- [ ] All resources within acceptable limits

---

## 🎨 Content Setup

### Admin Panel Configuration
- [ ] Login to admin panel
- [ ] Configure site settings
- [ ] Add initial categories
- [ ] Add initial products
- [ ] Upload vendor logos
- [ ] Test product creation
- [ ] Test image uploads
- [ ] Verify media files working

### Frontend Testing
- [ ] Homepage loads correctly
- [ ] Products display correctly
- [ ] Images load properly
- [ ] Navigation works
- [ ] Search functionality works
- [ ] API integration working
- [ ] No JavaScript errors

---

## 🔄 Ongoing Maintenance

### Daily Tasks
- [ ] Check application is accessible
- [ ] Review error logs if issues
- [ ] Monitor disk space

### Weekly Tasks
- [ ] Run `./health-check.sh`
- [ ] Verify backups are being created
- [ ] Review application logs
- [ ] Check for unusual activity

### Monthly Tasks
- [ ] Update system packages: `apt update && apt upgrade`
- [ ] Review backup strategy
- [ ] Check SSL certificate expiry (if using)
- [ ] Performance optimization review
- [ ] Security audit

### Quarterly Tasks
- [ ] Full backup test (restore to test environment)
- [ ] Update Docker images: `docker-compose pull`
- [ ] Review and update dependencies
- [ ] Security vulnerability scan

---

## 🆘 Emergency Procedures

### If Application Down
- [ ] Check container status: `docker-compose ps`
- [ ] Review logs: `docker-compose logs --tail=100`
- [ ] Run health check: `./health-check.sh`
- [ ] Restart services: `docker-compose restart`
- [ ] If persist, rebuild: `docker-compose down && docker-compose up -d --build`

### If Database Issues
- [ ] Check database container: `docker-compose logs db`
- [ ] Check database connection: `docker-compose exec db psql -U postgres`
- [ ] If corrupted, restore from backup: `./restore-database.sh`

### If Need to Rollback
- [ ] Stop current version: `docker-compose down`
- [ ] Restore database backup: `./restore-database.sh`
- [ ] Deploy previous version
- [ ] Test application
- [ ] Investigate issue

---

## 📞 Support Resources

### Documentation
- [ ] Read [START_DEPLOYMENT_HERE.md](START_DEPLOYMENT_HERE.md)
- [ ] Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [ ] Check [README.md](README.md)

### Commands Quick Reference
```bash
# SSH to VPS
ssh root@158.255.74.123

# Navigate to project
cd /opt/multivendor_platform

# Management interface
./manage-deployment.sh

# Health check
./health-check.sh

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Backup
./backup-database.sh
```

---

## ✅ Final Verification

### Application Status
- [ ] All containers running
- [ ] Frontend accessible
- [ ] Admin panel accessible
- [ ] API responding
- [ ] No errors in logs
- [ ] SSL configured (if applicable)
- [ ] Backups working
- [ ] Monitoring configured

### Documentation
- [ ] Credentials documented securely
- [ ] Important IPs/domains noted
- [ ] Emergency procedures understood
- [ ] Team members informed

### Handoff (If Applicable)
- [ ] Access credentials shared securely
- [ ] Documentation provided
- [ ] Training completed
- [ ] Support plan established

---

## 🎉 Deployment Complete!

Congratulations! Your multivendor platform is now deployed and running.

### Your Application:
- **Frontend**: http://158.255.74.123
- **Admin**: http://158.255.74.123/admin
- **API**: http://158.255.74.123/api

### Next Steps:
1. Add your content and products
2. Configure any additional settings
3. Monitor regularly
4. Keep backups current
5. Update as needed

---

**Date Deployed**: _______________  
**Deployed By**: _______________  
**Notes**: _______________________________________________

---

💡 **Tip**: Keep this checklist for future reference and for subsequent deployments or updates!




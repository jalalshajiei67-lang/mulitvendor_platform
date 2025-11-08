# 🚀 Quick Start - Deploy in 5 Minutes

## Step 1: Prepare Environment (1 minute)

```bash
# Copy environment template
cp env.template .env

# Edit .env file and set:
# - DB_PASSWORD (choose a secure password)
# - SECRET_KEY (generate using Python command below)
```

Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 2: Test Connection (30 seconds)

```bash
chmod +x test-connection.sh
./test-connection.sh
```

## Step 3: Deploy (2 minutes)

### On Windows:
```bash
deploy-windows.bat
```

### On Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

## Step 4: Start Services on VPS (1-2 minutes)

```bash
# SSH into VPS
ssh root@158.255.74.123

# Navigate to project
cd /opt/multivendor_platform

# Run deployment script
chmod +x server-deploy.sh
./server-deploy.sh
```

## Step 5: Create Admin User (30 seconds)

```bash
docker-compose exec backend python manage.py createsuperuser
```

## ✅ Done!

Your application is now running at:
- **Frontend**: http://158.255.74.123
- **Admin Panel**: http://158.255.74.123/admin
- **API**: http://158.255.74.123/api

---

## 📋 Management Interface

For easy management, use:

```bash
./manage-deployment.sh
```

This provides a menu for:
- Starting/stopping services
- Viewing logs
- Running migrations
- Database backups
- And more!

---

## 🔧 Common Commands

```bash
# View all logs
docker-compose logs -f

# Restart services
docker-compose restart

# Check status
docker-compose ps

# Monitor health
./monitor.sh
```

---

## 🆘 Need Help?

See `DEPLOYMENT_GUIDE.md` for detailed documentation.




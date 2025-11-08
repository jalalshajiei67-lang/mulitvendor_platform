# CapRover Fresh Installation Guide

This guide will help you remove the existing CapRover installation and install a fresh instance on your server (158.255.74.123).

## Prerequisites

- SSH access to server: `ssh root@158.255.74.123`
- CapRover CLI installed locally: `npm install -g caprover`
- Domain DNS records configured (indexo.ir)

## Quick Start (Windows)

If you're on Windows, use the automated script:

```powershell
.\caprover-fresh-install.bat
```

This will guide you through:
1. Removing CapRover
2. Installing fresh CapRover
3. Verifying installation

## Manual Steps

### Phase 1: Remove CapRover

#### Option A: Using the Script (Recommended)

1. Upload the removal script to your server:
```powershell
scp remove-caprover.sh root@158.255.74.123:/root/
```

2. SSH to server and run:
```powershell
ssh root@158.255.74.123
chmod +x /root/remove-caprover.sh
/root/remove-caprover.sh
```

#### Option B: Manual Removal

SSH to your server and run these commands:

```bash
ssh root@158.255.74.123

# Stop all containers
docker stop $(docker ps -q)

# Remove CapRover containers
docker rm -f $(docker ps -aq --filter "name=captain")

# Remove CapRover volumes
docker volume ls | grep captain | awk '{print $2}' | xargs docker volume rm

# Remove CapRover images
docker images | grep captain | awk '{print $3}' | xargs docker rmi -f

# Remove CapRover data directories
rm -rf /var/lib/docker/volumes/captain-data
rm -rf /captain

# Clean up Docker
docker container prune -f
docker volume prune -f
docker network prune -f
```

### Phase 2: Install Fresh CapRover

#### Option A: Using the Script (Recommended)

1. Upload the installation script:
```powershell
scp install-caprover.sh root@158.255.74.123:/root/
```

2. SSH to server and run:
```powershell
ssh root@158.255.74.123
chmod +x /root/install-caprover.sh
/root/install-caprover.sh
```

#### Option B: Manual Installation

SSH to your server and run:

```bash
ssh root@158.255.74.123

# Pull latest CapRover image
docker pull caprover/caprover

# Run CapRover
docker run -d \
    -p 80:80 \
    -p 443:443 \
    -p 3000:3000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /captain:/captain \
    --name captain-captain \
    --restart=always \
    caprover/caprover
```

Wait 1-2 minutes for CapRover to initialize.

### Phase 3: Initial CapRover Setup

1. **Access CapRover Dashboard:**
   - Open browser: `http://158.255.74.123:3000`
   - Or via domain: `http://captain.indexo.ir` (if DNS configured)

2. **Complete Initial Setup:**
   - Set root domain: `indexo.ir`
   - Set CapRover password (save this securely!)
   - Click "Save & Update"

3. **Verify Installation:**
   ```bash
   # Check container is running
   docker ps | grep captain
   
   # Check dashboard is accessible
   curl http://158.255.74.123:3000
   ```

### Phase 4: Configure CapRover CLI

1. **Login to CapRover:**
   ```powershell
   caprover login
   ```
   - Enter CapRover Machine: `https://captain.indexo.ir`
   - Enter Password: [your CapRover password]

2. **Verify Connection:**
   ```powershell
   caprover apps:list
   ```

### Phase 5: Recreate Apps

1. **Access Dashboard:**
   - Go to: `https://captain.indexo.ir`
   - Login with your password

2. **Create Apps:**
   - Click **"Apps"** in left sidebar
   - Click **"One-Click Apps/Databases"**
   - Find **PostgreSQL** and click **"Deploy"**
   - App Name: `postgres-db`
   - Click **"Deploy"**

   - Click **"Apps"** → **"One-Click Apps/Empty"**
   - App Name: `multivendor-backend`
   - Click **"Deploy"**

   - App Name: `multivendor-frontend`
   - Click **"Deploy"**

3. **Configure Apps:**
   Follow the detailed guide: `📱_DASHBOARD_CONFIGURATION_STEPS.md`

   Quick summary:
   - **postgres-db**: Set environment variables (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
   - **multivendor-backend**: Set all environment variables, add persistent directories, configure domain
   - **multivendor-frontend**: Set environment variables, configure domain

### Phase 6: Deploy Applications

1. **Deploy Backend:**
   ```powershell
   cd C:\Users\F003\Desktop\damirco
   caprover deploy -a multivendor-backend
   ```

2. **Deploy Frontend:**
   ```powershell
   caprover deploy -a multivendor-frontend
   ```

3. **Run Django Setup:**
   ```powershell
   # Run migrations
   caprover apps:exec multivendor-backend --command "python manage.py migrate"
   
   # Create superuser
   caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"
   
   # Collect static files
   caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
   ```

## Verification

1. **Check Apps Status:**
   ```powershell
   caprover apps:list
   ```

2. **Check Logs:**
   ```powershell
   caprover apps:logs multivendor-backend
   caprover apps:logs multivendor-frontend
   caprover apps:logs postgres-db
   ```

3. **Test Endpoints:**
   - Frontend: `https://indexo.ir`
   - Backend API: `https://multivendor-backend.indexo.ir/api`
   - Admin Panel: `https://multivendor-backend.indexo.ir/admin`

## Troubleshooting

### Issue: Cannot access CapRover dashboard after installation

- Check if container is running:
  ```bash
  ssh root@158.255.74.123
  docker ps | grep captain
  ```

- Check ports:
  ```bash
  netstat -tulpn | grep -E ':(80|443|3000)'
  ```

- Check firewall:
  ```bash
  ufw status
  # or
  iptables -L
  ```

- Wait a few minutes: CapRover takes 1-2 minutes to initialize

### Issue: Domain not working

- Verify DNS records point to server IP (158.255.74.123)
- Check DNS propagation:
  ```powershell
  nslookup captain.indexo.ir
  ```
- Wait for DNS propagation (can take up to 24 hours, usually much faster)

### Issue: SSL certificate not working

- SSL certificates are generated automatically by Let's Encrypt
- Wait 5-10 minutes after enabling HTTPS
- Make sure ports 80 and 443 are open
- Verify DNS records are correct

### Issue: Apps won't deploy

- Check if CapRover CLI is logged in:
  ```powershell
  caprover apps:list
  ```

- Verify app names match exactly (case-sensitive)
- Check logs in dashboard for errors

## Important Notes

- **DNS Configuration**: Ensure DNS records for `indexo.ir`, `captain.indexo.ir`, and `multivendor-backend.indexo.ir` point to 158.255.74.123
- **Firewall**: Ensure ports 80, 443, and 3000 are open
- **SSL Certificates**: Will be automatically generated by Let's Encrypt after domain configuration (takes 5-10 minutes)
- **Fresh Start**: No backup needed since project has no important data yet

## Files Reference

- `📱_DASHBOARD_CONFIGURATION_STEPS.md` - Complete dashboard configuration guide
- `🚀_CAPROVER_FRESH_SETUP_GUIDE.md` - Detailed setup instructions
- `caprover-env-backend.txt` - Backend environment variables
- `caprover-env-frontend.txt` - Frontend environment variables
- `remove-caprover.sh` - Automatic removal script
- `install-caprover.sh` - Automatic installation script
- `caprover-fresh-install.bat` - Windows automation script

## Quick Command Reference

```powershell
# Remove CapRover
ssh root@158.255.74.123 "bash -s" < remove-caprover.sh

# Install CapRover
ssh root@158.255.74.123 "bash -s" < install-caprover.sh

# Login to CapRover
caprover login

# Deploy apps
caprover deploy -a multivendor-backend
caprover deploy -a multivendor-frontend

# Check status
caprover apps:list
caprover apps:logs multivendor-backend
```


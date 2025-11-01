# CapRover Fresh Installation - Quick Reference

## Server Information
- **Server IP**: 158.255.74.123
- **SSH Command**: `ssh root@158.255.74.123`
- **Domain**: indexo.ir
- **CapRover Dashboard**: http://captain.indexo.ir

## Quick Start (Windows)

Run the automated script:
```powershell
.\caprover-fresh-install.bat
```

## Manual Steps

### 1. Remove CapRover

```powershell
# Upload and run removal script
scp remove-caprover.sh root@158.255.74.123:/root/
ssh root@158.255.74.123 "chmod +x /root/remove-caprover.sh && bash /root/remove-caprover.sh"
```

### 2. Install Fresh CapRover

```powershell
# Upload and run installation script
scp install-caprover.sh root@158.255.74.123:/root/
ssh root@158.255.74.123 "chmod +x /root/install-caprover.sh && bash /root/install-caprover.sh"
```

### 3. Initial Setup

1. Open browser: `http://158.255.74.123:3000`
2. Set root domain: `indexo.ir`
3. Set CapRover password
4. Save configuration

### 4. Login via CLI

```powershell
caprover login
# Enter: https://captain.indexo.ir
# Enter: [your password]
```

### 5. Create Apps

1. Go to dashboard: `https://captain.indexo.ir`
2. Create `postgres-db` (One-Click App: PostgreSQL)
3. Create `multivendor-backend` (Empty app)
4. Create `multivendor-frontend` (Empty app)

### 6. Configure Apps

Follow: `📱_DASHBOARD_CONFIGURATION_STEPS.md`

### 7. Deploy

```powershell
cd C:\Users\F003\Desktop\damirco
caprover deploy -a multivendor-backend
caprover deploy -a multivendor-frontend
```

### 8. Django Setup

```powershell
caprover apps:exec multivendor-backend --command "python manage.py migrate"
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput"
```

## Verification

```powershell
# Check apps
caprover apps:list

# Check logs
caprover apps:logs multivendor-backend
caprover apps:logs multivendor-frontend
caprover apps:logs postgres-db

# Test endpoints
# Frontend: https://indexo.ir
# Backend API: https://multivendor-backend.indexo.ir/api
# Admin: https://multivendor-backend.indexo.ir/admin
```

## Troubleshooting

**Dashboard not accessible?**
- Wait 2-3 minutes after installation
- Check: `ssh root@158.255.74.123 "docker ps | grep captain"`

**Apps won't deploy?**
- Verify logged in: `caprover apps:list`
- Check app names match exactly

**Domain not working?**
- Verify DNS points to 158.255.74.123
- Wait for DNS propagation

## Files Created

- `remove-caprover.sh` - Removal script
- `install-caprover.sh` - Installation script
- `caprover-fresh-install.bat` - Windows automation
- `CAPROVER_FRESH_INSTALL_GUIDE.md` - Complete guide


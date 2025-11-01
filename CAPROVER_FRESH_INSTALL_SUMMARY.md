# CapRover Fresh Installation - Implementation Summary

## Files Created

The following files have been created to help you remove and reinstall CapRover:

### Scripts

1. **`remove-caprover.sh`** - Bash script to remove CapRover from server
   - Stops all Docker containers
   - Removes CapRover containers, volumes, images, and data directories
   - Cleans up Docker system
   - Verifies removal

2. **`install-caprover.sh`** - Bash script to install fresh CapRover
   - Checks port availability
   - Pulls latest CapRover image
   - Runs CapRover container with proper configuration
   - Verifies installation

3. **`caprover-fresh-install.bat`** - Windows PowerShell script
   - Interactive menu for removal, installation, and verification
   - Handles file uploads and SSH connections
   - Provides guided workflow

### Documentation

1. **`CAPROVER_FRESH_INSTALL_GUIDE.md`** - Complete guide
   - Detailed step-by-step instructions
   - Manual and automated options
   - Troubleshooting section
   - Reference to existing configuration guides

2. **`CAPROVER_FRESH_INSTALL_QUICK.md`** - Quick reference
   - Command summary
   - Essential steps only
   - Quick troubleshooting tips

## Quick Start

### Option 1: Automated (Windows)

```powershell
# Run the interactive script
.\caprover-fresh-install.bat
```

Follow the menu prompts to:
1. Remove CapRover
2. Install fresh CapRover
3. Verify installation

### Option 2: Manual Steps

1. **Remove CapRover:**
   ```powershell
   scp remove-caprover.sh root@158.255.74.123:/root/
   ssh root@158.255.74.123 "chmod +x /root/remove-caprover.sh && bash /root/remove-caprover.sh"
   ```

2. **Install CapRover:**
   ```powershell
   scp install-caprover.sh root@158.255.74.123:/root/
   ssh root@158.255.74.123 "chmod +x /root/install-caprover.sh && bash /root/install-caprover.sh"
   ```

3. **Complete Setup:**
   - Open browser: `http://158.255.74.123:3000`
   - Set root domain: `indexo.ir`
   - Set CapRover password
   - Login via CLI: `caprover login`

4. **Recreate Apps:**
   - Follow: `📱_DASHBOARD_CONFIGURATION_STEPS.md`

## What Gets Removed

- All CapRover containers
- All CapRover volumes
- All CapRover images
- CapRover data directories (`/captain`, `/var/lib/docker/volumes/captain-data`)
- CapRover scripts

## What Gets Installed

- Fresh CapRover Docker container
- Latest CapRover image
- CapRover on ports 80, 443, 3000

## Next Steps After Installation

1. Complete initial CapRover setup (root domain, password)
2. Create apps: `postgres-db`, `multivendor-backend`, `multivendor-frontend`
3. Configure apps using `📱_DASHBOARD_CONFIGURATION_STEPS.md`
4. Deploy applications
5. Run Django setup commands

## Important Notes

- **No data backup**: Since you confirmed there's no important data, no backup is performed
- **Same server**: All operations target 158.255.74.123
- **Same domain**: Using indexo.ir (DNS must point to server IP)
- **Ports**: Ensure 80, 443, and 3000 are open in firewall

## Server Details

- **IP**: 158.255.74.123
- **SSH**: `ssh root@158.255.74.123`
- **Domain**: indexo.ir
- **CapRover Dashboard**: http://captain.indexo.ir

## Verification Commands

```powershell
# Check CapRover is running
ssh root@158.255.74.123 "docker ps | grep captain"

# Check dashboard
curl http://158.255.74.123:3000

# Login and verify
caprover login
caprover apps:list
```

## Troubleshooting

### Dashboard not accessible
- Wait 2-3 minutes after installation
- Check container: `ssh root@158.255.74.123 "docker ps | grep captain"`
- Check logs: `ssh root@158.255.74.123 "docker logs captain-captain"`

### Port conflicts
- Check ports: `ssh root@158.255.74.123 "netstat -tulpn | grep -E ':(80|443|3000)'"`
- Stop conflicting services if needed

### DNS issues
- Verify DNS records point to 158.255.74.123
- Check: `nslookup captain.indexo.ir`

## Related Files

- `📱_DASHBOARD_CONFIGURATION_STEPS.md` - App configuration guide
- `🚀_CAPROVER_FRESH_SETUP_GUIDE.md` - Detailed setup instructions
- `caprover-env-backend.txt` - Backend environment variables
- `caprover-env-frontend.txt` - Frontend environment variables

## Implementation Status

✅ Removal script created
✅ Installation script created
✅ Windows automation script created
✅ Complete guide created
✅ Quick reference created
✅ Scripts handle errors gracefully
✅ Verification steps included

All scripts are ready to use. Follow the Quick Start section above to begin the fresh installation process.


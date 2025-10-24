#!/bin/bash

# Setup Automated Daily Backups using Cron
# Run on VPS to configure automatic database backups

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="/opt/multivendor_platform"
BACKUP_SCRIPT="${SCRIPT_DIR}/backup-database.sh"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Setup Automated Backups (Cron)      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if backup script exists
if [ ! -f "$BACKUP_SCRIPT" ]; then
    echo -e "${RED}Backup script not found at $BACKUP_SCRIPT${NC}"
    exit 1
fi

# Make sure script is executable
chmod +x $BACKUP_SCRIPT

echo -e "${YELLOW}Setting up daily backup at 2 AM...${NC}"

# Create cron job
CRON_JOB="0 2 * * * cd ${SCRIPT_DIR} && ${BACKUP_SCRIPT} >> /var/log/multivendor-backup.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$BACKUP_SCRIPT"; then
    echo -e "${YELLOW}Cron job already exists. Updating...${NC}"
    (crontab -l 2>/dev/null | grep -v "$BACKUP_SCRIPT"; echo "$CRON_JOB") | crontab -
else
    echo -e "${YELLOW}Adding new cron job...${NC}"
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi

echo -e "${GREEN}✓ Automated backup configured${NC}"
echo ""
echo -e "${YELLOW}Backup Schedule:${NC}"
echo "  Time: 2:00 AM daily"
echo "  Location: /opt/multivendor_platform/backups/"
echo "  Retention: Last 7 backups"
echo "  Log: /var/log/multivendor-backup.log"
echo ""
echo -e "${YELLOW}Current cron jobs:${NC}"
crontab -l | grep -v "^#"
echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo -e "${YELLOW}To test backup manually:${NC}"
echo "  $BACKUP_SCRIPT"
echo ""
echo -e "${YELLOW}To view backup logs:${NC}"
echo "  tail -f /var/log/multivendor-backup.log"




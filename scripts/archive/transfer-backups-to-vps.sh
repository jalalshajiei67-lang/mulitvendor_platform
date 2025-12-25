#!/bin/bash

# Transfer Database and Static Files Backups to VPS
# Usage: ./transfer-backups-to-vps.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VPS_USER="deploy"
VPS_HOST="46.249.101.84"
VPS_BACKUP_DIR="/home/deploy/backups"
PROJECT_DIR="/media/jalal/New Volume/project/mulitvendor_platform"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Transfer Backups to VPS Script       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if files exist
echo -e "${YELLOW}Checking backup files...${NC}"

DB_BACKUP="${PROJECT_DIR}/database_backups/multivendor_db_backup.sql.gz"
STATIC_BACKUP="${PROJECT_DIR}/backend-deploy.tar.gz"

if [ ! -f "$DB_BACKUP" ]; then
    echo -e "${RED}✗ Database backup not found: $DB_BACKUP${NC}"
    exit 1
fi

if [ ! -f "$STATIC_BACKUP" ]; then
    echo -e "${YELLOW}⚠ Static files backup not found: $STATIC_BACKUP${NC}"
    echo -e "${YELLOW}  Continuing with database backup only...${NC}"
    STATIC_BACKUP=""
fi

# Display file sizes
echo -e "${BLUE}Backup files found:${NC}"
ls -lh "$DB_BACKUP" | awk '{print "  Database: " $9 " (" $5 ")"}'
if [ -n "$STATIC_BACKUP" ]; then
    ls -lh "$STATIC_BACKUP" | awk '{print "  Static:   " $9 " (" $5 ")"}'
fi
echo ""

# Test SSH connection
echo -e "${YELLOW}Testing SSH connection to ${VPS_USER}@${VPS_HOST}...${NC}"
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes "${VPS_USER}@${VPS_HOST}" exit 2>/dev/null; then
    echo -e "${RED}✗ Cannot connect to VPS. Please check:${NC}"
    echo -e "${RED}  1. SSH key is set up${NC}"
    echo -e "${RED}  2. VPS is accessible${NC}"
    echo -e "${RED}  3. User '${VPS_USER}' exists on VPS${NC}"
    exit 1
fi
echo -e "${GREEN}✓ SSH connection successful${NC}"
echo ""

# Create backup directory on VPS
echo -e "${YELLOW}Creating backup directory on VPS...${NC}"
ssh "${VPS_USER}@${VPS_HOST}" "mkdir -p ${VPS_BACKUP_DIR}"
echo -e "${GREEN}✓ Directory created: ${VPS_BACKUP_DIR}${NC}"
echo ""

# Transfer database backup
echo -e "${YELLOW}Transferring database backup...${NC}"
scp "$DB_BACKUP" "${VPS_USER}@${VPS_HOST}:${VPS_BACKUP_DIR}/"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database backup transferred successfully${NC}"
else
    echo -e "${RED}✗ Database backup transfer failed${NC}"
    exit 1
fi
echo ""

# Transfer static files backup if it exists
if [ -n "$STATIC_BACKUP" ]; then
    echo -e "${YELLOW}Transferring static files backup...${NC}"
    scp "$STATIC_BACKUP" "${VPS_USER}@${VPS_HOST}:${VPS_BACKUP_DIR}/"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Static files backup transferred successfully${NC}"
    else
        echo -e "${RED}✗ Static files backup transfer failed${NC}"
        exit 1
    fi
    echo ""
fi

# Verify files on VPS
echo -e "${YELLOW}Verifying files on VPS...${NC}"
ssh "${VPS_USER}@${VPS_HOST}" "ls -lh ${VPS_BACKUP_DIR}/"
echo ""

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Transfer Complete!                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Backups are now available on VPS at:${NC}"
echo -e "${BLUE}  ${VPS_BACKUP_DIR}${NC}"
echo ""
echo -e "${YELLOW}To restore database backup, SSH to VPS and run:${NC}"
echo -e "${YELLOW}  cd ${VPS_BACKUP_DIR}${NC}"
echo -e "${YELLOW}  gunzip -c multivendor_db_backup.sql.gz | docker exec -i <db-container> psql -U postgres multivendor_db${NC}"



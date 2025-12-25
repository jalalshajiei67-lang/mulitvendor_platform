#!/bin/bash

# Restore Backups to VPS Script
# This script transfers backups from local machine to VPS and restores them

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VPS_USER="root"
VPS_HOST="46.249.101.84"
VPS_BACKUP_DIR="/tmp/restore_backups"
PROJECT_DIR="/media/jalal/New Volume/project/mulitvendor_platform"
LOCAL_BACKUP_DIR="${PROJECT_DIR}/backups_from_vps"

# Docker volume paths
STATIC_PATH="/var/lib/docker/volumes/multivendor_platform_static_files/_data"
MEDIA_PATH="/var/lib/docker/volumes/multivendor_platform_media_files/_data"
DB_CONTAINER="multivendor_db"
DB_NAME="multivendor_db"
DB_USER="postgres"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Restore Backups to VPS Script         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if local backup files exist
echo -e "${YELLOW}Checking local backup files...${NC}"

DB_BACKUP="${LOCAL_BACKUP_DIR}/multivendor_db_backup_20251129.sql"
STATIC_BACKUP="${LOCAL_BACKUP_DIR}/static_files_backup_20251129.tar.gz"
MEDIA_BACKUP="${LOCAL_BACKUP_DIR}/media_files_backup_20251129.tar.gz"

if [ ! -f "$DB_BACKUP" ]; then
    echo -e "${RED}✗ Database backup not found: $DB_BACKUP${NC}"
    exit 1
fi

if [ ! -f "$STATIC_BACKUP" ]; then
    echo -e "${RED}✗ Static files backup not found: $STATIC_BACKUP${NC}"
    exit 1
fi

if [ ! -f "$MEDIA_BACKUP" ]; then
    echo -e "${RED}✗ Media files backup not found: $MEDIA_BACKUP${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All backup files found${NC}"
echo ""

# Display file sizes
echo -e "${BLUE}Backup files:${NC}"
ls -lh "$DB_BACKUP" "$STATIC_BACKUP" "$MEDIA_BACKUP" | awk '{print "  " $9 " (" $5 ")"}'
echo ""

# Test SSH connection
echo -e "${YELLOW}Testing SSH connection to ${VPS_USER}@${VPS_HOST}...${NC}"
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes "${VPS_USER}@${VPS_HOST}" exit 2>/dev/null; then
    echo -e "${RED}✗ Cannot connect to VPS. Please check SSH connection.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ SSH connection successful${NC}"
echo ""

# Create backup directory on VPS
echo -e "${YELLOW}Creating backup directory on VPS...${NC}"
ssh "${VPS_USER}@${VPS_HOST}" "mkdir -p ${VPS_BACKUP_DIR}"
echo -e "${GREEN}✓ Directory created: ${VPS_BACKUP_DIR}${NC}"
echo ""

# Transfer backups
echo -e "${YELLOW}Transferring backups to VPS...${NC}"
scp "$DB_BACKUP" "$STATIC_BACKUP" "$MEDIA_BACKUP" "${VPS_USER}@${VPS_HOST}:${VPS_BACKUP_DIR}/"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All backups transferred successfully${NC}"
else
    echo -e "${RED}✗ Backup transfer failed${NC}"
    exit 1
fi
echo ""

# Verify files on VPS
echo -e "${YELLOW}Verifying files on VPS...${NC}"
ssh "${VPS_USER}@${VPS_HOST}" "ls -lh ${VPS_BACKUP_DIR}/"
echo ""

# Warning
echo -e "${RED}╔════════════════════════════════════════╗${NC}"
echo -e "${RED}║   WARNING: DATA RESTORATION             ║${NC}"
echo -e "${RED}╚════════════════════════════════════════╝${NC}"
echo -e "${RED}This will overwrite existing data on VPS!${NC}"
echo -e "${RED}  - Database will be replaced${NC}"
echo -e "${RED}  - Static files will be replaced${NC}"
echo -e "${RED}  - Media files will be replaced${NC}"
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Restore cancelled${NC}"
    exit 0
fi
echo ""

# Restore Database
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 1: Restoring Database...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

ssh "${VPS_USER}@${VPS_HOST}" << 'ENDSSH'
set -e

VPS_BACKUP_DIR="/tmp/restore_backups"
DB_CONTAINER="multivendor_db"
BACKEND_CONTAINER="multivendor_backend"
DB_NAME="multivendor_db"
DB_USER="postgres"

# Check if container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${DB_CONTAINER}$"; then
    echo "⚠ Database container not found: ${DB_CONTAINER}"
    echo "Trying alternative container names..."
    DB_CONTAINER=$(docker ps -a --format '{{.Names}}' | grep -i postgres | head -1)
    if [ -z "$DB_CONTAINER" ]; then
        echo "✗ No PostgreSQL container found"
        exit 1
    fi
    echo "Using container: ${DB_CONTAINER}"
fi

# Stop backend to disconnect all database connections
echo "Stopping backend service to disconnect database connections..."
if docker ps --format '{{.Names}}' | grep -q "^${BACKEND_CONTAINER}$"; then
    docker stop ${BACKEND_CONTAINER} || true
    echo "✓ Backend stopped"
else
    echo "⚠ Backend container not running"
fi

# Wait a moment for connections to close
sleep 2

# Terminate all connections to the database
echo "Terminating all connections to database..."
docker exec ${DB_CONTAINER} psql -U ${DB_USER} -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${DB_NAME}' AND pid <> pg_backend_pid();" || true

# Get database password from environment (if available)
DB_PASSWORD=$(docker inspect ${DB_CONTAINER} --format '{{range .Config.Env}}{{println .}}{{end}}' | grep POSTGRES_PASSWORD | cut -d= -f2 || echo "")

echo "Dropping existing database..."
docker exec ${DB_CONTAINER} psql -U ${DB_USER} -c "DROP DATABASE IF EXISTS ${DB_NAME};" || true

echo "Creating new database..."
docker exec ${DB_CONTAINER} psql -U ${DB_USER} -c "CREATE DATABASE ${DB_NAME};"

echo "Restoring database from backup..."
if [ -n "$DB_PASSWORD" ]; then
    PGPASSWORD=${DB_PASSWORD} docker exec -i ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME} < ${VPS_BACKUP_DIR}/multivendor_db_backup_20251129.sql
else
    docker exec -i ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME} < ${VPS_BACKUP_DIR}/multivendor_db_backup_20251129.sql
fi

if [ $? -eq 0 ]; then
    echo "✓ Database restored successfully"
    
    # Restart backend
    echo "Starting backend service..."
    docker start ${BACKEND_CONTAINER} || true
else
    echo "✗ Database restore failed"
    # Restart backend even if restore failed
    docker start ${BACKEND_CONTAINER} || true
    exit 1
fi
ENDSSH

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database restoration complete${NC}"
else
    echo -e "${RED}✗ Database restoration failed${NC}"
    exit 1
fi
echo ""

# Restore Static Files
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2: Restoring Static Files...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

ssh "${VPS_USER}@${VPS_HOST}" << 'ENDSSH'
set -e

VPS_BACKUP_DIR="/tmp/restore_backups"
STATIC_PATH="/var/lib/docker/volumes/multivendor_platform_static_files/_data"

# Create directory if it doesn't exist
mkdir -p ${STATIC_PATH}

# Backup existing files (if any)
if [ -d "${STATIC_PATH}" ] && [ "$(ls -A ${STATIC_PATH} 2>/dev/null)" ]; then
    echo "Backing up existing static files..."
    mv ${STATIC_PATH} ${STATIC_PATH}.backup.$(date +%Y%m%d_%H%M%S) || true
fi

# Create fresh directory
mkdir -p ${STATIC_PATH}

# Extract backup
echo "Extracting static files backup..."
tar -xzf ${VPS_BACKUP_DIR}/static_files_backup_20251129.tar.gz -C ${STATIC_PATH} --strip-components=1 2>/dev/null || \
tar -xzf ${VPS_BACKUP_DIR}/static_files_backup_20251129.tar.gz -C ${STATIC_PATH}

# Fix permissions
chmod -R 755 ${STATIC_PATH}

echo "✓ Static files restored successfully"
ENDSSH

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Static files restoration complete${NC}"
else
    echo -e "${RED}✗ Static files restoration failed${NC}"
    exit 1
fi
echo ""

# Restore Media Files
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 3: Restoring Media Files...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

ssh "${VPS_USER}@${VPS_HOST}" << 'ENDSSH'
set -e

VPS_BACKUP_DIR="/tmp/restore_backups"
MEDIA_PATH="/var/lib/docker/volumes/multivendor_platform_media_files/_data"

# Create directory if it doesn't exist
mkdir -p ${MEDIA_PATH}

# Backup existing files (if any)
if [ -d "${MEDIA_PATH}" ] && [ "$(ls -A ${MEDIA_PATH} 2>/dev/null)" ]; then
    echo "Backing up existing media files..."
    mv ${MEDIA_PATH} ${MEDIA_PATH}.backup.$(date +%Y%m%d_%H%M%S) || true
fi

# Create fresh directory
mkdir -p ${MEDIA_PATH}

# Extract backup
echo "Extracting media files backup..."
tar -xzf ${VPS_BACKUP_DIR}/media_files_backup_20251129.tar.gz -C ${MEDIA_PATH} --strip-components=1 2>/dev/null || \
tar -xzf ${VPS_BACKUP_DIR}/media_files_backup_20251129.tar.gz -C ${MEDIA_PATH}

# Fix permissions
chmod -R 755 ${MEDIA_PATH}

echo "✓ Media files restored successfully"
ENDSSH

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Media files restoration complete${NC}"
else
    echo -e "${RED}✗ Media files restoration failed${NC}"
    exit 1
fi
echo ""

# Cleanup
echo -e "${YELLOW}Cleaning up temporary files...${NC}"
ssh "${VPS_USER}@${VPS_HOST}" "rm -rf ${VPS_BACKUP_DIR}"
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo ""

# Final summary
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Restore Complete!                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Restored:${NC}"
echo -e "${BLUE}  ✓ Database: ${DB_NAME}${NC}"
echo -e "${BLUE}  ✓ Static files: ${STATIC_PATH}${NC}"
echo -e "${BLUE}  ✓ Media files: ${MEDIA_PATH}${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "${YELLOW}  1. Restart backend app in CapRover dashboard${NC}"
echo -e "${YELLOW}  2. Verify data is accessible${NC}"
echo -e "${YELLOW}  3. Check application logs for any errors${NC}"


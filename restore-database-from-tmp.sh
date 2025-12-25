#!/bin/bash

# Restore Database from /tmp/database.sql on VPS
# This script restores the database backup that's already on the VPS

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VPS_USER="root"
VPS_HOST="46.249.101.84"
DB_BACKUP_FILE="/tmp/database.sql"
DB_CONTAINER="multivendor_db"
BACKEND_CONTAINER="multivendor_backend"
DB_NAME="multivendor_db"
DB_USER="postgres"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Restore Database from VPS             ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Verify backup file exists
echo -e "${YELLOW}Verifying backup file on VPS...${NC}"
if ! ssh "${VPS_USER}@${VPS_HOST}" "test -f ${DB_BACKUP_FILE}"; then
    echo -e "${RED}✗ Backup file not found: ${DB_BACKUP_FILE}${NC}"
    exit 1
fi

# Get file info
FILE_INFO=$(ssh "${VPS_USER}@${VPS_HOST}" "ls -lh ${DB_BACKUP_FILE}")
echo -e "${GREEN}✓ Backup file found${NC}"
echo -e "${BLUE}  ${FILE_INFO}${NC}"
echo ""

# Warning
echo -e "${RED}╔════════════════════════════════════════╗${NC}"
echo -e "${RED}║   WARNING: DATABASE RESTORATION          ║${NC}"
echo -e "${RED}╚════════════════════════════════════════╝${NC}"
echo -e "${RED}This will overwrite the existing database!${NC}"
echo -e "${RED}  - All current data will be lost${NC}"
echo -e "${RED}  - Database will be replaced with backup${NC}"
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Restore cancelled${NC}"
    exit 0
fi
echo ""

# Restore Database
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Restoring Database...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

ssh "${VPS_USER}@${VPS_HOST}" << ENDSSH
set -e

DB_BACKUP_FILE="/tmp/database.sql"
DB_CONTAINER="multivendor_db"
BACKEND_CONTAINER="multivendor_backend"
DB_NAME="multivendor_db"
DB_USER="postgres"

# Check if containers exist
if ! docker ps -a --format '{{.Names}}' | grep -q "^${DB_CONTAINER}$"; then
    echo "✗ Database container not found: ${DB_CONTAINER}"
    exit 1
fi

# Stop backend to disconnect all database connections
echo "Step 1: Stopping backend service..."
if docker ps --format '{{.Names}}' | grep -q "^${BACKEND_CONTAINER}$"; then
    docker stop ${BACKEND_CONTAINER}
    echo "✓ Backend stopped"
else
    echo "⚠ Backend container not running"
fi

# Wait a moment for connections to close
sleep 2

# Terminate all connections to the database
echo "Step 2: Terminating all database connections..."
docker exec ${DB_CONTAINER} psql -U ${DB_USER} -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${DB_NAME}' AND pid <> pg_backend_pid();" 2>/dev/null || true
echo "✓ Connections terminated"

# Get database password from environment (if available)
DB_PASSWORD=$(docker inspect ${DB_CONTAINER} --format '{{range .Config.Env}}{{println .}}{{end}}' | grep POSTGRES_PASSWORD | cut -d= -f2 || echo "")

# Drop existing database
echo "Step 3: Dropping existing database..."
docker exec ${DB_CONTAINER} psql -U ${DB_USER} -c "DROP DATABASE IF EXISTS ${DB_NAME};" || true
echo "✓ Database dropped"

# Create new database
echo "Step 4: Creating new database..."
docker exec ${DB_CONTAINER} psql -U ${DB_USER} -c "CREATE DATABASE ${DB_NAME};"
echo "✓ Database created"

# Restore database from backup
echo "Step 5: Restoring database from backup..."
echo "  This may take a few minutes..."
if [ -n "\${DB_PASSWORD}" ]; then
    PGPASSWORD=\${DB_PASSWORD} docker exec -i ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME} < ${DB_BACKUP_FILE}
else
    docker exec -i ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME} < ${DB_BACKUP_FILE}
fi

if [ \$? -eq 0 ]; then
    echo "✓ Database restored successfully"
    
    # Restart backend
    echo "Step 6: Starting backend service..."
    docker start ${BACKEND_CONTAINER} || true
    echo "✓ Backend started"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✓ Database restoration complete!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "✗ Database restore failed"
    # Restart backend even if restore failed
    docker start ${BACKEND_CONTAINER} || true
    exit 1
fi
ENDSSH

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Restore Complete!                    ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Database restored from: ${DB_BACKUP_FILE}${NC}"
    echo -e "${BLUE}Backend service has been restarted${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "${YELLOW}  1. Check backend logs: docker logs ${BACKEND_CONTAINER}${NC}"
    echo -e "${YELLOW}  2. Verify application is working${NC}"
    echo -e "${YELLOW}  3. Test database connection${NC}"
else
    echo ""
    echo -e "${RED}╔════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   Restore Failed!                      ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════╝${NC}"
    exit 1
fi

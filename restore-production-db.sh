#!/bin/bash

# Production Database Restore Script
# Run on VPS to restore PostgreSQL database from backup
# Works with docker-compose setup

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Production Database Restore Script         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ] && [ ! -f "docker-compose.production.yml" ]; then
    echo -e "${RED}✗ Error: docker-compose.yml not found!${NC}"
    echo -e "${YELLOW}  Please run this script from the project root directory${NC}"
    exit 1
fi

# Use docker-compose.yml if it exists, otherwise use production
COMPOSE_FILE="docker-compose.yml"
if [ ! -f "$COMPOSE_FILE" ] && [ -f "docker-compose.production.yml" ]; then
    COMPOSE_FILE="docker-compose.production.yml"
fi

# Check if database container is running
if ! docker ps --filter "name=multivendor_db" --format "{{.Names}}" | grep -q multivendor_db; then
    echo -e "${RED}✗ Database container is not running!${NC}"
    echo -e "${YELLOW}  Starting database container...${NC}"
    docker compose -f $COMPOSE_FILE up -d db
    echo -e "${YELLOW}  Waiting for database to be ready...${NC}"
    sleep 10
fi

# Check for backup files in common locations
BACKUP_LOCATIONS=(
    "/opt/multivendor_platform/backups"
    "/home/deploy/docker-deploy/database_backups"
    "/root/database_backups"
    "./database_backups"
    "."
)

BACKUP_DIR=""
for location in "${BACKUP_LOCATIONS[@]}"; do
    if [ -d "$location" ] && [ -n "$(ls -A $location/*.sql* 2>/dev/null)" ]; then
        BACKUP_DIR="$location"
        break
    fi
done

if [ -z "$BACKUP_DIR" ]; then
    echo -e "${YELLOW}No backup directory found. Checking current directory...${NC}"
    if [ -n "$(ls -A ./*.sql* 2>/dev/null)" ]; then
        BACKUP_DIR="."
    else
        echo -e "${RED}✗ No backup files found!${NC}"
        echo -e "${YELLOW}  Please provide the path to your backup file${NC}"
        read -p "Enter backup file path: " BACKUP_FILE
        if [ ! -f "$BACKUP_FILE" ]; then
            echo -e "${RED}✗ Backup file not found: $BACKUP_FILE${NC}"
            exit 1
        fi
    fi
fi

# List available backups
if [ -n "$BACKUP_DIR" ]; then
    echo -e "${YELLOW}Available backups in ${BACKUP_DIR}:${NC}"
    ls -lh ${BACKUP_DIR}/*.sql* 2>/dev/null | head -10
    echo ""
    read -p "Enter backup filename (or 'latest' for most recent, or full path): " BACKUP_INPUT
    
    if [ "$BACKUP_INPUT" == "latest" ]; then
        BACKUP_FILE=$(ls -t ${BACKUP_DIR}/*.sql* 2>/dev/null | head -1)
        echo -e "${YELLOW}Using latest backup: $(basename $BACKUP_FILE)${NC}"
    elif [ -f "$BACKUP_INPUT" ]; then
        BACKUP_FILE="$BACKUP_INPUT"
    elif [ -f "${BACKUP_DIR}/${BACKUP_INPUT}" ]; then
        BACKUP_FILE="${BACKUP_DIR}/${BACKUP_INPUT}"
    elif [ -f "${BACKUP_DIR}/${BACKUP_INPUT}.gz" ]; then
        BACKUP_FILE="${BACKUP_DIR}/${BACKUP_INPUT}.gz"
    else
        echo -e "${RED}✗ Backup file not found: $BACKUP_INPUT${NC}"
        exit 1
    fi
else
    BACKUP_FILE="$BACKUP_INPUT"
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}✗ Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

echo ""
echo -e "${RED}⚠ WARNING: This will overwrite the current database!${NC}"
echo -e "${YELLOW}  Backup file: $(basename $BACKUP_FILE)${NC}"
read -p "Are you sure you want to continue? (type 'yes' to confirm): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Restore cancelled${NC}"
    exit 0
fi

# Create backup of current database first
echo ""
echo -e "${YELLOW}[1/6] Creating backup of current database...${NC}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CURRENT_BACKUP="/tmp/multivendor_db_before_restore_${TIMESTAMP}.sql"
if docker exec multivendor_db psql -U postgres -lqt | cut -d \| -f 1 | grep -qw multivendor_db; then
    docker exec multivendor_db pg_dump -U postgres multivendor_db > "$CURRENT_BACKUP" 2>/dev/null || {
        echo -e "${YELLOW}  (Could not backup current database - it may be empty)${NC}"
    }
    if [ -f "$CURRENT_BACKUP" ] && [ -s "$CURRENT_BACKUP" ]; then
        echo -e "${GREEN}✓ Current database backed up to: $CURRENT_BACKUP${NC}"
    fi
else
    echo -e "${YELLOW}  (Database doesn't exist yet, skipping backup)${NC}"
fi

# Decompress if needed
echo ""
echo -e "${YELLOW}[2/6] Preparing backup file...${NC}"
RESTORE_FILE="/tmp/restore_${TIMESTAMP}.sql"
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo -e "${YELLOW}  Decompressing backup...${NC}"
    gunzip -c "$BACKUP_FILE" > "$RESTORE_FILE"
else
    echo -e "${YELLOW}  Copying backup file...${NC}"
    cp "$BACKUP_FILE" "$RESTORE_FILE"
fi

# Get database credentials from environment or docker-compose
DB_NAME="${DB_NAME:-multivendor_db}"
DB_USER="${DB_USER:-postgres}"

# Drop existing database
echo ""
echo -e "${YELLOW}[3/6] Dropping existing database (if exists)...${NC}"
docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS ${DB_NAME};" 2>/dev/null || true

# Create new database
echo ""
echo -e "${YELLOW}[4/6] Creating new database...${NC}"
docker exec multivendor_db psql -U postgres -c "CREATE DATABASE ${DB_NAME};"

# Restore database
echo ""
echo -e "${YELLOW}[5/6] Restoring database...${NC}"
cat "$RESTORE_FILE" | docker exec -i multivendor_db psql -U postgres -d ${DB_NAME}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database restored successfully!${NC}"
    
    # Clean up temp file
    rm -f "$RESTORE_FILE"
    
    # Restart backend to reconnect
    echo ""
    echo -e "${YELLOW}[6/6] Restarting backend service...${NC}"
    docker compose -f $COMPOSE_FILE restart backend || docker restart multivendor_backend
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Database Restore Complete!                  ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Check backend logs: docker logs multivendor_backend --tail 50"
    echo -e "  2. Verify connection: docker exec multivendor_backend python manage.py check --database default"
    echo -e "  3. Run migrations if needed: docker exec multivendor_backend python manage.py migrate"
else
    echo -e "${RED}✗ Restore failed!${NC}"
    rm -f "$RESTORE_FILE"
    exit 1
fi



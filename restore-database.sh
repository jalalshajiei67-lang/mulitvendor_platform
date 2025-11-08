#!/bin/bash

# Database Restore Script
# Run on VPS to restore PostgreSQL database from backup

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BACKUP_DIR="/opt/multivendor_platform/backups"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Database Restore Script            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# List available backups
echo -e "${YELLOW}Available backups:${NC}"
ls -lh ${BACKUP_DIR}/multivendor_db_*.sql.gz 2>/dev/null || {
    echo -e "${RED}No backups found in ${BACKUP_DIR}${NC}"
    exit 1
}

echo ""
read -p "Enter backup filename (or 'latest' for most recent): " BACKUP_FILE

if [ "$BACKUP_FILE" == "latest" ]; then
    BACKUP_FILE=$(ls -t ${BACKUP_DIR}/multivendor_db_*.sql.gz | head -1)
    echo -e "${YELLOW}Using latest backup: $(basename $BACKUP_FILE)${NC}"
elif [ ! -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
    # Try adding .gz if not present
    if [ -f "${BACKUP_DIR}/${BACKUP_FILE}.gz" ]; then
        BACKUP_FILE="${BACKUP_DIR}/${BACKUP_FILE}.gz"
    else
        BACKUP_FILE="${BACKUP_DIR}/${BACKUP_FILE}"
    fi
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

echo ""
echo -e "${RED}WARNING: This will overwrite the current database!${NC}"
read -p "Are you sure you want to continue? (type 'yes' to confirm): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Restore cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}Creating backup of current database...${NC}"
./backup-database.sh

echo ""
echo -e "${YELLOW}Decompressing backup...${NC}"
gunzip -c $BACKUP_FILE > /tmp/restore.sql

echo -e "${YELLOW}Dropping existing database...${NC}"
docker-compose exec -T db psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;"

echo -e "${YELLOW}Creating new database...${NC}"
docker-compose exec -T db psql -U postgres -c "CREATE DATABASE multivendor_db;"

echo -e "${YELLOW}Restoring database...${NC}"
cat /tmp/restore.sql | docker-compose exec -T db psql -U postgres -d multivendor_db

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database restored successfully!${NC}"
    rm /tmp/restore.sql
    
    echo ""
    echo -e "${YELLOW}Restarting services...${NC}"
    docker-compose restart backend
    
    echo -e "${GREEN}✓ Restore complete${NC}"
else
    echo -e "${RED}✗ Restore failed${NC}"
    rm /tmp/restore.sql
    exit 1
fi




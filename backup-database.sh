#!/bin/bash

# Database Backup Script
# Run on VPS to backup PostgreSQL database

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BACKUP_DIR="/opt/multivendor_platform/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="multivendor_db_${TIMESTAMP}.sql"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Database Backup Script             ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

echo -e "${YELLOW}Creating backup...${NC}"
docker-compose exec -T db pg_dump -U postgres multivendor_db > ${BACKUP_DIR}/${BACKUP_FILE}

if [ $? -eq 0 ]; then
    # Compress backup
    echo -e "${YELLOW}Compressing backup...${NC}"
    gzip ${BACKUP_DIR}/${BACKUP_FILE}
    
    BACKUP_SIZE=$(du -h ${BACKUP_DIR}/${BACKUP_FILE}.gz | cut -f1)
    
    echo -e "${GREEN}✓ Backup created successfully!${NC}"
    echo -e "${GREEN}  File: ${BACKUP_FILE}.gz${NC}"
    echo -e "${GREEN}  Size: ${BACKUP_SIZE}${NC}"
    echo -e "${GREEN}  Location: ${BACKUP_DIR}/${NC}"
    
    # Keep only last 7 backups
    echo -e "\n${YELLOW}Cleaning old backups (keeping last 7)...${NC}"
    cd ${BACKUP_DIR}
    ls -t multivendor_db_*.sql.gz | tail -n +8 | xargs -r rm
    
    echo -e "${GREEN}✓ Cleanup complete${NC}"
    echo ""
    echo -e "${YELLOW}Available backups:${NC}"
    ls -lh ${BACKUP_DIR}/multivendor_db_*.sql.gz 2>/dev/null || echo "No backups found"
else
    echo -e "${RED}✗ Backup failed${NC}"
    exit 1
fi




#!/bin/bash

# Bash Script to Download Online Database to Local Project
# Usage: ./download-database.sh

set -e

# Configuration
SERVER_IP="${SERVER_IP:-185.208.172.76}"
DB_NAME="${DB_NAME:-multivendor_db}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^}"
DB_PORT="${DB_PORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-./database_backups}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Download Online Database to Local    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if pg_dump is available
if ! command -v pg_dump &> /dev/null; then
    echo -e "${YELLOW}⚠️  pg_dump not found. Checking Docker method...${NC}"
    
    if command -v docker &> /dev/null; then
        echo -e "${CYAN}Using Docker method instead...${NC}"
        docker run --rm -e PGPASSWORD="$DB_PASSWORD" \
            postgres:15-alpine \
            pg_dump -h "$SERVER_IP" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -F p \
            > "$BACKUP_DIR/multivendor_db_$(date +%Y%m%d_%H%M%S).sql"
    else
        echo -e "${RED}❌ pg_dump not found and Docker is not available.${NC}"
        echo -e "${YELLOW}Please install PostgreSQL client tools or Docker.${NC}"
        exit 1
    fi
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/multivendor_db_${TIMESTAMP}.sql"

echo ""
echo -e "${YELLOW}📥 Downloading database from server...${NC}"
echo -e "   Server: $SERVER_IP"
echo -e "   Database: $DB_NAME"
echo ""

# Export password for pg_dump
export PGPASSWORD="$DB_PASSWORD"

# Download database
if pg_dump -h "$SERVER_IP" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -F p -f "$BACKUP_FILE"; then
    echo -e "${GREEN}✓ Database downloaded successfully!${NC}"
else
    echo -e "${RED}❌ Direct connection failed.${NC}"
    echo ""
    echo -e "${CYAN}📋 Alternative methods:${NC}"
    echo ""
    echo -e "${YELLOW}Method 1: SSH into server${NC}"
    echo "  ssh root@$SERVER_IP"
    echo "  docker exec srv-captain--postgres-db pg_dump -U postgres multivendor_db > backup.sql"
    echo "  scp root@$SERVER_IP:/root/backup.sql ."
    echo ""
    echo -e "${YELLOW}Method 2: Use CapRover dashboard${NC}"
    echo "  1. Open https://captain.indexo.ir"
    echo "  2. Go to postgres-db app"
    echo "  3. Use terminal/one-click command to export"
    echo ""
    exit 1
fi

# Compress backup
echo ""
echo -e "${YELLOW}📦 Compressing backup...${NC}"
if command -v gzip &> /dev/null; then
    gzip "$BACKUP_FILE"
    BACKUP_FILE="${BACKUP_FILE}.gz"
    echo -e "${GREEN}✓ Backup compressed${NC}"
else
    echo -e "${YELLOW}⚠️  gzip not found, keeping uncompressed file${NC}"
fi

FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo ""
echo -e "${GREEN}✅ Backup completed successfully!${NC}"
echo -e "   File: $BACKUP_FILE"
echo -e "   Size: $FILE_SIZE"
echo ""

# Ask if user wants to restore
read -p "$(echo -e ${CYAN}Do you want to restore this backup to your local database? [y/N]: ${NC})" restore

if [[ $restore =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}🔄 Restoring to local database...${NC}"
    
    # Check if Docker is running
    if ! docker ps &> /dev/null; then
        echo -e "${RED}❌ Docker is not running.${NC}"
        exit 1
    fi
    
    # Check if local database container exists
    if ! docker ps -a --filter "name=multivendor_db" --format "{{.Names}}" | grep -q multivendor_db; then
        echo -e "${YELLOW}⚠️  Starting local database container...${NC}"
        docker-compose up -d db
        sleep 5
    fi
    
    # Decompress if needed
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        echo -e "${YELLOW}📦 Decompressing backup...${NC}"
        RESTORE_FILE="${BACKUP_FILE%.gz}"
        gunzip -c "$BACKUP_FILE" > "$RESTORE_FILE"
    else
        RESTORE_FILE="$BACKUP_FILE"
    fi
    
    echo -e "${YELLOW}🗑️  Dropping existing local database...${NC}"
    docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;" || true
    
    echo -e "${YELLOW}➕ Creating new local database...${NC}"
    docker exec multivendor_db psql -U postgres -c "CREATE DATABASE multivendor_db;"
    
    echo -e "${YELLOW}📥 Restoring backup...${NC}"
    cat "$RESTORE_FILE" | docker exec -i multivendor_db psql -U postgres -d multivendor_db
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Local database restored successfully!${NC}"
        if [[ "$RESTORE_FILE" != "$BACKUP_FILE" ]]; then
            rm "$RESTORE_FILE"
        fi
    else
        echo -e "${RED}❌ Restore failed${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}✨ Done!${NC}"





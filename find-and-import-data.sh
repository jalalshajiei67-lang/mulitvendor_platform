#!/bin/bash

# Script to find backup files and help import data to staging

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Find & Import Data to Staging         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Find backup files
echo -e "${YELLOW}Step 1: Searching for backup files...${NC}"
echo ""

BACKUP_LOCATIONS=(
    "/opt/multivendor_platform/backups"
    "/root"
    "/root/indexo-staging"
    "/root/backups"
    "/var/backups"
    "/tmp"
)

FOUND_BACKUPS=()

for location in "${BACKUP_LOCATIONS[@]}"; do
    if [ -d "$location" ]; then
        echo -e "${BLUE}Checking: $location${NC}"
        # Find .sql and .sql.gz files
        while IFS= read -r file; do
            if [ -n "$file" ]; then
                FOUND_BACKUPS+=("$file")
                SIZE=$(du -h "$file" | cut -f1)
                echo -e "  ${GREEN}✓ Found: $(basename $file) (${SIZE})${NC}"
            fi
        done < <(find "$location" -maxdepth 2 -type f \( -name "*.sql" -o -name "*.sql.gz" \) 2>/dev/null)
    fi
done

echo ""
if [ ${#FOUND_BACKUPS[@]} -eq 0 ]; then
    echo -e "${YELLOW}No backup files found.${NC}"
else
    echo -e "${GREEN}Found ${#FOUND_BACKUPS[@]} backup file(s)${NC}"
fi

# Step 2: Check for production database
echo ""
echo -e "${YELLOW}Step 2: Checking for production database...${NC}"
echo ""

PROD_CONTAINERS=$(docker ps -a --format "{{.Names}}" | grep -E "multivendor_db|postgres" | grep -v staging || true)

if [ -n "$PROD_CONTAINERS" ]; then
    echo -e "${GREEN}Found potential production databases:${NC}"
    echo "$PROD_CONTAINERS" | while read container; do
        echo -e "  ${BLUE}→ $container${NC}"
    done
else
    echo -e "${YELLOW}No production database containers found${NC}"
fi

# Step 3: Options
echo ""
echo -e "${YELLOW}Step 3: Choose an option:${NC}"
echo ""
echo "1) Import from backup file (if found above)"
echo "2) Copy from production database"
echo "3) Create backup from production first, then import"
echo "4) Exit"
echo ""

read -p "Enter option (1-4): " OPTION

case $OPTION in
    1)
        if [ ${#FOUND_BACKUPS[@]} -eq 0 ]; then
            echo -e "${RED}No backup files found!${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${YELLOW}Available backups:${NC}"
        for i in "${!FOUND_BACKUPS[@]}"; do
            echo "  $((i+1))) ${FOUND_BACKUPS[$i]}"
        done
        
        read -p "Enter backup number: " BACKUP_NUM
        BACKUP_INDEX=$((BACKUP_NUM - 1))
        
        if [ $BACKUP_INDEX -lt 0 ] || [ $BACKUP_INDEX -ge ${#FOUND_BACKUPS[@]} ]; then
            echo -e "${RED}Invalid selection${NC}"
            exit 1
        fi
        
        BACKUP_FILE="${FOUND_BACKUPS[$BACKUP_INDEX]}"
        
        echo ""
        echo -e "${YELLOW}⚠️  WARNING: This will overwrite staging database!${NC}"
        read -p "Continue? (type 'yes'): " CONFIRM
        
        if [ "$CONFIRM" != "yes" ]; then
            echo "Cancelled"
            exit 0
        fi
        
        echo ""
        echo -e "${YELLOW}Creating backup of current staging database...${NC}"
        docker exec multivendor_db_staging pg_dump -U postgres multivendor_db_staging > /tmp/staging_backup_$(date +%Y%m%d_%H%M%S).sql || true
        
        echo -e "${YELLOW}Dropping staging database...${NC}"
        docker exec multivendor_db_staging psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db_staging;"
        
        echo -e "${YELLOW}Creating fresh staging database...${NC}"
        docker exec multivendor_db_staging psql -U postgres -c "CREATE DATABASE multivendor_db_staging;"
        
        if [[ "$BACKUP_FILE" == *.gz ]]; then
            echo -e "${YELLOW}Decompressing and importing...${NC}"
            gunzip -c "$BACKUP_FILE" | docker exec -i multivendor_db_staging psql -U postgres -d multivendor_db_staging
        else
            echo -e "${YELLOW}Importing...${NC}"
            cat "$BACKUP_FILE" | docker exec -i multivendor_db_staging psql -U postgres -d multivendor_db_staging
        fi
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}✅ Data imported successfully!${NC}"
        else
            echo -e "${RED}❌ Import failed${NC}"
            exit 1
        fi
        ;;
        
    2)
        if [ -z "$PROD_CONTAINERS" ]; then
            echo -e "${RED}No production database found!${NC}"
            exit 1
        fi
        
        echo ""
        echo "Available production databases:"
        echo "$PROD_CONTAINERS" | nl -w2 -s') '
        read -p "Enter container number: " CONTAINER_NUM
        
        PROD_CONTAINER=$(echo "$PROD_CONTAINERS" | sed -n "${CONTAINER_NUM}p")
        
        if [ -z "$PROD_CONTAINER" ]; then
            echo -e "${RED}Invalid selection${NC}"
            exit 1
        fi
        
        read -p "Enter production database name (default: multivendor_db): " PROD_DB_NAME
        PROD_DB_NAME=${PROD_DB_NAME:-multivendor_db}
        
        echo ""
        echo -e "${YELLOW}⚠️  WARNING: This will overwrite staging database!${NC}"
        read -p "Continue? (type 'yes'): " CONFIRM
        
        if [ "$CONFIRM" != "yes" ]; then
            echo "Cancelled"
            exit 0
        fi
        
        echo ""
        echo -e "${YELLOW}Creating backup of current staging database...${NC}"
        docker exec multivendor_db_staging pg_dump -U postgres multivendor_db_staging > /tmp/staging_backup_$(date +%Y%m%d_%H%M%S).sql || true
        
        echo -e "${YELLOW}Dumping production database...${NC}"
        docker exec $PROD_CONTAINER pg_dump -U postgres $PROD_DB_NAME > /tmp/prod_dump.sql
        
        echo -e "${YELLOW}Dropping staging database...${NC}"
        docker exec multivendor_db_staging psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db_staging;"
        
        echo -e "${YELLOW}Creating fresh staging database...${NC}"
        docker exec multivendor_db_staging psql -U postgres -c "CREATE DATABASE multivendor_db_staging;"
        
        echo -e "${YELLOW}Importing production data...${NC}"
        cat /tmp/prod_dump.sql | docker exec -i multivendor_db_staging psql -U postgres -d multivendor_db_staging
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}✅ Data imported successfully!${NC}"
            rm /tmp/prod_dump.sql
        else
            echo -e "${RED}❌ Import failed${NC}"
            exit 1
        fi
        ;;
        
    3)
        if [ -z "$PROD_CONTAINERS" ]; then
            echo -e "${RED}No production database found!${NC}"
            exit 1
        fi
        
        echo ""
        echo "Available production databases:"
        echo "$PROD_CONTAINERS" | nl -w2 -s') '
        read -p "Enter container number: " CONTAINER_NUM
        
        PROD_CONTAINER=$(echo "$PROD_CONTAINERS" | sed -n "${CONTAINER_NUM}p")
        
        if [ -z "$PROD_CONTAINER" ]; then
            echo -e "${RED}Invalid selection${NC}"
            exit 1
        fi
        
        read -p "Enter production database name (default: multivendor_db): " PROD_DB_NAME
        PROD_DB_NAME=${PROD_DB_NAME:-multivendor_db}
        
        BACKUP_FILE="/root/prod_backup_$(date +%Y%m%d_%H%M%S).sql"
        
        echo ""
        echo -e "${YELLOW}Creating backup from production...${NC}"
        docker exec $PROD_CONTAINER pg_dump -U postgres $PROD_DB_NAME > $BACKUP_FILE
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Backup created: $BACKUP_FILE${NC}"
            echo ""
            echo "Now you can import it using option 1, or continue now..."
            read -p "Import now? (y/n): " IMPORT_NOW
            
            if [[ $IMPORT_NOW =~ ^[Yy]$ ]]; then
                echo ""
                echo -e "${YELLOW}Dropping staging database...${NC}"
                docker exec multivendor_db_staging psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db_staging;"
                
                echo -e "${YELLOW}Creating fresh staging database...${NC}"
                docker exec multivendor_db_staging psql -U postgres -c "CREATE DATABASE multivendor_db_staging;"
                
                echo -e "${YELLOW}Importing...${NC}"
                cat $BACKUP_FILE | docker exec -i multivendor_db_staging psql -U postgres -d multivendor_db_staging
                
                if [ $? -eq 0 ]; then
                    echo ""
                    echo -e "${GREEN}✅ Data imported successfully!${NC}"
                else
                    echo -e "${RED}❌ Import failed${NC}"
                    exit 1
                fi
            fi
        else
            echo -e "${RED}❌ Backup failed${NC}"
            exit 1
        fi
        ;;
        
    4)
        echo "Exiting..."
        exit 0
        ;;
        
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Done!${NC}"
echo ""
echo "Next steps:"
echo "1. Restart backend: docker restart multivendor_backend_staging"
echo "2. Check website: https://staging.indexo.ir"
echo "3. Access admin: https://api-staging.indexo.ir/admin/"


#!/bin/bash

# Script to import data into staging database
# Options: Copy from production, restore from backup, or create test data

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Import Data to Staging Database      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

echo "Choose an option:"
echo ""
echo "1) Copy data from PRODUCTION database (if available)"
echo "2) Restore from backup file (.sql or .sql.gz)"
echo "3) Create test data using Django management commands"
echo "4) Exit"
echo ""
read -p "Enter option (1-4): " OPTION

case $OPTION in
    1)
        echo ""
        echo -e "${YELLOW}Copying data from production database...${NC}"
        echo ""
        
        # Check if production database container exists
        PROD_DB_CONTAINER=$(docker ps -a --filter "name=multivendor_db" --format "{{.Names}}" | grep -v staging | head -1)
        
        if [ -z "$PROD_DB_CONTAINER" ]; then
            echo -e "${RED}❌ Production database container not found${NC}"
            echo "Looking for containers with 'multivendor_db' in name (excluding staging)..."
            docker ps -a | grep multivendor_db | grep -v staging || echo "No production database found"
            exit 1
        fi
        
        echo -e "${BLUE}Found production database: $PROD_DB_CONTAINER${NC}"
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
        docker exec $PROD_DB_CONTAINER pg_dump -U postgres $PROD_DB_NAME > /tmp/prod_dump.sql
        
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
        
    2)
        echo ""
        read -p "Enter path to backup file (.sql or .sql.gz): " BACKUP_FILE
        
        if [ ! -f "$BACKUP_FILE" ]; then
            echo -e "${RED}❌ File not found: $BACKUP_FILE${NC}"
            exit 1
        fi
        
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
        
    3)
        echo ""
        echo -e "${YELLOW}Creating test data...${NC}"
        echo ""
        echo "This will use Django management commands to create sample data."
        echo "Make sure you have management commands for creating test data."
        echo ""
        
        # Check if there's a management command for creating test data
        if docker exec multivendor_backend_staging python manage.py help | grep -q "create_test_data\|create_fake_data"; then
            echo -e "${YELLOW}Running test data creation command...${NC}"
            docker exec multivendor_backend_staging python manage.py create_test_data || \
            docker exec multivendor_backend_staging python manage.py create_fake_data
        else
            echo -e "${YELLOW}No test data command found. Creating a superuser...${NC}"
            echo "You can create test data manually through Django admin or API."
            echo ""
            read -p "Create superuser? (y/n): " CREATE_SUPERUSER
            if [[ $CREATE_SUPERUSER =~ ^[Yy]$ ]]; then
                docker exec -it multivendor_backend_staging python manage.py createsuperuser
            fi
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


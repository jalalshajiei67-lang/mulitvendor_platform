#!/bin/bash

# Script to fix staging volume issue and restore data

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Fix Staging Volume & Restore Data   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Check current volume
echo -e "${YELLOW}Step 1: Checking current database volume...${NC}"
CURRENT_VOLUME=$(docker inspect multivendor_db_staging --format='{{range .Mounts}}{{if eq .Destination "/var/lib/postgresql/data"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")

if [ -n "$CURRENT_VOLUME" ]; then
    echo -e "${BLUE}Current volume: $CURRENT_VOLUME${NC}"
    
    # Check if it has data
    TABLE_COUNT=$(docker exec multivendor_db_staging psql -U postgres -d multivendor_db_staging -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")
    echo "  Tables in current database: $TABLE_COUNT"
    
    if [ "$TABLE_COUNT" -gt "10" ]; then
        echo -e "${GREEN}✅ Current database has data!${NC}"
        echo "Your data is already there. The issue might be elsewhere."
        exit 0
    fi
else
    echo -e "${RED}❌ Could not find current volume${NC}"
fi

echo ""

# Step 2: Find all postgres volumes
echo -e "${YELLOW}Step 2: Finding all PostgreSQL staging volumes...${NC}"
ALL_VOLUMES=$(docker volume ls --format "{{.Name}}" | grep -iE "(postgres|staging)" || true)

if [ -z "$ALL_VOLUMES" ]; then
    echo -e "${RED}❌ No volumes found${NC}"
    exit 1
fi

echo "Found volumes:"
for vol in $ALL_VOLUMES; do
    SIZE=$(docker volume inspect "$vol" --format '{{.Mountpoint}}' 2>/dev/null | xargs du -sh 2>/dev/null | cut -f1 || echo "unknown")
    echo "  - $vol (size: $SIZE)"
done
echo ""

# Step 3: Find volume with data (indexo-staging_postgres_data_staging)
echo -e "${YELLOW}Step 3: Looking for volume with old data...${NC}"
OLD_VOLUME="indexo-staging_postgres_data_staging"

if docker volume inspect "$OLD_VOLUME" >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Found old volume: $OLD_VOLUME${NC}"
    
    # Check if it has data by creating temp container
    echo "Checking if volume has data..."
    TEMP_CONTAINER="temp_vol_check_$(date +%s)"
    
    docker run --rm \
        -v "$OLD_VOLUME:/data" \
        alpine sh -c "test -d /data/base && echo 'has_data' || echo 'empty'" > /tmp/vol_check.txt 2>&1 || echo "error" > /tmp/vol_check.txt
    
    if grep -q "has_data" /tmp/vol_check.txt; then
        echo -e "${GREEN}✓ Volume contains database files${NC}"
        echo ""
        echo -e "${YELLOW}⚠️  WARNING: This will replace the current database!${NC}"
        read -p "Restore data from $OLD_VOLUME? (type 'yes'): " CONFIRM
        
        if [ "$CONFIRM" = "yes" ]; then
            echo ""
            echo -e "${YELLOW}Stopping current database container...${NC}"
            docker stop multivendor_db_staging || true
            docker rm multivendor_db_staging || true
            
            echo -e "${YELLOW}Starting database with old volume...${NC}"
            docker run -d \
                --name multivendor_db_staging \
                --network multivendor_network \
                -v "$OLD_VOLUME:/var/lib/postgresql/data" \
                -e POSTGRES_DB=multivendor_db_staging \
                -e POSTGRES_USER=postgres \
                -e POSTGRES_PASSWORD=MySecurePassword123! \
                --health-cmd="pg_isready -U postgres -d multivendor_db_staging" \
                --health-interval=10s \
                --health-timeout=5s \
                --health-retries=5 \
                postgres:15-alpine
            
            echo "Waiting for database to start..."
            sleep 15
            
            # Verify data
            TABLE_COUNT=$(docker exec multivendor_db_staging psql -U postgres -d multivendor_db_staging -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")
            USER_COUNT=$(docker exec multivendor_db_staging psql -U postgres -d multivendor_db_staging -t -c "SELECT COUNT(*) FROM auth_user;" 2>/dev/null | tr -d ' ' || echo "0")
            
            if [ "$TABLE_COUNT" -gt "10" ]; then
                echo ""
                echo -e "${GREEN}✅ Data restored successfully!${NC}"
                echo "  Tables: $TABLE_COUNT"
                echo "  Users: $USER_COUNT"
                echo ""
                echo -e "${YELLOW}Restarting backend to pick up the data...${NC}"
                docker restart multivendor_backend_staging
                echo ""
                echo -e "${GREEN}✅ Done! Your old data should now be visible.${NC}"
            else
                echo -e "${RED}❌ Volume appears to be empty${NC}"
            fi
            
            rm -f /tmp/vol_check.txt
            exit 0
        else
            echo "Restore cancelled."
            rm -f /tmp/vol_check.txt
            exit 0
        fi
    else
        echo -e "${YELLOW}⚠️  Volume exists but appears empty${NC}"
    fi
    rm -f /tmp/vol_check.txt
else
    echo -e "${YELLOW}⚠️  Old volume not found: $OLD_VOLUME${NC}"
    echo ""
    echo "Available volumes:"
    for vol in $ALL_VOLUMES; do
        echo "  - $vol"
    done
fi

echo ""
echo -e "${YELLOW}If you have a backup file, you can restore it manually:${NC}"
echo "  gunzip -c /path/to/backup.sql.gz | docker exec -i multivendor_db_staging psql -U postgres -d multivendor_db_staging"


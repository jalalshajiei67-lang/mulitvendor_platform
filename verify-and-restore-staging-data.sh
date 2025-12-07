#!/bin/bash

# Script to verify staging data and restore if needed

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Verify & Restore Staging Data       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Check which volume the database is using
echo -e "${YELLOW}Step 1: Checking database volume...${NC}"
DB_VOLUME=$(docker inspect multivendor_db_staging --format='{{range .Mounts}}{{if eq .Destination "/var/lib/postgresql/data"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")

if [ -z "$DB_VOLUME" ]; then
    echo -e "${RED}❌ Could not find database volume${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Database is using volume: $DB_VOLUME${NC}"
echo ""

# Step 2: Check if database has data
echo -e "${YELLOW}Step 2: Checking if database has data...${NC}"
TABLE_COUNT=$(docker exec multivendor_db_staging psql -U postgres -d multivendor_db_staging -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")
USER_COUNT=$(docker exec multivendor_db_staging psql -U postgres -d multivendor_db_staging -t -c "SELECT COUNT(*) FROM auth_user;" 2>/dev/null | tr -d ' ' || echo "0")

echo "  Tables: $TABLE_COUNT"
echo "  Users: $USER_COUNT"
echo ""

if [ "$TABLE_COUNT" -gt "10" ] && [ "$USER_COUNT" -gt "0" ]; then
    echo -e "${GREEN}✅ Database has data!${NC}"
    echo ""
    echo "Your data is safe. The database contains:"
    echo "  - $TABLE_COUNT tables"
    echo "  - $USER_COUNT users"
    exit 0
fi

# Step 3: Find old volume with data
echo -e "${YELLOW}Step 3: Looking for old volume with data...${NC}"
echo ""

OLD_VOLUMES=$(docker volume ls --format "{{.Name}}" | grep -E "(postgres.*staging|indexo.*postgres)" || true)

if [ -z "$OLD_VOLUMES" ]; then
    echo -e "${YELLOW}⚠️  No old volumes found${NC}"
    echo "This might be a fresh deployment."
    exit 0
fi

echo "Found potential old volumes:"
for vol in $OLD_VOLUMES; do
    echo "  - $vol"
done
echo ""

# Step 4: Check if any old volume has data
echo -e "${YELLOW}Step 4: Checking old volumes for data...${NC}"
echo ""

for vol in $OLD_VOLUMES; do
    if [ "$vol" != "$DB_VOLUME" ]; then
        echo "Checking volume: $vol"
        # Create temporary container to check volume
        TEMP_CONTAINER="temp_check_$(date +%s)"
        docker run --rm -v "$vol:/data" alpine sh -c "ls -la /data/base 2>/dev/null | head -5" > /tmp/vol_check_$TEMP_CONTAINER 2>&1 || true
        
        if grep -q "total" /tmp/vol_check_$TEMP_CONTAINER 2>/dev/null; then
            echo -e "  ${GREEN}✓ Volume $vol contains database files${NC}"
            echo ""
            echo -e "${YELLOW}Would you like to restore data from $vol?${NC}"
            read -p "Type 'yes' to restore: " RESTORE
            
            if [ "$RESTORE" = "yes" ]; then
                echo ""
                echo -e "${YELLOW}Restoring data from $vol...${NC}"
                
                # Stop current database
                docker stop multivendor_db_staging
                docker rm multivendor_db_staging
                
                # Start new container with old volume
                docker run -d \
                    --name multivendor_db_staging \
                    --network multivendor_network \
                    -v "$vol:/var/lib/postgresql/data" \
                    -e POSTGRES_DB=multivendor_db_staging \
                    -e POSTGRES_USER=postgres \
                    -e POSTGRES_PASSWORD=MySecurePassword123! \
                    postgres:15-alpine
                
                echo "Waiting for database to start..."
                sleep 10
                
                # Verify data
                NEW_TABLE_COUNT=$(docker exec multivendor_db_staging psql -U postgres -d multivendor_db_staging -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")
                
                if [ "$NEW_TABLE_COUNT" -gt "10" ]; then
                    echo -e "${GREEN}✅ Data restored successfully!${NC}"
                    echo "  Tables: $NEW_TABLE_COUNT"
                    
                    # Restart backend
                    echo ""
                    echo "Restarting backend..."
                    docker restart multivendor_backend_staging
                    
                    echo ""
                    echo -e "${GREEN}✅ Done! Your data should now be visible.${NC}"
                else
                    echo -e "${RED}❌ Restore failed - volume might be empty${NC}"
                fi
                
                rm -f /tmp/vol_check_$TEMP_CONTAINER
                exit 0
            fi
        fi
        rm -f /tmp/vol_check_$TEMP_CONTAINER
    fi
done

echo ""
echo -e "${YELLOW}⚠️  No data found in old volumes${NC}"
echo "This appears to be a fresh database."


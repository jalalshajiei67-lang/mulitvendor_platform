#!/bin/bash
# Comprehensive VPS debugging and fix script
# Run this on your VPS: bash debug-and-fix-vps.sh

set -e

echo "=========================================="
echo "🔍 VPS Database Debugging & Fix Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Step 1: Check current directory and files
echo -e "${BLUE}[1/10] Checking environment...${NC}"
if [ ! -f "docker-compose.production.yml" ]; then
    echo -e "${RED}❌ Error: Not in project directory!${NC}"
    echo "   Please run: cd ~/multivendor_platform"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ In correct directory${NC}"
echo ""

# Step 2: Read current .env configuration
echo -e "${BLUE}[2/10] Reading .env configuration...${NC}"
DB_NAME=$(grep "^DB_NAME=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
DB_USER=$(grep "^DB_USER=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
DB_PASSWORD=$(grep "^DB_PASSWORD=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
DB_HOST=$(grep "^DB_HOST=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)

DB_USER=${DB_USER:-postgres}
DB_NAME=${DB_NAME:-multivendor_db}
DB_HOST=${DB_HOST:-db}

echo "   DB_NAME: $DB_NAME"
echo "   DB_USER: $DB_USER"
echo "   DB_HOST: $DB_HOST"
echo "   DB_PASSWORD: ${DB_PASSWORD:0:10}***"
echo ""

# Step 3: Check Docker containers
echo -e "${BLUE}[3/10] Checking Docker containers...${NC}"
DB_CONTAINER=$(docker ps --filter "name=multivendor_db" --format "{{.Names}}" | head -n 1)
BACKEND_CONTAINER=$(docker ps --filter "name=multivendor_backend" --format "{{.Names}}" | head -n 1)

if [ -z "$DB_CONTAINER" ]; then
    echo -e "${RED}❌ Database container not running!${NC}"
    echo "   Starting database container..."
    docker compose -f docker-compose.production.yml up -d db
    sleep 5
    DB_CONTAINER=$(docker ps --filter "name=multivendor_db" --format "{{.Names}}" | head -n 1)
    if [ -z "$DB_CONTAINER" ]; then
        echo -e "${RED}❌ Could not start database container${NC}"
        exit 1
    fi
fi

if [ -z "$BACKEND_CONTAINER" ]; then
    echo -e "${YELLOW}⚠️  Backend container not running${NC}"
else
    echo -e "${GREEN}✅ Backend container: $BACKEND_CONTAINER${NC}"
fi

echo -e "${GREEN}✅ Database container: $DB_CONTAINER${NC}"
echo ""

# Step 4: Check database container status
echo -e "${BLUE}[4/10] Checking database container health...${NC}"
DB_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$DB_CONTAINER" 2>/dev/null || echo "unknown")
echo "   Database status: $DB_STATUS"

if [ "$DB_STATUS" != "healthy" ] && [ "$DB_STATUS" != "running" ]; then
    echo -e "${YELLOW}⚠️  Database container is not healthy${NC}"
    echo "   Checking logs..."
    docker logs "$DB_CONTAINER" --tail 20
fi
echo ""

# Step 5: Test database connection with current password
echo -e "${BLUE}[5/10] Testing database connection with current .env password...${NC}"
if [ -n "$DB_PASSWORD" ]; then
    if docker exec -e PGPASSWORD="$DB_PASSWORD" "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Password is correct! Database connection successful.${NC}"
        echo ""
        echo -e "${GREEN}✅ No password fix needed. Restarting backend...${NC}"
        if [ -n "$BACKEND_CONTAINER" ]; then
            docker restart "$BACKEND_CONTAINER"
            echo -e "${GREEN}✅ Backend restarted${NC}"
        fi
        exit 0
    else
        echo -e "${RED}❌ Password mismatch! Connection failed.${NC}"
        echo "   The password in .env doesn't match the database password."
    fi
else
    echo -e "${RED}❌ DB_PASSWORD is empty in .env file${NC}"
    exit 1
fi
echo ""

# Step 6: Try to connect without password (to see if trust auth works)
echo -e "${BLUE}[6/10] Testing if we can connect without password...${NC}"
if docker exec "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Can connect without password (trust auth enabled)${NC}"
    CAN_RESET_PASSWORD=true
else
    echo -e "${YELLOW}⚠️  Cannot connect without password${NC}"
    CAN_RESET_PASSWORD=false
fi
echo ""

# Step 7: Check what password the database actually has
echo -e "${BLUE}[7/10] Attempting to reset password...${NC}"

if [ "$CAN_RESET_PASSWORD" = true ]; then
    echo "   Resetting password directly..."
    docker exec "$DB_CONTAINER" psql -U "$DB_USER" -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" && {
        echo -e "${GREEN}✅ Password reset successful!${NC}"
        sleep 2
        # Test again
        if docker exec -e PGPASSWORD="$DB_PASSWORD" "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Verified: New password works!${NC}"
        fi
    } || {
        echo -e "${YELLOW}⚠️  Direct reset failed, trying alternative method...${NC}"
        CAN_RESET_PASSWORD=false
    }
fi

# Step 8: Alternative method - modify pg_hba.conf
if [ "$CAN_RESET_PASSWORD" = false ]; then
    echo -e "${BLUE}[8/10] Using alternative method: Modifying pg_hba.conf...${NC}"
    
    echo "   Stopping database container..."
    docker stop "$DB_CONTAINER"
    
    # Get volume name
    VOLUME_NAME=$(docker inspect "$DB_CONTAINER" --format '{{ range .Mounts }}{{ if eq .Destination "/var/lib/postgresql/data" }}{{ .Name }}{{ end }}{{ end }}')
    
    if [ -z "$VOLUME_NAME" ]; then
        echo -e "${RED}❌ Could not find PostgreSQL data volume${NC}"
        echo "   Starting database container..."
        docker start "$DB_CONTAINER"
        exit 1
    fi
    
    echo "   Found volume: $VOLUME_NAME"
    echo "   Enabling trust authentication temporarily..."
    
    # Modify pg_hba.conf
    docker run --rm \
        -v "$VOLUME_NAME:/var/lib/postgresql/data" \
        postgres:15-alpine \
        sh -c "
            cp /var/lib/postgresql/data/pg_hba.conf /var/lib/postgresql/data/pg_hba.conf.backup 2>/dev/null || true
            echo 'local   all             all                                     trust' > /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             127.0.0.1/32            trust' >> /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             ::1/128                 trust' >> /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/postgresql/data/pg_hba.conf
        "
    
    echo "   Starting database container..."
    docker start "$DB_CONTAINER"
    
    echo "   Waiting for database to be ready..."
    sleep 5
    for i in {1..30}; do
        if docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" > /dev/null 2>&1; then
            break
        fi
        echo "      Waiting... ($i/30)"
        sleep 1
    done
    
    echo "   Resetting password..."
    docker exec "$DB_CONTAINER" psql -U "$DB_USER" -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" || {
        echo -e "${RED}❌ Failed to reset password${NC}"
        docker start "$DB_CONTAINER"
        exit 1
    }
    
    echo "   Restoring secure authentication..."
    docker stop "$DB_CONTAINER"
    
    docker run --rm \
        -v "$VOLUME_NAME:/var/lib/postgresql/data" \
        postgres:15-alpine \
        sh -c "
            if [ -f /var/lib/postgresql/data/pg_hba.conf.backup ]; then
                cp /var/lib/postgresql/data/pg_hba.conf.backup /var/lib/postgresql/data/pg_hba.conf
            else
                echo 'local   all             all                                     md5' > /var/lib/postgresql/data/pg_hba.conf
                echo 'host    all             all             127.0.0.1/32            md5' >> /var/lib/postgresql/data/pg_hba.conf
                echo 'host    all             all             ::1/128                 md5' >> /var/lib/postgresql/data/pg_hba.conf
                echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/postgresql/data/pg_hba.conf
            fi
        "
    
    echo "   Starting database with new password..."
    docker start "$DB_CONTAINER"
    sleep 3
fi

# Step 9: Verify password works
echo -e "${BLUE}[9/10] Verifying password...${NC}"
if docker exec -e PGPASSWORD="$DB_PASSWORD" "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Password verification successful!${NC}"
else
    echo -e "${RED}❌ Password verification failed${NC}"
    echo "   Please check the password manually"
    exit 1
fi
echo ""

# Step 10: Restart backend and check status
echo -e "${BLUE}[10/10] Restarting backend container...${NC}"
if [ -n "$BACKEND_CONTAINER" ]; then
    docker restart "$BACKEND_CONTAINER"
    echo -e "${GREEN}✅ Backend container restarted${NC}"
    
    echo ""
    echo "   Waiting for backend to initialize..."
    sleep 10
    
    echo ""
    echo "   Backend container status:"
    docker ps --filter "name=multivendor_backend" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    echo "   Recent backend logs:"
    docker logs "$BACKEND_CONTAINER" --tail 30 2>&1 | tail -20
else
    echo -e "${YELLOW}⚠️  Backend container not found${NC}"
    echo "   Starting backend..."
    docker compose -f docker-compose.production.yml up -d backend
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Debugging and fix complete!${NC}"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Database password has been reset to match .env file"
echo "  - Backend container has been restarted"
echo "  - Check the logs above for any remaining issues"
echo ""
echo "To check backend health:"
echo "  docker ps | grep multivendor_backend"
echo "  docker logs multivendor_backend --tail 50"
echo ""


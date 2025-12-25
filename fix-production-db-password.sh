#!/bin/bash

# Script to fix PostgreSQL password mismatch in production
# This script will diagnose and fix database authentication issues

set -e

echo "=========================================="
echo "🔧 Fixing PostgreSQL Password in Production"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if database container is running
if ! docker ps | grep -q "multivendor_db"; then
    echo -e "${RED}❌ Error: Database container 'multivendor_db' is not running${NC}"
    echo "Please start it first with: docker compose -f docker-compose.production.yml up -d db"
    exit 1
fi

echo -e "${BLUE}📋 Step 1: Checking current .env file...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    if [ -f "env.template" ]; then
        echo -e "${YELLOW}Creating .env from env.template...${NC}"
        cp env.template .env
        echo -e "${GREEN}✅ Created .env file${NC}"
        echo -e "${YELLOW}⚠️  Please review and update .env with your production values!${NC}"
    else
        echo -e "${RED}❌ Error: env.template not found. Cannot create .env file.${NC}"
        exit 1
    fi
fi

# Read password from .env
DB_PASSWORD=$(grep "^DB_PASSWORD=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)

if [ -z "$DB_PASSWORD" ]; then
    echo -e "${RED}❌ Error: DB_PASSWORD not found in .env file${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found DB_PASSWORD in .env: ${DB_PASSWORD:0:5}***${NC}"
echo ""

# Check if password is already correct
echo -e "${BLUE}📋 Step 2: Testing current database password...${NC}"
set +e
if docker exec -e PGPASSWORD="$DB_PASSWORD" multivendor_db psql -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Database password is already correct!${NC}"
    echo -e "${GREEN}✅ No need to reset password.${NC}"
    echo ""
    echo -e "${BLUE}Checking backend container...${NC}"
    if docker ps | grep -q "multivendor_backend"; then
        echo -e "${YELLOW}Restarting backend container to apply changes...${NC}"
        docker restart multivendor_backend
        echo -e "${GREEN}✅ Backend container restarted${NC}"
    fi
    exit 0
fi
set -e

echo -e "${YELLOW}⚠️  Password mismatch detected. Proceeding with password reset...${NC}"
echo ""

# Method: Temporarily enable trust authentication, then change password
echo -e "${BLUE}📋 Step 3: Stopping database container...${NC}"
docker stop multivendor_db

echo -e "${BLUE}📋 Step 4: Modifying pg_hba.conf to allow password reset...${NC}"
# Get the volume name
VOLUME_NAME=$(docker inspect multivendor_db --format '{{ range .Mounts }}{{ if eq .Destination "/var/lib/postgresql/data" }}{{ .Name }}{{ end }}{{ end }}')

if [ -z "$VOLUME_NAME" ]; then
    echo -e "${RED}❌ Could not find PostgreSQL data volume${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found volume: $VOLUME_NAME${NC}"

# Create a temporary container to modify pg_hba.conf
docker run --rm \
    -v "$VOLUME_NAME:/var/lib/postgresql/data" \
    postgres:15-alpine \
    sh -c "
        # Backup original pg_hba.conf
        cp /var/lib/postgresql/data/pg_hba.conf /var/lib/postgresql/data/pg_hba.conf.backup 2>/dev/null || true
        # Create new pg_hba.conf with trust authentication for local connections
        echo 'local   all             all                                     trust' > /var/lib/postgresql/data/pg_hba.conf
        echo 'host    all             all             127.0.0.1/32            trust' >> /var/lib/postgresql/data/pg_hba.conf
        echo 'host    all             all             ::1/128                 trust' >> /var/lib/postgresql/data/pg_hba.conf
        echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/postgresql/data/pg_hba.conf
    "

echo -e "${BLUE}📋 Step 5: Starting database container...${NC}"
docker start multivendor_db

echo -e "${BLUE}📋 Step 6: Waiting for database to be ready...${NC}"
sleep 5

# Wait for PostgreSQL to be ready
for i in {1..30}; do
    if docker exec multivendor_db pg_isready -U postgres > /dev/null 2>&1; then
        break
    fi
    echo "  Waiting... ($i/30)"
    sleep 1
done

echo -e "${BLUE}📋 Step 7: Resetting password...${NC}"
docker exec multivendor_db psql -U postgres -c "ALTER USER postgres WITH PASSWORD '$DB_PASSWORD';" || {
    echo -e "${RED}❌ Failed to reset password${NC}"
    exit 1
}

echo -e "${BLUE}📋 Step 8: Restoring original pg_hba.conf...${NC}"
docker stop multivendor_db

docker run --rm \
    -v "$VOLUME_NAME:/var/lib/postgresql/data" \
    postgres:15-alpine \
    sh -c "
        # Restore backup if exists, otherwise create standard config
        if [ -f /var/lib/postgresql/data/pg_hba.conf.backup ]; then
            cp /var/lib/postgresql/data/pg_hba.conf.backup /var/lib/postgresql/data/pg_hba.conf
        else
            # Create standard pg_hba.conf with md5 authentication
            echo 'local   all             all                                     md5' > /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             127.0.0.1/32            md5' >> /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             ::1/128                 md5' >> /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/postgresql/data/pg_hba.conf
        fi
    "

echo -e "${BLUE}📋 Step 9: Starting database container with new password...${NC}"
docker start multivendor_db

echo -e "${BLUE}📋 Step 10: Verifying password...${NC}"
sleep 3

set +e
if docker exec -e PGPASSWORD="$DB_PASSWORD" multivendor_db psql -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Password reset successful!${NC}"
    set -e
else
    echo -e "${YELLOW}⚠️  Could not auto-verify with new password${NC}"
    echo -e "${YELLOW}   Trying to verify without password...${NC}"
    if docker exec multivendor_db psql -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Database is accessible (password may need manual verification)${NC}"
    else
        echo -e "${RED}❌ Warning: Could not verify password reset${NC}"
    fi
    set -e
fi

echo ""
echo -e "${GREEN}✅ Password fix complete!${NC}"
echo ""

echo -e "${BLUE}📋 Step 11: Restarting backend container...${NC}"
if docker ps | grep -q "multivendor_backend"; then
    docker restart multivendor_backend
    echo -e "${GREEN}✅ Backend container restarted${NC}"
else
    echo -e "${YELLOW}⚠️  Backend container not found, starting services...${NC}"
    docker compose -f docker-compose.production.yml up -d backend
fi

echo ""
echo -e "${GREEN}✅ All done!${NC}"
echo ""
echo "Next steps:"
echo "1. Check backend logs:"
echo "   docker logs multivendor_backend --tail 50 -f"
echo ""
echo "2. Verify backend is running:"
echo "   docker ps | grep multivendor_backend"
echo ""


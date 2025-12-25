#!/bin/bash

# Quick diagnostic and fix script for production database password issue
# Run this on your VPS server

set -e

echo "=========================================="
echo "🔍 Quick Database Password Diagnostic"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "docker-compose.production.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.production.yml not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo -e "${BLUE}1. Checking containers...${NC}"
if docker ps | grep -q "multivendor_db"; then
    echo -e "${GREEN}✅ Database container is running${NC}"
else
    echo -e "${RED}❌ Database container is not running${NC}"
    exit 1
fi

if docker ps | grep -q "multivendor_backend"; then
    BACKEND_STATUS=$(docker ps --filter "name=multivendor_backend" --format "{{.Status}}")
    echo -e "${YELLOW}⚠️  Backend container status: $BACKEND_STATUS${NC}"
else
    echo -e "${RED}❌ Backend container is not running${NC}"
fi

echo ""
echo -e "${BLUE}2. Checking .env file...${NC}"
if [ -f ".env" ]; then
    DB_PASSWORD=$(grep "^DB_PASSWORD=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
    if [ -z "$DB_PASSWORD" ]; then
        echo -e "${RED}❌ DB_PASSWORD not found in .env${NC}"
    else
        echo -e "${GREEN}✅ DB_PASSWORD found: ${DB_PASSWORD:0:5}***${NC}"
    fi
else
    echo -e "${RED}❌ .env file not found${NC}"
    echo "Creating from template..."
    if [ -f "env.template" ]; then
        cp env.template .env
        echo -e "${GREEN}✅ Created .env from template${NC}"
        echo -e "${YELLOW}⚠️  Please review .env file before continuing${NC}"
    else
        echo -e "${RED}❌ env.template not found${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}3. Testing database connection...${NC}"
if [ ! -z "$DB_PASSWORD" ]; then
    set +e
    if docker exec -e PGPASSWORD="$DB_PASSWORD" multivendor_db psql -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Database connection successful!${NC}"
        echo -e "${GREEN}✅ Password is correct${NC}"
        set -e
        echo ""
        echo -e "${BLUE}4. Checking backend logs...${NC}"
        echo "Last 20 lines of backend logs:"
        echo "----------------------------------------"
        docker logs multivendor_backend --tail 20 2>&1 | tail -20
        echo ""
        echo -e "${YELLOW}If backend is still failing, try restarting it:${NC}"
        echo "  docker restart multivendor_backend"
        exit 0
    else
        echo -e "${RED}❌ Database connection failed!${NC}"
        echo -e "${YELLOW}⚠️  Password mismatch detected${NC}"
        set -e
    fi
else
    echo -e "${YELLOW}⚠️  Cannot test connection (no DB_PASSWORD)${NC}"
fi

echo ""
echo -e "${BLUE}4. Summary${NC}"
echo "----------------------------------------"
echo "Issue: Database password authentication failed"
echo "Solution: Run the fix script:"
echo ""
echo -e "${GREEN}  ./fix-production-db-password.sh${NC}"
echo ""
echo "Or manually fix by:"
echo "  1. Ensure .env file has correct DB_PASSWORD"
echo "  2. Run: docker compose -f docker-compose.production.yml down db"
echo "  3. Remove the database volume (if safe to do so) OR"
echo "  4. Run the fix-production-db-password.sh script"
echo ""


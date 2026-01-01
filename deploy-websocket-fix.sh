#!/bin/bash

# Deploy WebSocket and 403 Error Fixes
# This script applies fixes for WebSocket connection refused and 403 errors

set -e

echo "=========================================="
echo "Deploying WebSocket and 403 Error Fixes"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're on the server
if [ ! -f "docker-compose.production.yml" ]; then
    echo -e "${RED}Error: docker-compose.production.yml not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo -e "${YELLOW}Step 1: Pulling latest changes...${NC}"
git pull origin main || echo "Warning: Could not pull latest changes"

echo ""
echo -e "${YELLOW}Step 2: Rebuilding backend container with fixes...${NC}"
docker-compose -f docker-compose.production.yml build backend

echo ""
echo -e "${YELLOW}Step 3: Restarting backend container...${NC}"
docker-compose -f docker-compose.production.yml up -d backend

echo ""
echo -e "${YELLOW}Step 4: Waiting for backend to be healthy...${NC}"
sleep 10

# Check if backend is healthy
if docker ps | grep -q "multivendor_backend.*healthy"; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Backend might still be starting...${NC}"
    echo "Checking logs..."
    docker logs multivendor_backend --tail 20
fi

echo ""
echo -e "${YELLOW}Step 5: Verifying fixes...${NC}"

# Check if Daphne is running
if docker exec multivendor_backend ps aux | grep -q daphne; then
    echo -e "${GREEN}✅ Daphne (ASGI server) is running${NC}"
else
    echo -e "${RED}❌ Daphne is not running${NC}"
fi

# Check environment variables
echo ""
echo "Checking environment variables:"
docker exec multivendor_backend env | grep -E "ALLOWED_HOSTS|CORS_ALLOW" | head -5

echo ""
echo -e "${GREEN}=========================================="
echo "Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test WebSocket connection in browser console"
echo "2. Test API endpoint: curl -H 'Authorization: Token YOUR_TOKEN' https://multivendor-backend.indexo.ir/api/auth/buyer/orders/"
echo "3. Check logs: docker logs multivendor_backend --tail 50"
echo ""


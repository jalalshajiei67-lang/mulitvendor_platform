#!/bin/bash
# Local test script to reproduce and fix 502 errors
# This simulates the production setup locally

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Local 502 Error Test & Fix${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.simple.yml" ]; then
    echo -e "${RED}✗ docker-compose.simple.yml not found${NC}"
    echo "   Please run this script from the project root"
    exit 1
fi

# Step 1: Start services
echo -e "${YELLOW}[1/5] Starting services with docker-compose...${NC}"
docker-compose -f docker-compose.simple.yml up -d

# Wait for services to be ready
echo ""
echo -e "${YELLOW}[2/5] Waiting for services to be healthy...${NC}"
echo "   This may take 2-3 minutes..."

MAX_WAIT=180
WAIT_INTERVAL=5
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
    BACKEND_HEALTH=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' multivendor_backend 2>/dev/null || echo "unknown")
    
    if [ "$BACKEND_HEALTH" = "healthy" ]; then
        echo -e "${GREEN}✓ Backend is healthy!${NC}"
        break
    fi
    
    if [ "$BACKEND_HEALTH" = "unhealthy" ]; then
        echo -e "${RED}✗ Backend is unhealthy!${NC}"
        echo "   Check logs: docker logs multivendor_backend"
        exit 1
    fi
    
    echo "   Waiting... ($ELAPSED/$MAX_WAIT seconds) - Status: $BACKEND_HEALTH"
    sleep $WAIT_INTERVAL
    ELAPSED=$((ELAPSED + WAIT_INTERVAL))
done

if [ "$BACKEND_HEALTH" != "healthy" ]; then
    echo -e "${RED}✗ Backend did not become healthy in time${NC}"
    echo "   Check logs: docker logs multivendor_backend"
    exit 1
fi

# Step 3: Run diagnostics
echo ""
echo -e "${YELLOW}[3/5] Running diagnostics...${NC}"
if [ -f "./diagnose-502.sh" ]; then
    ./diagnose-502.sh
else
    echo "   Diagnostic script not found, skipping..."
fi

# Step 4: Test API endpoint
echo ""
echo -e "${YELLOW}[4/5] Testing API endpoint through nginx...${NC}"
sleep 2

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/health/ 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "404" ]; then
    echo -e "${GREEN}✓ API endpoint is responding (HTTP $HTTP_CODE)${NC}"
    echo "   Note: 404 is OK if /health/ endpoint doesn't exist"
elif [ "$HTTP_CODE" = "502" ]; then
    echo -e "${RED}✗ 502 Bad Gateway - This is the problem!${NC}"
    echo ""
    echo -e "${YELLOW}Attempting to fix...${NC}"
    
    if [ -f "./fix-nginx-backend.sh" ]; then
        ./fix-nginx-backend.sh
        echo ""
        echo "Testing again..."
        sleep 2
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/health/ 2>/dev/null || echo "000")
        if [ "$HTTP_CODE" != "502" ]; then
            echo -e "${GREEN}✓ Fix successful! (HTTP $HTTP_CODE)${NC}"
        else
            echo -e "${RED}✗ Fix did not resolve the issue${NC}"
            echo "   Check: docker logs multivendor_nginx"
            echo "   Check: docker logs multivendor_backend"
        fi
    else
        echo "   Fix script not found"
    fi
else
    echo -e "${YELLOW}⚠ Unexpected status: HTTP $HTTP_CODE${NC}"
fi

# Step 5: Test direct backend connection
echo ""
echo -e "${YELLOW}[5/5] Testing direct backend connection...${NC}"
if curl -f -s -m 5 http://localhost:8000/health/ > /dev/null 2>&1 || \
   curl -f -s -m 5 http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is responding directly on port 8000${NC}"
else
    echo -e "${YELLOW}⚠ Backend port 8000 not exposed (this is OK if using nginx only)${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Services status:"
docker-compose -f docker-compose.simple.yml ps

echo ""
echo "Useful commands:"
echo "  - View backend logs: docker logs multivendor_backend"
echo "  - View nginx logs: docker logs multivendor_nginx"
echo "  - Test API: curl http://localhost/api/health/"
echo "  - Stop services: docker-compose -f docker-compose.simple.yml down"
echo ""
echo -e "${GREEN}Test completed!${NC}"


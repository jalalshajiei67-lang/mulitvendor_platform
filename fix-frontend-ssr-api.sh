#!/bin/bash

echo "🔧 Fixing Frontend SSR API Connection Issue"
echo "=============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "1️⃣ Testing API from frontend container..."
echo "----------------------------------------"
FRONTEND_CONTAINER=$(docker ps --filter "name=multivendor_frontend" --format "{{.Names}}")

if [ -z "$FRONTEND_CONTAINER" ]; then
    echo -e "${RED}❌ Frontend container not found!${NC}"
    exit 1
fi

echo "Testing https://api.indexo.ir/api/categories/ from frontend container..."
HTTP_CODE=$(docker exec $FRONTEND_CONTAINER curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://api.indexo.ir/api/categories/ 2>&1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Frontend container CAN reach api.indexo.ir (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}❌ Frontend container CANNOT reach api.indexo.ir (HTTP $HTTP_CODE)${NC}"
    echo ""
    echo "This is the problem! Frontend container can't reach the API during SSR."
    echo ""
    echo "Solution: Use internal Docker network hostname instead of external domain"
fi
echo ""

echo "2️⃣ Testing internal Docker network connection..."
echo "----------------------------------------"
echo "Testing http://multivendor_backend:8000/api/categories/ from frontend container..."
HTTP_CODE=$(docker exec $FRONTEND_CONTAINER curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://multivendor_backend:8000/api/categories/ 2>&1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Frontend container CAN reach backend via Docker network (HTTP $HTTP_CODE)${NC}"
    echo ""
    echo -e "${YELLOW}💡 SOLUTION: Use internal Docker hostname for SSR!${NC}"
    echo ""
    echo "The frontend should use 'http://multivendor_backend:8000/api' for server-side requests"
    echo "and 'https://api.indexo.ir/api' for client-side requests."
else
    echo -e "${RED}❌ Frontend container CANNOT reach backend via Docker network (HTTP $HTTP_CODE)${NC}"
fi
echo ""

echo "3️⃣ Checking current frontend environment..."
echo "----------------------------------------"
echo "NUXT_PUBLIC_API_BASE:"
docker exec $FRONTEND_CONTAINER env | grep NUXT_PUBLIC_API_BASE || echo "Not set"
echo ""

echo "4️⃣ Checking frontend logs for API errors..."
echo "----------------------------------------"
echo "Recent errors in frontend logs:"
docker logs $FRONTEND_CONTAINER --tail 30 | grep -i "error\|404\|fetch" | tail -5
echo ""

echo "=============================================="
echo "📝 RECOMMENDED FIX:"
echo "=============================================="
echo ""
echo "The issue is that during SSR (server-side rendering), the frontend container"
echo "tries to reach https://api.indexo.ir from inside Docker, which may fail due to:"
echo "1. Network routing issues"
echo "2. SSL certificate validation"
echo "3. DNS resolution inside container"
echo ""
echo "Solution: Configure Nuxt to use internal Docker hostname for SSR"
echo ""
echo "Update docker-compose.production.yml frontend service:"
echo ""
echo "  frontend:"
echo "    environment:"
echo "      - NUXT_PUBLIC_API_BASE=https://api.indexo.ir/api  # For client-side"
echo "      - NUXT_API_BASE=http://multivendor_backend:8000/api  # For SSR (no PUBLIC prefix)"
echo ""
echo "Then update Nuxt code to use NUXT_API_BASE for SSR and NUXT_PUBLIC_API_BASE for client."
echo ""
echo "OR simpler fix: Ensure frontend container can resolve api.indexo.ir"
echo "by adding to docker-compose:"
echo ""
echo "  frontend:"
echo "    extra_hosts:"
echo "      - 'api.indexo.ir:172.18.0.1'  # Traefik IP or host gateway"
echo ""


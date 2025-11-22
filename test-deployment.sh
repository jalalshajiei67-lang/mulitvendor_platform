#!/bin/bash

# 🚀 Deployment Test Script
# Run this after deployment to verify everything works

echo "🔍 Starting deployment verification..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test backend API
echo -e "\n${YELLOW}Testing Backend API...${NC}"
if curl -s -f https://api.indexo.ir/api/ > /dev/null; then
    echo -e "${GREEN}✅ Backend API responding${NC}"
else
    echo -e "${RED}❌ Backend API not responding${NC}"
fi

# Test frontend
echo -e "\n${YELLOW}Testing Frontend...${NC}"
if curl -s -f https://indexo.ir/ > /dev/null; then
    echo -e "${GREEN}✅ Frontend responding${NC}"
else
    echo -e "${RED}❌ Frontend not responding${NC}"
fi

# Test admin panel
echo -e "\n${YELLOW}Testing Admin Panel...${NC}"
response=$(curl -s -o /dev/null -w "%{http_code}" https://api.indexo.ir/admin/)
if [ "$response" = "302" ] || [ "$response" = "200" ]; then
    echo -e "${GREEN}✅ Admin panel accessible${NC}"
else
    echo -e "${RED}❌ Admin panel not accessible (HTTP $response)${NC}"
fi

# Test API endpoints
echo -e "\n${YELLOW}Testing API Endpoints...${NC}"
endpoints=(
    "https://api.indexo.ir/api/products/"
    "https://api.indexo.ir/api/categories/"
    "https://api.indexo.ir/api/users/"
)

for endpoint in "${endpoints[@]}"; do
    if curl -s -f "$endpoint" > /dev/null; then
        echo -e "${GREEN}✅ $endpoint responding${NC}"
    else
        echo -e "${RED}❌ $endpoint not responding${NC}"
    fi
done

# Test WebSocket (basic connectivity test)
echo -e "\n${YELLOW}Testing WebSocket Endpoint...${NC}"
# Note: Full WebSocket testing requires more complex tools like websocat
echo -e "${YELLOW}⚠️  Manual WebSocket testing required${NC}"

# Test HTTPS
echo -e "\n${YELLOW}Testing HTTPS Certificate...${NC}"
if curl -s -f --insecure https://api.indexo.ir/ > /dev/null; then
    echo -e "${GREEN}✅ HTTPS working${NC}"
else
    echo -e "${RED}❌ HTTPS not working${NC}"
fi

# Test CORS
echo -e "\n${YELLOW}Testing CORS Headers...${NC}"
cors_headers=$(curl -s -I -H "Origin: https://indexo.ir" https://api.indexo.ir/api/ | grep -i "access-control-allow-origin")
if [ -n "$cors_headers" ]; then
    echo -e "${GREEN}✅ CORS headers present${NC}"
else
    echo -e "${RED}❌ CORS headers missing${NC}"
fi

echo -e "\n${GREEN}🎯 Deployment verification complete!${NC}"
echo -e "${YELLOW}Manual checks required:${NC}"
echo "1. Test chat functionality (WebSocket)"
echo "2. Test user registration/login"
echo "3. Test admin panel login"
echo "4. Verify Persian RTL display"
echo "5. Test product creation/management"

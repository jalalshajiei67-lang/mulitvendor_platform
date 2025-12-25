#!/bin/bash
# Script to rebuild frontend on VPS with fixed Nuxt configuration
# This fixes the NS_ERROR_CORRUPTED_CONTENT issue

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VPS_HOST="root@46.249.101.84"
PROJECT_DIR="/root/multivendor_platform"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Rebuild Frontend on VPS${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Pull latest code
echo -e "${YELLOW}[1/5] Pulling latest code from Git...${NC}"
ssh $VPS_HOST "cd $PROJECT_DIR && git pull origin main" || {
    echo -e "${YELLOW}⚠ Git pull failed or no changes${NC}"
}

# Step 2: Verify nuxt.config.ts has the fixes
echo ""
echo -e "${YELLOW}[2/5] Verifying nuxt.config.ts changes...${NC}"
if ssh $VPS_HOST "cd $PROJECT_DIR && grep -q 'cssCodeSplit: true' multivendor_platform/front_end/nuxt/nuxt.config.ts && grep -q 'inlineStyles: false' multivendor_platform/front_end/nuxt/nuxt.config.ts"; then
    echo -e "${GREEN}✓ Configuration fixes are present${NC}"
else
    echo -e "${RED}✗ Configuration fixes not found!${NC}"
    echo "   Please ensure you've committed and pushed the nuxt.config.ts changes"
    echo "   Changes needed:"
    echo "   - cssCodeSplit: true"
    echo "   - inlineStyles: false"
    exit 1
fi

# Step 3: Rebuild frontend
echo ""
echo -e "${YELLOW}[3/5] Rebuilding frontend container (this may take 5-10 minutes)...${NC}"
echo "   This will build with --no-cache to ensure clean build"
ssh $VPS_HOST "cd $PROJECT_DIR && docker-compose -f docker-compose.production.yml build --no-cache frontend" || {
    echo -e "${RED}✗ Build failed!${NC}"
    echo "   Check the build logs above for errors"
    exit 1
}

# Step 4: Restart frontend
echo ""
echo -e "${YELLOW}[4/5] Restarting frontend container...${NC}"
ssh $VPS_HOST "cd $PROJECT_DIR && docker-compose -f docker-compose.production.yml up -d frontend"

# Step 5: Wait and verify
echo ""
echo -e "${YELLOW}[5/5] Waiting for frontend to be healthy...${NC}"
sleep 10

MAX_WAIT=120
WAIT_INTERVAL=5
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
    HEALTH=$(ssh $VPS_HOST "docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' multivendor_frontend 2>/dev/null || echo 'unknown'")
    
    if [ "$HEALTH" = "healthy" ]; then
        echo -e "${GREEN}✓ Frontend is healthy!${NC}"
        break
    fi
    
    echo "   Waiting... ($ELAPSED/$MAX_WAIT seconds) - Status: $HEALTH"
    sleep $WAIT_INTERVAL
    ELAPSED=$((ELAPSED + WAIT_INTERVAL))
done

# Verify assets are generated
echo ""
echo -e "${YELLOW}Verifying assets are generated...${NC}"
CSS_COUNT=$(ssh $VPS_HOST "docker exec multivendor_frontend find /app/.output/public/_nuxt -name '*.css' 2>/dev/null | wc -l")
JS_COUNT=$(ssh $VPS_HOST "docker exec multivendor_frontend find /app/.output/public/_nuxt -name '*.js' 2>/dev/null | wc -l")

if [ "$CSS_COUNT" -gt 0 ] && [ "$JS_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ Assets generated: $CSS_COUNT CSS files, $JS_COUNT JS files${NC}"
else
    echo -e "${YELLOW}⚠ Assets not found yet (may need more time)${NC}"
    echo "   CSS files: $CSS_COUNT"
    echo "   JS files: $JS_COUNT"
fi

# Test endpoint
echo ""
echo -e "${YELLOW}Testing frontend endpoint...${NC}"
HTTP_CODE=$(ssh $VPS_HOST "curl -s -o /dev/null -w '%{http_code}' https://indexo.ir/")
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Frontend is responding (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${YELLOW}⚠ Frontend returned HTTP $HTTP_CODE${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Rebuild Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Test in browser: https://indexo.ir"
echo "  2. Check browser console for any remaining errors"
echo "  3. Verify assets load: Check Network tab for _nuxt/ files"
echo ""
echo "If assets still don't load, check:"
echo "  - docker logs multivendor_frontend --tail 50"
echo "  - Verify assets exist: docker exec multivendor_frontend ls -la /app/.output/public/_nuxt/"


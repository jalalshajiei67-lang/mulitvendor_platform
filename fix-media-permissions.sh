#!/bin/bash

# Fix Media Directory Permissions
# Run on VPS to fix permission issues with media uploads

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Fix Media Directory Permissions              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Check if backend container is running
if ! docker ps --filter "name=multivendor_backend" --format "{{.Names}}" | grep -q multivendor_backend; then
    echo -e "${RED}✗ Backend container is not running!${NC}"
    exit 1
fi

echo -e "${YELLOW}[1/4] Checking current media directory permissions...${NC}"
docker exec multivendor_backend ls -la /app/media/ 2>/dev/null || {
    echo -e "${YELLOW}  Media directory doesn't exist, creating it...${NC}"
    docker exec multivendor_backend mkdir -p /app/media
}

echo ""
echo -e "${YELLOW}[2/4] Creating required media subdirectories...${NC}"
docker exec multivendor_backend mkdir -p /app/media/product_images
docker exec multivendor_backend mkdir -p /app/media/category_images
docker exec multivendor_backend mkdir -p /app/media/subcategory_images
docker exec multivendor_backend mkdir -p /app/media/department_images
docker exec multivendor_backend mkdir -p /app/media/blog_images
docker exec multivendor_backend mkdir -p /app/media/user_images

echo ""
echo -e "${YELLOW}[3/4] Fixing permissions...${NC}"
# Set permissions to 755 for directories and allow write access
docker exec multivendor_backend chmod -R 755 /app/media
docker exec multivendor_backend chown -R appuser:appuser /app/media 2>/dev/null || {
    # If appuser doesn't exist, try with the user that runs the process
    echo -e "${YELLOW}  appuser not found, checking current user...${NC}"
    CURRENT_USER=$(docker exec multivendor_backend whoami)
    echo -e "${YELLOW}  Current user: ${CURRENT_USER}${NC}"
    docker exec multivendor_backend chown -R ${CURRENT_USER}:${CURRENT_USER} /app/media 2>/dev/null || {
        echo -e "${YELLOW}  Using root to set permissions...${NC}"
        docker exec -u root multivendor_backend chown -R 1000:1000 /app/media 2>/dev/null || true
    }
}

echo ""
echo -e "${YELLOW}[4/4] Verifying permissions...${NC}"
docker exec multivendor_backend ls -la /app/media/ | head -10

echo ""
echo -e "${GREEN}✓ Permissions fixed!${NC}"
echo ""
echo -e "${YELLOW}Testing write access...${NC}"
if docker exec multivendor_backend touch /app/media/test_write.txt 2>/dev/null; then
    docker exec multivendor_backend rm /app/media/test_write.txt
    echo -e "${GREEN}✓ Write access confirmed!${NC}"
else
    echo -e "${RED}✗ Write access still denied. Trying alternative fix...${NC}"
    echo ""
    echo -e "${YELLOW}Attempting to fix with root user...${NC}"
    docker exec -u root multivendor_backend chmod -R 777 /app/media
    docker exec -u root multivendor_backend chown -R 1000:1000 /app/media
    
    if docker exec multivendor_backend touch /app/media/test_write2.txt 2>/dev/null; then
        docker exec multivendor_backend rm /app/media/test_write2.txt
        echo -e "${GREEN}✓ Write access now working!${NC}"
    else
        echo -e "${RED}✗ Still having issues. Check volume mount configuration.${NC}"
    fi
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Fix Complete                                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Try uploading an image in Django admin again"
echo -e "  2. If it still fails, check docker-compose volume configuration"
echo -e "  3. Restart backend: docker compose restart backend"



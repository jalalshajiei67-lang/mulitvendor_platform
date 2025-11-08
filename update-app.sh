#!/bin/bash

# Application Update Script
# Run on VPS to update the application with new code

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Application Update Script          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}Step 1: Creating database backup...${NC}"
./backup-database.sh

echo ""
echo -e "${YELLOW}Step 2: Pulling latest code...${NC}"
echo -e "${YELLOW}(Make sure you've uploaded new files to /tmp/deploy.tar.gz)${NC}"

if [ -f "/tmp/deploy.tar.gz" ]; then
    echo -e "${GREEN}✓ New deployment package found${NC}"
    
    echo ""
    echo -e "${YELLOW}Step 3: Extracting new files...${NC}"
    tar -xzf /tmp/deploy.tar.gz
    rm /tmp/deploy.tar.gz
    
    echo -e "${GREEN}✓ Files updated${NC}"
else
    echo -e "${RED}No deployment package found at /tmp/deploy.tar.gz${NC}"
    echo -e "${YELLOW}Please upload new files first using deploy.sh from local machine${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 4: Rebuilding containers...${NC}"
docker-compose down
docker-compose up -d --build

echo ""
echo -e "${YELLOW}Step 5: Running migrations...${NC}"
sleep 10  # Wait for containers to start
docker-compose exec -T backend python manage.py migrate --noinput

echo ""
echo -e "${YELLOW}Step 6: Collecting static files...${NC}"
docker-compose exec -T backend python manage.py collectstatic --noinput

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Update Complete! 🎉                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Container Status:${NC}"
docker-compose ps




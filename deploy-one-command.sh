#!/bin/bash
# One-command deployment script - does everything!

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VPS_IP="158.255.74.123"
VPS_USER="root"
VPS_PASS="e<c6w:1EDupHjf4*"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   One-Command Deployment Script       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.production .env
    echo -e "${GREEN}✓ .env created${NC}"
else
    echo -e "${GREEN}✓ .env exists${NC}"
fi

# Step 2: Deploy
echo -e "\n${YELLOW}Deploying to VPS...${NC}"
./deploy.sh

# Step 3: Setup on VPS
echo -e "\n${YELLOW}Setting up on VPS...${NC}"
echo -e "${BLUE}You'll be prompted for the SSH password: e<c6w:1EDupHjf4*${NC}"
echo ""

ssh ${VPS_USER}@${VPS_IP} "cd /opt/multivendor_platform && ./server-deploy.sh"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║      Deployment Complete! 🎉           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Your application is running at:${NC}"
echo "  Frontend: http://${VPS_IP}"
echo "  Admin:    http://${VPS_IP}/admin"
echo "  API:      http://${VPS_IP}/api"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Create superuser:"
echo "     ssh ${VPS_USER}@${VPS_IP}"
echo "     cd /opt/multivendor_platform"
echo "     docker-compose exec backend python manage.py createsuperuser"
echo ""
echo "  2. Access your application:"
echo "     http://${VPS_IP}"
echo ""
echo -e "${GREEN}Done!${NC}"




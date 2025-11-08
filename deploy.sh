#!/bin/bash

# Deployment Script for Multivendor Platform
# This script deploys the application to the VPS server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Multivendor Platform Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"

# Configuration
VPS_IP="158.255.74.123"
VPS_USER="root"
PROJECT_NAME="multivendor_platform"
REMOTE_DIR="/opt/${PROJECT_NAME}"

echo -e "\n${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please create .env file from env.template:${NC}"
    echo "  cp env.template .env"
    echo "  # Then edit .env with your configuration"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites checked${NC}"

echo -e "\n${YELLOW}Step 2: Creating deployment package...${NC}"

# Create a tar archive excluding unnecessary files
tar -czf deploy.tar.gz \
    --exclude='node_modules' \
    --exclude='venv' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.sqlite3' \
    --exclude='.env' \
    --exclude='multivendor_platform/multivendor_platform/media/*' \
    --exclude='multivendor_platform/front_end/dist' \
    docker-compose.yml \
    nginx/ \
    Dockerfile \
    requirements.txt \
    multivendor_platform/

echo -e "${GREEN}✓ Deployment package created${NC}"

echo -e "\n${YELLOW}Step 3: Uploading to VPS...${NC}"

# Upload files to VPS
scp deploy.tar.gz ${VPS_USER}@${VPS_IP}:/tmp/
scp .env ${VPS_USER}@${VPS_IP}:/tmp/deploy.env

echo -e "${GREEN}✓ Files uploaded${NC}"

echo -e "\n${YELLOW}Step 4: Setting up on VPS...${NC}"

# Execute commands on VPS
ssh ${VPS_USER}@${VPS_IP} bash -c "'
set -e

echo \"Creating project directory...\"
mkdir -p ${REMOTE_DIR}

echo \"Extracting files...\"
cd ${REMOTE_DIR}
tar -xzf /tmp/deploy.tar.gz

echo \"Setting up environment...\"
mv /tmp/deploy.env ${REMOTE_DIR}/.env

echo \"Cleaning up temporary files...\"
rm /tmp/deploy.tar.gz

echo \"Setting permissions...\"
chmod +x ${REMOTE_DIR}/*.sh 2>/dev/null || true

echo \"VPS setup complete!\"
'"

echo -e "${GREEN}✓ VPS setup complete${NC}"

# Clean up local deployment package
rm deploy.tar.gz

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment package uploaded successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. SSH into your VPS:"
echo "   ssh ${VPS_USER}@${VPS_IP}"
echo ""
echo "2. Navigate to project directory:"
echo "   cd ${REMOTE_DIR}"
echo ""
echo "3. Start the application:"
echo "   docker-compose up -d --build"
echo ""
echo "4. Check logs:"
echo "   docker-compose logs -f"
echo ""
echo "5. Create Django superuser:"
echo "   docker-compose exec backend python manage.py createsuperuser"
echo ""
echo -e "${YELLOW}Or use the server-deploy.sh script on the VPS for automated deployment.${NC}"




#!/bin/bash

# Test VPS Connection Script

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

VPS_IP="158.255.74.123"
VPS_USER="root"

echo -e "${YELLOW}Testing connection to VPS...${NC}"
echo ""

# Test SSH connection
echo -e "${YELLOW}1. Testing SSH connection...${NC}"
if ssh -o ConnectTimeout=5 -o BatchMode=yes ${VPS_USER}@${VPS_IP} exit 2>/dev/null; then
    echo -e "${GREEN}✓ SSH connection successful${NC}"
else
    echo -e "${YELLOW}⚠ SSH connection test (this is normal if password auth is required)${NC}"
    echo -e "${YELLOW}  Attempting to connect...${NC}"
    ssh ${VPS_USER}@${VPS_IP} "echo 'SSH connection successful!'"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ SSH connection works${NC}"
    else
        echo -e "${RED}✗ SSH connection failed${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${YELLOW}2. Getting server information...${NC}"
ssh ${VPS_USER}@${VPS_IP} "
echo -e '${YELLOW}OS:${NC}' \$(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2)
echo -e '${YELLOW}Kernel:${NC}' \$(uname -r)
echo -e '${YELLOW}CPU:${NC}' \$(nproc) cores
echo -e '${YELLOW}Memory:${NC}' \$(free -h | grep Mem | awk '{print \$2}')
echo -e '${YELLOW}Disk:${NC}' \$(df -h / | tail -1 | awk '{print \$2}')
echo -e '${YELLOW}Docker:${NC}' \$(docker --version 2>/dev/null || echo 'Not installed')
echo -e '${YELLOW}Docker Compose:${NC}' \$(docker-compose --version 2>/dev/null || echo 'Not installed')
"

echo ""
echo -e "${GREEN}Connection test complete!${NC}"
echo ""
echo -e "${YELLOW}You can proceed with deployment.${NC}"




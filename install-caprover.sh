#!/bin/bash

# CapRover Fresh Installation Script
# This script installs a fresh instance of CapRover

# Don't exit on error - we want to handle errors gracefully
set +e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   CapRover Fresh Installation          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Checking if ports are available...${NC}"
# Check if ports are in use
if command -v netstat &> /dev/null; then
    PORTS_IN_USE=$(netstat -tuln | grep -E ':(80|443|3000)' || true)
elif command -v ss &> /dev/null; then
    PORTS_IN_USE=$(ss -tuln | grep -E ':(80|443|3000)' || true)
fi

if [ ! -z "$PORTS_IN_USE" ]; then
    echo -e "${RED}Warning: Ports 80, 443, or 3000 are in use:${NC}"
    echo "$PORTS_IN_USE"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${YELLOW}Step 2: Installing CapRover...${NC}"
# Stop any existing CapRover container
docker stop captain-captain 2>/dev/null || true
docker rm captain-captain 2>/dev/null || true

# Pull latest CapRover image
docker pull caprover/caprover

# Run CapRover
docker run -d \
    -p 80:80 \
    -p 443:443 \
    -p 3000:3000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /captain:/captain \
    --name captain-captain \
    --restart=always \
    caprover/caprover

echo -e "${GREEN}✓ CapRover container started${NC}"

echo -e "${YELLOW}Step 3: Waiting for CapRover to initialize...${NC}"
sleep 5

# Wait for CapRover to be ready
echo -e "${YELLOW}Checking CapRover status...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1 || curl -s http://127.0.0.1:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ CapRover dashboard is accessible${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${YELLOW}CapRover is starting... Please wait a few minutes and check http://158.255.74.123:3000${NC}"
    else
        echo -n "."
        sleep 2
    fi
done

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   CapRover Installation Complete!     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Access CapRover dashboard:"
echo "   - Direct IP: http://158.255.74.123:3000"
echo "   - Domain: http://captain.indexo.ir (if DNS configured)"
echo ""
echo "2. Complete initial setup:"
echo "   - Set root domain: indexo.ir"
echo "   - Set CapRover password"
echo "   - Save configuration"
echo ""
echo "3. Login via CLI:"
echo "   caprover login"
echo "   Enter: https://captain.indexo.ir"
echo ""
echo "4. Verify installation:"
echo "   caprover apps:list"
echo ""
echo -e "${GREEN}CapRover is now running!${NC}"


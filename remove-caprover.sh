#!/bin/bash

# CapRover Removal Script
# This script removes CapRover and all associated containers, volumes, and data

# Don't exit on error - we want to continue even if some removals fail
set +e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     CapRover Removal Script            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Stopping all Docker containers...${NC}"
# Stop all running containers (safely)
RUNNING_CONTAINERS=$(docker ps -q)
if [ ! -z "$RUNNING_CONTAINERS" ]; then
    docker stop $RUNNING_CONTAINERS 2>/dev/null || echo "Some containers may already be stopped"
else
    echo "No containers to stop"
fi

echo -e "${YELLOW}Step 2: Removing CapRover containers...${NC}"
# Remove CapRover containers
docker rm -f $(docker ps -aq --filter "name=captain") 2>/dev/null || echo "No CapRover containers found"

echo -e "${YELLOW}Step 3: Removing CapRover volumes...${NC}"
# Remove CapRover volumes
VOLUMES=$(docker volume ls 2>/dev/null | grep captain | awk '{print $2}' || true)
if [ ! -z "$VOLUMES" ]; then
    echo "$VOLUMES" | while read vol; do
        docker volume rm "$vol" 2>/dev/null || echo "Volume $vol may be in use"
    done
else
    echo "No CapRover volumes found"
fi

echo -e "${YELLOW}Step 4: Removing CapRover images...${NC}"
# Remove CapRover images
IMAGES=$(docker images --format "{{.Repository}}:{{.ID}}" | grep captain || true)
if [ ! -z "$IMAGES" ]; then
    echo "$IMAGES" | while IFS=':' read repo id; do
        docker rmi -f "$id" 2>/dev/null || echo "Image $repo may be in use"
    done
else
    echo "No CapRover images found"
fi

echo -e "${YELLOW}Step 5: Removing CapRover data directories...${NC}"
# Remove CapRover data directories
rm -rf /var/lib/docker/volumes/captain-data 2>/dev/null || echo "Directory not found"
rm -rf /captain 2>/dev/null || echo "Directory not found"

echo -e "${YELLOW}Step 6: Removing CapRover scripts...${NC}"
# Remove CapRover scripts
rm -rf /usr/local/bin/captain 2>/dev/null || echo "Script not found"

echo -e "${YELLOW}Step 7: Cleaning up Docker...${NC}"
# Clean up Docker
docker container prune -f
docker volume prune -f
docker network prune -f

echo ""
echo -e "${GREEN}Step 8: Verifying removal...${NC}"
# Verify removal
if docker ps | grep -q captain; then
    echo -e "${RED}Warning: CapRover containers still running${NC}"
else
    echo -e "${GREEN}✓ No CapRover containers running${NC}"
fi

if docker volume ls | grep -q captain; then
    echo -e "${YELLOW}Warning: Some CapRover volumes may still exist${NC}"
else
    echo -e "${GREEN}✓ No CapRover volumes found${NC}"
fi

# Check ports
echo ""
echo -e "${YELLOW}Checking ports 80, 443, 3000...${NC}"
if command -v netstat &> /dev/null; then
    netstat -tulpn | grep -E ':(80|443|3000)' || echo -e "${GREEN}✓ Ports 80, 443, 3000 are free${NC}"
elif command -v ss &> /dev/null; then
    ss -tulpn | grep -E ':(80|443|3000)' || echo -e "${GREEN}✓ Ports 80, 443, 3000 are free${NC}"
else
    echo "Cannot check ports (netstat/ss not available)"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     CapRover Removal Complete!        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Run install-caprover.sh to install fresh CapRover"
echo "2. Or manually install using: docker run -p 80:80 -p 443:443 -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock -v /captain:/captain caprover/caprover"


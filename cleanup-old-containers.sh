#!/bin/bash

# Cleanup Old Containers, Images, and Volumes
# Helps identify and remove unused Docker resources from previous deployments

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Docker Cleanup Tool                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Show all containers (running and stopped)
echo -e "${YELLOW}[1/6] All containers (running and stopped):${NC}"
docker ps -a

echo ""
echo -e "${YELLOW}[2/6] Stopped containers:${NC}"
STOPPED=$(docker ps -a --filter "status=exited" --format "{{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Image}}")
if [ -z "$STOPPED" ]; then
    echo -e "${GREEN}  No stopped containers found${NC}"
else
    echo "$STOPPED" | column -t
fi

echo ""
echo -e "${YELLOW}[3/6] Unused images (dangling):${NC}"
DANGLING_IMAGES=$(docker images -f "dangling=true" -q)
if [ -z "$DANGLING_IMAGES" ]; then
    echo -e "${GREEN}  No dangling images found${NC}"
else
    docker images -f "dangling=true"
fi

echo ""
echo -e "${YELLOW}[4/6] All images (sorted by creation date):${NC}"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}\t{{.Size}}" | head -20

echo ""
echo -e "${YELLOW}[5/6] Unused volumes:${NC}"
UNUSED_VOLUMES=$(docker volume ls -f "dangling=true" -q)
if [ -z "$UNUSED_VOLUMES" ]; then
    echo -e "${GREEN}  No unused volumes found${NC}"
else
    docker volume ls -f "dangling=true"
fi

echo ""
echo -e "${YELLOW}[6/6] All volumes:${NC}"
docker volume ls

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Cleanup Options                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Choose what to clean:${NC}"
echo "  1) Remove stopped containers"
echo "  2) Remove dangling images"
echo "  3) Remove unused volumes"
echo "  4) Remove all unused resources (containers, images, volumes, networks)"
echo "  5) Show disk usage"
echo "  6) Exit"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}Removing stopped containers...${NC}"
        docker container prune -f
        echo -e "${GREEN}✓ Stopped containers removed${NC}"
        ;;
    2)
        echo ""
        echo -e "${YELLOW}Removing dangling images...${NC}"
        docker image prune -f
        echo -e "${GREEN}✓ Dangling images removed${NC}"
        ;;
    3)
        echo ""
        echo -e "${YELLOW}Removing unused volumes...${NC}"
        echo -e "${RED}⚠ WARNING: This will remove volumes not used by any container!${NC}"
        read -p "Are you sure? (type 'yes' to confirm): " confirm
        if [ "$confirm" = "yes" ]; then
            docker volume prune -f
            echo -e "${GREEN}✓ Unused volumes removed${NC}"
        else
            echo -e "${YELLOW}Cancelled${NC}"
        fi
        ;;
    4)
        echo ""
        echo -e "${RED}⚠ WARNING: This will remove ALL unused resources!${NC}"
        echo -e "${YELLOW}This includes:${NC}"
        echo "  - Stopped containers"
        echo "  - Dangling images"
        echo "  - Unused volumes"
        echo "  - Unused networks"
        read -p "Are you sure? (type 'yes' to confirm): " confirm
        if [ "$confirm" = "yes" ]; then
            docker system prune -a --volumes -f
            echo -e "${GREEN}✓ All unused resources removed${NC}"
        else
            echo -e "${YELLOW}Cancelled${NC}"
        fi
        ;;
    5)
        echo ""
        echo -e "${YELLOW}Disk usage:${NC}"
        docker system df
        ;;
    6)
        echo -e "${YELLOW}Exiting...${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Cleanup Complete                             ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"



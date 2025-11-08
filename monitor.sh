#!/bin/bash

# Monitoring script for deployed application
# Run on VPS to monitor application health

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Multivendor Platform Monitor        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if docker-compose is running
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose not found!${NC}"
    exit 1
fi

echo -e "${YELLOW}=== Container Status ===${NC}"
docker-compose ps
echo ""

echo -e "${YELLOW}=== Health Checks ===${NC}"

# Check database
if docker-compose exec -T db pg_isready -U postgres &> /dev/null; then
    echo -e "${GREEN}✓ Database: Healthy${NC}"
else
    echo -e "${RED}✗ Database: Unhealthy${NC}"
fi

# Check backend
if docker-compose exec -T backend python -c "import django; print('OK')" &> /dev/null; then
    echo -e "${GREEN}✓ Backend: Healthy${NC}"
else
    echo -e "${RED}✗ Backend: Unhealthy${NC}"
fi

# Check frontend
if curl -s -o /dev/null -w "%{http_code}" http://localhost:80 | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✓ Frontend: Accessible${NC}"
else
    echo -e "${RED}✗ Frontend: Not accessible${NC}"
fi

# Check API
if curl -s -o /dev/null -w "%{http_code}" http://localhost:80/api/ | grep -q "200\|301\|302\|403"; then
    echo -e "${GREEN}✓ API: Accessible${NC}"
else
    echo -e "${RED}✗ API: Not accessible${NC}"
fi

echo ""
echo -e "${YELLOW}=== Resource Usage ===${NC}"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo ""
echo -e "${YELLOW}=== Disk Usage ===${NC}"
df -h | grep -E '^Filesystem|/$|/var/lib/docker'

echo ""
echo -e "${YELLOW}=== Recent Errors (last 50 lines) ===${NC}"
docker-compose logs --tail=50 2>&1 | grep -i error || echo "No errors found"

echo ""
echo -e "${YELLOW}=== Last 10 Log Entries ===${NC}"
docker-compose logs --tail=10

echo ""
echo -e "${GREEN}Monitor complete!${NC}"




#!/bin/bash

# Health Check Script
# Quick health check for all services

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_service() {
    local service=$1
    local check_cmd=$2
    
    if eval $check_cmd &>/dev/null; then
        echo -e "${GREEN}✓${NC} $service"
        return 0
    else
        echo -e "${RED}✗${NC} $service"
        return 1
    fi
}

echo -e "${YELLOW}Running health checks...${NC}\n"

# Check Docker
check_service "Docker daemon" "docker ps"

# Check containers
check_service "PostgreSQL container" "docker-compose ps db | grep -q Up"
check_service "Backend container" "docker-compose ps backend | grep -q Up"
check_service "Frontend container" "docker-compose ps frontend | grep -q Up"
check_service "Nginx container" "docker-compose ps nginx | grep -q Up"

# Check database connection
check_service "Database connection" "docker-compose exec -T db pg_isready -U postgres"

# Check HTTP endpoints
check_service "Nginx (HTTP)" "curl -s -o /dev/null -w '%{http_code}' http://localhost:80 | grep -q '200\|301\|302'"
check_service "API endpoint" "curl -s -o /dev/null -w '%{http_code}' http://localhost:80/api/ | grep -q '200\|403'"
check_service "Admin endpoint" "curl -s -o /dev/null -w '%{http_code}' http://localhost:80/admin/ | grep -q '200\|302'"

echo ""
echo -e "${YELLOW}Resource Usage:${NC}"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -5

echo ""
ERRORS=$(docker-compose logs --tail=100 2>&1 | grep -i error | wc -l)
if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}⚠ Found $ERRORS error(s) in logs${NC}"
    echo -e "${YELLOW}Run 'docker-compose logs' to view details${NC}"
else
    echo -e "${GREEN}✓ No errors in recent logs${NC}"
fi




#!/bin/bash
# Diagnostic script for 502 Bad Gateway errors
# This script helps identify why nginx can't connect to backend

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}502 Bad Gateway Diagnostic Tool${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if containers are running
echo -e "${YELLOW}[1/8] Checking container status...${NC}"
BACKEND_STATUS=$(docker ps --filter "name=multivendor_backend" --format "{{.Status}}" 2>/dev/null || echo "NOT_FOUND")
NGINX_STATUS=$(docker ps --filter "name=multivendor_nginx" --format "{{.Status}}" 2>/dev/null || echo "NOT_FOUND")

if [ "$BACKEND_STATUS" = "NOT_FOUND" ]; then
    echo -e "${RED}✗ Backend container not found${NC}"
    echo "   Run: docker-compose up -d backend"
    exit 1
else
    echo -e "${GREEN}✓ Backend container: $BACKEND_STATUS${NC}"
fi

if [ "$NGINX_STATUS" = "NOT_FOUND" ]; then
    echo -e "${RED}✗ Nginx container not found${NC}"
    echo "   Run: docker-compose up -d nginx"
    exit 1
else
    echo -e "${GREEN}✓ Nginx container: $NGINX_STATUS${NC}"
fi

# Check backend health
echo ""
echo -e "${YELLOW}[2/8] Checking backend health status...${NC}"
BACKEND_HEALTH=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' multivendor_backend 2>/dev/null || echo "unknown")
echo "   Backend health: $BACKEND_HEALTH"

if [ "$BACKEND_HEALTH" = "healthy" ] || [ "$BACKEND_HEALTH" = "running" ]; then
    echo -e "${GREEN}✓ Backend appears healthy${NC}"
else
    echo -e "${RED}✗ Backend is not healthy!${NC}"
    echo "   Check logs: docker logs multivendor_backend"
fi

# Check if backend is listening on port 8000
echo ""
echo -e "${YELLOW}[3/8] Testing backend port 8000 from host...${NC}"
if curl -f -s -m 5 http://localhost:8000/health/ > /dev/null 2>&1 || curl -f -s -m 5 http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is responding on localhost:8000${NC}"
else
    echo -e "${RED}✗ Backend is NOT responding on localhost:8000${NC}"
    echo "   This might be normal if backend port is not exposed"
fi

# Check Docker network connectivity
echo ""
echo -e "${YELLOW}[4/8] Checking Docker network connectivity...${NC}"
BACKEND_IP=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' multivendor_backend 2>/dev/null || echo "NOT_FOUND")
NGINX_IP=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' multivendor_nginx 2>/dev/null || echo "NOT_FOUND")

if [ "$BACKEND_IP" != "NOT_FOUND" ] && [ "$NGINX_IP" != "NOT_FOUND" ]; then
    echo "   Backend IP: $BACKEND_IP"
    echo "   Nginx IP: $NGINX_IP"
    
    # Test if nginx can reach backend by IP
    if docker exec multivendor_nginx wget -q -O- --timeout=5 http://$BACKEND_IP:8000/health/ > /dev/null 2>&1 || \
       docker exec multivendor_nginx wget -q -O- --timeout=5 http://$BACKEND_IP:8000/ > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Nginx can reach backend by IP ($BACKEND_IP:8000)${NC}"
    else
        echo -e "${RED}✗ Nginx CANNOT reach backend by IP${NC}"
    fi
else
    echo -e "${RED}✗ Could not determine container IPs${NC}"
fi

# Test DNS resolution from nginx
echo ""
echo -e "${YELLOW}[5/8] Testing DNS resolution from nginx container...${NC}"
if docker exec multivendor_nginx nslookup backend > /dev/null 2>&1 || \
   docker exec multivendor_nginx getent hosts backend > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Nginx can resolve 'backend' hostname${NC}"
    BACKEND_RESOLVED=$(docker exec multivendor_nginx getent hosts backend | awk '{print $1}' 2>/dev/null || echo "NOT_FOUND")
    echo "   'backend' resolves to: $BACKEND_RESOLVED"
else
    echo -e "${RED}✗ Nginx CANNOT resolve 'backend' hostname${NC}"
    echo "   This is likely the root cause!"
fi

# Test direct connection from nginx to backend
echo ""
echo -e "${YELLOW}[6/8] Testing direct connection from nginx to backend:8000...${NC}"
if docker exec multivendor_nginx wget -q -O- --timeout=5 http://backend:8000/health/ > /dev/null 2>&1 || \
   docker exec multivendor_nginx wget -q -O- --timeout=5 http://backend:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Nginx can connect to backend:8000${NC}"
else
    echo -e "${RED}✗ Nginx CANNOT connect to backend:8000${NC}"
    echo "   This is the root cause of 502 errors!"
fi

# Check nginx configuration
echo ""
echo -e "${YELLOW}[7/8] Checking nginx configuration...${NC}"
if docker exec multivendor_nginx nginx -t > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Nginx configuration is valid${NC}"
else
    echo -e "${RED}✗ Nginx configuration has errors${NC}"
    docker exec multivendor_nginx nginx -t
fi

# Check nginx error logs
echo ""
echo -e "${YELLOW}[8/8] Checking nginx error logs for recent errors...${NC}"
ERROR_COUNT=$(docker logs multivendor_backend 2>&1 | grep -i "error\|exception\|traceback" | tail -5 | wc -l)
if [ "$ERROR_COUNT" -gt 0 ]; then
    echo -e "${RED}✗ Found $ERROR_COUNT recent errors in backend logs${NC}"
    echo "   Recent errors:"
    docker logs multivendor_backend 2>&1 | grep -i "error\|exception\|traceback" | tail -3
else
    echo -e "${GREEN}✓ No recent errors in backend logs${NC}"
fi

NGINX_ERRORS=$(docker logs multivendor_nginx 2>&1 | grep -i "upstream\|502\|bad gateway" | tail -5 | wc -l)
if [ "$NGINX_ERRORS" -gt 0 ]; then
    echo -e "${YELLOW}⚠ Found $NGINX_ERRORS upstream/502 errors in nginx logs${NC}"
    echo "   Recent nginx errors:"
    docker logs multivendor_nginx 2>&1 | grep -i "upstream\|502\|bad gateway" | tail -3
fi

# Summary and recommendations
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Summary & Recommendations${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if they're on the same network
BACKEND_NETWORK=$(docker inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' multivendor_backend 2>/dev/null)
NGINX_NETWORK=$(docker inspect --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' multivendor_nginx 2>/dev/null)

if [ "$BACKEND_NETWORK" = "$NGINX_NETWORK" ] && [ "$BACKEND_NETWORK" != "" ]; then
    echo -e "${GREEN}✓ Both containers are on the same network: $BACKEND_NETWORK${NC}"
else
    echo -e "${RED}✗ Containers are on different networks!${NC}"
    echo "   Backend: $BACKEND_NETWORK"
    echo "   Nginx: $NGINX_NETWORK"
    echo ""
    echo "   Fix: Ensure both services use the same network in docker-compose.yml"
fi

echo ""
echo "Next steps:"
echo "1. If DNS resolution fails, check docker-compose.yml network configuration"
echo "2. If connection fails, check backend logs: docker logs multivendor_backend"
echo "3. Test backend directly: docker exec multivendor_nginx wget -O- http://backend:8000/health/"
echo "4. Check nginx config: docker exec multivendor_nginx cat /etc/nginx/conf.d/default.conf"


#!/bin/bash
# Script to diagnose Traefik routing issues
# Usage: ./diagnose-traefik-routing.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Traefik Routing Diagnostics${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⚠ Running without root privileges. Some checks may fail.${NC}"
    echo ""
fi

# 1. Check Traefik container status
echo -e "${CYAN}[1/10] Checking Traefik container status...${NC}"
if docker ps --format '{{.Names}}' | grep -q "^traefik$"; then
    echo -e "${GREEN}✓ Traefik container is running${NC}"
    TRAEFIK_CONTAINER="traefik"
elif docker ps --format '{{.Names}}' | grep -q "traefik"; then
    TRAEFIK_CONTAINER=$(docker ps --format '{{.Names}}' | grep traefik | head -1)
    echo -e "${GREEN}✓ Traefik container found: $TRAEFIK_CONTAINER${NC}"
else
    echo -e "${RED}✗ Traefik container not found${NC}"
    exit 1
fi
echo ""

# 2. Check backend container status
echo -e "${CYAN}[2/10] Checking backend container status...${NC}"
if docker ps --format '{{.Names}}' | grep -q "backend"; then
    BACKEND_CONTAINER=$(docker ps --format '{{.Names}}' | grep backend | head -1)
    echo -e "${GREEN}✓ Backend container found: $BACKEND_CONTAINER${NC}"
    
    # Check if backend is healthy
    BACKEND_HEALTH=$(docker inspect --format='{{.State.Health.Status}}' $BACKEND_CONTAINER 2>/dev/null || echo "no-healthcheck")
    if [ "$BACKEND_HEALTH" = "healthy" ]; then
        echo -e "${GREEN}  → Backend health: healthy${NC}"
    elif [ "$BACKEND_HEALTH" = "no-healthcheck" ]; then
        echo -e "${YELLOW}  → Backend health: no healthcheck configured${NC}"
    else
        echo -e "${RED}  → Backend health: $BACKEND_HEALTH${NC}"
    fi
else
    echo -e "${RED}✗ Backend container not found${NC}"
    BACKEND_CONTAINER=""
fi
echo ""

# 3. Check network connectivity
echo -e "${CYAN}[3/10] Checking network connectivity...${NC}"
NETWORK_NAME="multivendor_network"
if docker network ls | grep -q "$NETWORK_NAME"; then
    echo -e "${GREEN}✓ Network '$NETWORK_NAME' exists${NC}"
    
    # Check if Traefik is on the network
    if docker network inspect $NETWORK_NAME --format '{{range .Containers}}{{.Name}} {{end}}' | grep -q "$TRAEFIK_CONTAINER"; then
        echo -e "${GREEN}  → Traefik is connected to network${NC}"
    else
        echo -e "${RED}  → Traefik is NOT connected to network${NC}"
    fi
    
    # Check if backend is on the network
    if [ -n "$BACKEND_CONTAINER" ]; then
        if docker network inspect $NETWORK_NAME --format '{{range .Containers}}{{.Name}} {{end}}' | grep -q "$BACKEND_CONTAINER"; then
            echo -e "${GREEN}  → Backend is connected to network${NC}"
        else
            echo -e "${RED}  → Backend is NOT connected to network${NC}"
        fi
    fi
else
    echo -e "${RED}✗ Network '$NETWORK_NAME' not found${NC}"
fi
echo ""

# 4. Check Traefik can discover backend
echo -e "${CYAN}[4/10] Checking Traefik service discovery...${NC}"
if docker exec $TRAEFIK_CONTAINER wget -qO- http://localhost:8080/api/http/services 2>/dev/null | grep -q "backend"; then
    echo -e "${GREEN}✓ Traefik discovered backend service${NC}"
else
    echo -e "${RED}✗ Traefik did NOT discover backend service${NC}"
    echo -e "${YELLOW}  → Checking Traefik API...${NC}"
    docker exec $TRAEFIK_CONTAINER wget -qO- http://localhost:8080/api/http/services 2>/dev/null | head -20 || echo "  → Traefik API not accessible"
fi
echo ""

# 5. Check Traefik routers
echo -e "${CYAN}[5/10] Checking Traefik routers...${NC}"
ROUTERS=$(docker exec $TRAEFIK_CONTAINER wget -qO- http://localhost:8080/api/http/routers 2>/dev/null || echo "")
if echo "$ROUTERS" | grep -q "backend"; then
    echo -e "${GREEN}✓ Backend router found in Traefik${NC}"
    echo -e "${CYAN}  Backend router details:${NC}"
    echo "$ROUTERS" | grep -A 10 "backend" | head -15 || true
else
    echo -e "${RED}✗ Backend router NOT found in Traefik${NC}"
fi
echo ""

# 6. Check backend container labels
echo -e "${CYAN}[6/10] Checking backend container labels...${NC}"
if [ -n "$BACKEND_CONTAINER" ]; then
    BACKEND_LABELS=$(docker inspect --format='{{range $k, $v := .Config.Labels}}{{$k}}={{$v}}{{"\n"}}{{end}}' $BACKEND_CONTAINER)
    
    if echo "$BACKEND_LABELS" | grep -q "traefik.enable=true"; then
        echo -e "${GREEN}✓ traefik.enable=true found${NC}"
    else
        echo -e "${RED}✗ traefik.enable=true NOT found${NC}"
    fi
    
    if echo "$BACKEND_LABELS" | grep -q "traefik.http.routers.backend"; then
        echo -e "${GREEN}✓ Backend router labels found:${NC}"
        echo "$BACKEND_LABELS" | grep "traefik" | sed 's/^/  → /'
    else
        echo -e "${RED}✗ Backend router labels NOT found${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Backend container not found, skipping label check${NC}"
fi
echo ""

# 7. Test backend connectivity from Traefik
echo -e "${CYAN}[7/10] Testing backend connectivity from Traefik...${NC}"
if [ -n "$BACKEND_CONTAINER" ]; then
    BACKEND_IP=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $BACKEND_CONTAINER 2>/dev/null || echo "")
    if [ -n "$BACKEND_IP" ]; then
        echo -e "${CYAN}  Backend IP: $BACKEND_IP${NC}"
        
        # Try to curl backend from Traefik container
        if docker exec $TRAEFIK_CONTAINER wget -qO- --timeout=5 "http://$BACKEND_IP:8000/api/" 2>/dev/null | grep -q ""; then
            echo -e "${GREEN}  → Traefik can reach backend directly${NC}"
        else
            echo -e "${YELLOW}  → Traefik cannot reach backend directly (may be normal if using service name)${NC}"
        fi
        
        # Try using service name
        if docker exec $TRAEFIK_CONTAINER wget -qO- --timeout=5 "http://backend:8000/api/" 2>/dev/null | grep -q ""; then
            echo -e "${GREEN}  → Traefik can reach backend via service name${NC}"
        else
            echo -e "${RED}  → Traefik cannot reach backend via service name${NC}"
        fi
    else
        echo -e "${RED}  → Could not determine backend IP${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Backend container not found, skipping connectivity test${NC}"
fi
echo ""

# 8. Check for router conflicts
echo -e "${CYAN}[8/10] Checking for router conflicts...${NC}"
if echo "$ROUTERS" | grep -q "nginx"; then
    echo -e "${YELLOW}⚠ Both backend and nginx routers exist${NC}"
    echo -e "${CYAN}  Checking router rules:${NC}"
    
    BACKEND_RULE=$(echo "$ROUTERS" | grep -A 5 "backend" | grep "Rule" | head -1 || echo "")
    NGINX_RULE=$(echo "$ROUTERS" | grep -A 5 "nginx" | grep "Rule" | head -1 || echo "")
    
    if [ -n "$BACKEND_RULE" ]; then
        echo -e "  Backend: $BACKEND_RULE"
    fi
    if [ -n "$NGINX_RULE" ]; then
        echo -e "  Nginx: $NGINX_RULE"
    fi
    
    # Check if both match same domain
    if echo "$BACKEND_RULE" | grep -q "Host" && echo "$NGINX_RULE" | grep -q "Host"; then
        BACKEND_HOST=$(echo "$BACKEND_RULE" | grep -oP "Host\([^)]+\)" | head -1 || echo "")
        NGINX_HOST=$(echo "$NGINX_RULE" | grep -oP "Host\([^)]+\)" | head -1 || echo "")
        
        if [ "$BACKEND_HOST" = "$NGINX_HOST" ]; then
            echo -e "${RED}  → CONFLICT: Both routers match same host!${NC}"
            echo -e "${YELLOW}  → Backend should have PathPrefix('/api') to avoid conflicts${NC}"
        else
            echo -e "${GREEN}  → No host conflict (different hosts)${NC}"
        fi
    fi
else
    echo -e "${GREEN}✓ No nginx router found (no conflict)${NC}"
fi
echo ""

# 9. Check Traefik logs for errors
echo -e "${CYAN}[9/10] Checking recent Traefik logs for errors...${NC}"
TRAEFIK_ERRORS=$(docker logs --tail 50 $TRAEFIK_CONTAINER 2>&1 | grep -i "error\|warn\|404" | tail -10 || echo "")
if [ -n "$TRAEFIK_ERRORS" ]; then
    echo -e "${YELLOW}Recent Traefik errors/warnings:${NC}"
    echo "$TRAEFIK_ERRORS" | sed 's/^/  → /'
else
    echo -e "${GREEN}✓ No recent errors in Traefik logs${NC}"
fi
echo ""

# 10. Test actual routing
echo -e "${CYAN}[10/10] Testing actual routing...${NC}"
echo -e "${YELLOW}  Note: This requires API_DOMAIN to be set${NC}"

# Try to get API_DOMAIN from backend container
if [ -n "$BACKEND_CONTAINER" ]; then
    API_DOMAIN=$(docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' $BACKEND_CONTAINER 2>/dev/null | grep "API_DOMAIN" | cut -d'=' -f2 || echo "")
    
    if [ -n "$API_DOMAIN" ]; then
        echo -e "${CYAN}  Testing: https://$API_DOMAIN/api/${NC}"
        
        # Test from host
        if curl -k -s -o /dev/null -w "%{http_code}" "https://$API_DOMAIN/api/" | grep -q "200\|404"; then
            HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" "https://$API_DOMAIN/api/")
            if [ "$HTTP_CODE" = "200" ]; then
                echo -e "${GREEN}  → Routing works! Got 200 response${NC}"
            else
                echo -e "${RED}  → Routing issue! Got $HTTP_CODE response${NC}"
            fi
        else
            echo -e "${YELLOW}  → Could not test routing (network issue or domain not accessible)${NC}"
        fi
    else
        echo -e "${YELLOW}  → API_DOMAIN not found in backend container${NC}"
    fi
else
    echo -e "${YELLOW}  → Backend container not found, skipping routing test${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Diagnostics Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${CYAN}Common Issues Found:${NC}"
echo "  1. Backend router missing PathPrefix('/api') rule"
echo "  2. Router priority conflicts between backend and nginx"
echo "  3. Backend service not explicitly defined in labels"
echo "  4. Network connectivity issues"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo "  1. Review the issues above"
echo "  2. Run fix-traefik-backend.sh to apply fixes"
echo "  3. Restart backend container: docker restart $BACKEND_CONTAINER"
echo "  4. Check Traefik dashboard or logs for updates"
echo ""


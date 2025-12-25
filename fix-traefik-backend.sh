#!/bin/bash
# Script to fix Traefik backend routing configuration
# Usage: ./fix-traefik-backend.sh [production|staging]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

ENVIRONMENT="${1:-production}"

if [ "$ENVIRONMENT" != "production" ] && [ "$ENVIRONMENT" != "staging" ]; then
    echo -e "${RED}Error: Environment must be 'production' or 'staging'${NC}"
    echo "Usage: $0 [production|staging]"
    exit 1
fi

COMPOSE_FILE="docker-compose.production.yml"
BACKEND_CONTAINER="multivendor_backend"
if [ "$ENVIRONMENT" = "staging" ]; then
    COMPOSE_FILE="docker-compose.staging.yml"
    BACKEND_CONTAINER="multivendor_backend_staging"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Fix Traefik Backend Routing${NC}"
echo -e "${BLUE}Environment: $ENVIRONMENT${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if docker-compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    echo -e "${RED}✗ $COMPOSE_FILE not found${NC}"
    exit 1
fi

# Check if backend container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${BACKEND_CONTAINER}$"; then
    echo -e "${RED}✗ Backend container '$BACKEND_CONTAINER' not found${NC}"
    exit 1
fi

echo -e "${CYAN}[1/6] Checking current backend labels...${NC}"
CURRENT_LABELS=$(docker inspect --format='{{range $k, $v := .Config.Labels}}{{$k}}={{$v}}{{"\n"}}{{end}}' $BACKEND_CONTAINER)
CURRENT_RULE=$(echo "$CURRENT_LABELS" | grep "traefik.http.routers.backend.rule" || echo "")

if [ -n "$CURRENT_RULE" ]; then
    echo -e "${CYAN}  Current rule: $CURRENT_RULE${NC}"
    
    if echo "$CURRENT_RULE" | grep -q "PathPrefix"; then
        echo -e "${GREEN}  → PathPrefix already configured${NC}"
        echo -e "${YELLOW}  → Skipping fix (already correct)${NC}"
        exit 0
    else
        echo -e "${YELLOW}  → PathPrefix missing, will fix...${NC}"
    fi
else
    echo -e "${RED}  → No router rule found${NC}"
fi
echo ""

# Backup docker-compose file
echo -e "${CYAN}[2/6] Backing up $COMPOSE_FILE...${NC}"
BACKUP_FILE="${COMPOSE_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$COMPOSE_FILE" "$BACKUP_FILE"
echo -e "${GREEN}✓ Backup created: $BACKUP_FILE${NC}"
echo ""

# Update docker-compose file
echo -e "${CYAN}[3/6] Updating $COMPOSE_FILE...${NC}"

# Check if the fix is already applied
if grep -q 'traefik.http.routers.backend.rule=Host.*PathPrefix.*\/api' "$COMPOSE_FILE"; then
    echo -e "${GREEN}✓ Fix already applied in $COMPOSE_FILE${NC}"
else
    # Apply the fix using sed
    sed -i 's|traefik.http.routers.backend.rule=Host(`\${API_DOMAIN}`)|traefik.http.routers.backend.rule=Host(`\${API_DOMAIN}`) \&\& PathPrefix(`/api`)|g' "$COMPOSE_FILE"
    
    # Add priority if not present
    if ! grep -q 'traefik.http.routers.backend.priority' "$COMPOSE_FILE"; then
        # Insert priority after tls.certresolver line
        sed -i '/traefik.http.routers.backend.tls.certresolver/a\      - "traefik.http.routers.backend.priority=10"' "$COMPOSE_FILE"
    fi
    
    echo -e "${GREEN}✓ Updated $COMPOSE_FILE${NC}"
fi
echo ""

# Recreate backend container with new labels
echo -e "${CYAN}[4/6] Recreating backend container with new labels...${NC}"
echo -e "${YELLOW}  This will restart the backend service${NC}"

# Stop backend
docker stop $BACKEND_CONTAINER 2>/dev/null || true
echo -e "${GREEN}  → Backend stopped${NC}"

# Remove backend container
docker rm $BACKEND_CONTAINER 2>/dev/null || true
echo -e "${GREEN}  → Backend container removed${NC}"

# Recreate using docker-compose
if docker-compose -f "$COMPOSE_FILE" up -d --no-deps backend; then
    echo -e "${GREEN}✓ Backend container recreated${NC}"
else
    echo -e "${RED}✗ Failed to recreate backend container${NC}"
    echo -e "${YELLOW}  Restoring backup...${NC}"
    cp "$BACKUP_FILE" "$COMPOSE_FILE"
    exit 1
fi
echo ""

# Wait for backend to be healthy
echo -e "${CYAN}[5/6] Waiting for backend to be healthy...${NC}"
MAX_WAIT=60
WAIT_TIME=0
while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if docker ps --format '{{.Names}}' | grep -q "^${BACKEND_CONTAINER}$"; then
        HEALTH=$(docker inspect --format='{{.State.Health.Status}}' $BACKEND_CONTAINER 2>/dev/null || echo "starting")
        
        if [ "$HEALTH" = "healthy" ]; then
            echo -e "${GREEN}✓ Backend is healthy${NC}"
            break
        elif [ "$HEALTH" = "unhealthy" ]; then
            echo -e "${RED}✗ Backend is unhealthy${NC}"
            break
        else
            echo -e "${YELLOW}  → Waiting... ($WAIT_TIME/$MAX_WAIT seconds)${NC}"
            sleep 5
            WAIT_TIME=$((WAIT_TIME + 5))
        fi
    else
        echo -e "${RED}✗ Backend container not running${NC}"
        break
    fi
done
echo ""

# Verify new labels
echo -e "${CYAN}[6/6] Verifying new configuration...${NC}"
NEW_LABELS=$(docker inspect --format='{{range $k, $v := .Config.Labels}}{{$k}}={{$v}}{{"\n"}}{{end}}' $BACKEND_CONTAINER)
NEW_RULE=$(echo "$NEW_LABELS" | grep "traefik.http.routers.backend.rule" || echo "")

if [ -n "$NEW_RULE" ]; then
    echo -e "${CYAN}  New rule: $NEW_RULE${NC}"
    
    if echo "$NEW_RULE" | grep -q "PathPrefix.*\/api"; then
        echo -e "${GREEN}✓ PathPrefix('/api') configured correctly${NC}"
    else
        echo -e "${RED}✗ PathPrefix('/api') not found in new rule${NC}"
    fi
    
    if echo "$NEW_LABELS" | grep -q "traefik.http.routers.backend.priority=10"; then
        echo -e "${GREEN}✓ Priority configured correctly${NC}"
    else
        echo -e "${YELLOW}⚠ Priority not found (may be optional)${NC}"
    fi
else
    echo -e "${RED}✗ Router rule not found${NC}"
fi
echo ""

# Check Traefik discovery
echo -e "${CYAN}Checking Traefik service discovery...${NC}"
TRAEFIK_CONTAINER="traefik"
if [ "$ENVIRONMENT" = "staging" ]; then
    TRAEFIK_CONTAINER="traefik_staging"
fi

if docker ps --format '{{.Names}}' | grep -q "^${TRAEFIK_CONTAINER}$"; then
    sleep 3  # Give Traefik time to discover
    
    if docker exec $TRAEFIK_CONTAINER wget -qO- http://localhost:8080/api/http/services 2>/dev/null | grep -q "backend"; then
        echo -e "${GREEN}✓ Traefik discovered backend service${NC}"
    else
        echo -e "${YELLOW}⚠ Traefik may not have discovered backend yet (wait a few seconds)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Traefik container not found, skipping discovery check${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Fix Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${CYAN}Changes Applied:${NC}"
echo "  1. Added PathPrefix('/api') to backend router rule"
echo "  2. Added priority=10 to backend router"
echo "  3. Recreated backend container with new labels"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo "  1. Wait 10-30 seconds for Traefik to update routing"
echo "  2. Test the API: curl -k https://\${API_DOMAIN}/api/"
echo "  3. Check Traefik logs: docker logs $TRAEFIK_CONTAINER"
echo "  4. If issues persist, run: ./diagnose-traefik-routing.sh"
echo ""
echo -e "${YELLOW}Backup saved: $BACKUP_FILE${NC}"
echo ""


#!/bin/bash
# Fix Django ALLOWED_HOSTS to include Docker network IPs

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Fix Django ALLOWED_HOSTS${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get backend IP
BACKEND_IP=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' multivendor_backend 2>/dev/null)

if [ -z "$BACKEND_IP" ]; then
    echo -e "${RED}✗ Could not determine backend IP${NC}"
    exit 1
fi

echo "Backend IP: $BACKEND_IP"

# Get current ALLOWED_HOSTS
CURRENT_HOSTS=$(docker exec multivendor_backend env | grep "^ALLOWED_HOSTS=" | cut -d'=' -f2-)

echo "Current ALLOWED_HOSTS: $CURRENT_HOSTS"

# Extract IP network (first 3 octets)
IP_NETWORK=$(echo $BACKEND_IP | cut -d'.' -f1-3)

# Add Docker network IPs if not present
if echo "$CURRENT_HOSTS" | grep -q "$BACKEND_IP"; then
    echo -e "${GREEN}✓ Backend IP already in ALLOWED_HOSTS${NC}"
else
    echo -e "${YELLOW}⚠ Adding Docker network IPs to ALLOWED_HOSTS...${NC}"
    
    # Update environment variable in docker-compose or container
    # For now, we'll update the .env file if it exists
    ENV_FILE="/root/multivendor_platform/.env"
    
    if [ -f "$ENV_FILE" ]; then
        # Backup
        cp "$ENV_FILE" "${ENV_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        
        # Update ALLOWED_HOSTS
        if grep -q "^ALLOWED_HOSTS=" "$ENV_FILE"; then
            # Append Docker IPs
            sed -i "s|^ALLOWED_HOSTS=\(.*\)|ALLOWED_HOSTS=\1,$BACKEND_IP,$IP_NETWORK.0/16|" "$ENV_FILE"
        else
            echo "ALLOWED_HOSTS=$CURRENT_HOSTS,$BACKEND_IP,$IP_NETWORK.0/16" >> "$ENV_FILE"
        fi
        
        echo -e "${GREEN}✓ Updated .env file${NC}"
        echo "   You need to restart the backend container for changes to take effect"
        echo "   Run: docker-compose restart backend"
    else
        echo -e "${YELLOW}⚠ .env file not found at $ENV_FILE${NC}"
        echo "   You can manually add to ALLOWED_HOSTS:"
        echo "   $BACKEND_IP,$IP_NETWORK.0/16"
    fi
fi

# Better solution: Update settings.py to auto-add Docker network IPs
echo ""
echo -e "${YELLOW}Alternative: Update settings.py to auto-detect Docker network IPs${NC}"
echo "   This would automatically add Docker network IPs to ALLOWED_HOSTS"

echo ""
echo -e "${GREEN}Fix completed!${NC}"
echo ""
echo "To apply changes, restart the backend:"
echo "  docker-compose restart backend"
echo "  # or"
echo "  docker restart multivendor_backend"


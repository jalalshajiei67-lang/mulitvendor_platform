#!/bin/bash
# Script to run diagnostics remotely on VPS
# Usage: ./run-diagnostics-remote.sh [diagnose|fix|both]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VPS_HOST="root@46.249.101.84"
VPS_PATH="/root"
ACTION="${1:-both}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Run Diagnostics on VPS${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if scripts exist on VPS
echo -e "${YELLOW}[1/3] Checking scripts on VPS...${NC}"
if ssh $VPS_HOST "test -f $VPS_PATH/diagnose-502.sh && test -x $VPS_PATH/diagnose-502.sh"; then
    echo -e "${GREEN}✓ diagnose-502.sh found and executable${NC}"
else
    echo -e "${RED}✗ diagnose-502.sh not found or not executable${NC}"
    echo "   Run ./deploy-diagnostics.sh first"
    exit 1
fi

if ssh $VPS_HOST "test -f $VPS_PATH/fix-nginx-backend.sh && test -x $VPS_PATH/fix-nginx-backend.sh"; then
    echo -e "${GREEN}✓ fix-nginx-backend.sh found and executable${NC}"
else
    echo -e "${RED}✗ fix-nginx-backend.sh not found or not executable${NC}"
    echo "   Run ./deploy-diagnostics.sh first"
    exit 1
fi

# Run diagnostics
if [ "$ACTION" = "diagnose" ] || [ "$ACTION" = "both" ]; then
    echo ""
    echo -e "${YELLOW}[2/3] Running diagnostics...${NC}"
    echo ""
    ssh -t $VPS_HOST "$VPS_PATH/diagnose-502.sh"
    DIAGNOSTIC_EXIT=$?
    
    if [ $DIAGNOSTIC_EXIT -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Diagnostics completed${NC}"
    else
        echo ""
        echo -e "${YELLOW}⚠ Diagnostics completed with warnings${NC}"
    fi
fi

# Run fix if requested
if [ "$ACTION" = "fix" ] || [ "$ACTION" = "both" ]; then
    echo ""
    echo -e "${YELLOW}[3/3] Applying fixes...${NC}"
    echo ""
    
    # Ask for confirmation if running fix
    if [ "$ACTION" = "both" ]; then
        echo -e "${YELLOW}Do you want to apply fixes? (y/n)${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            echo "Skipping fix. Run with 'fix' argument to apply fixes directly."
            exit 0
        fi
    fi
    
    ssh -t $VPS_HOST "$VPS_PATH/fix-nginx-backend.sh"
    FIX_EXIT=$?
    
    if [ $FIX_EXIT -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Fixes applied successfully${NC}"
    else
        echo ""
        echo -e "${RED}✗ Fix failed${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Remote Execution Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Check nginx logs: ssh $VPS_HOST 'docker logs multivendor_nginx --tail 50'"
echo "  2. Check backend logs: ssh $VPS_HOST 'docker logs multivendor_backend --tail 50'"
echo "  3. Test API: ssh $VPS_HOST 'curl -I http://localhost/api/health/'"
echo ""


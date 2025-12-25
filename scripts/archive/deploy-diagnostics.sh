#!/bin/bash
# Script to copy diagnostic and fix scripts to VPS
# Usage: ./deploy-diagnostics.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VPS_HOST="root@46.249.101.84"
VPS_PATH="/root"
SCRIPT_DIR="."

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Deploy Diagnostics Scripts to VPS${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if scripts exist locally
echo -e "${YELLOW}[1/5] Checking local scripts...${NC}"

if [ ! -f "$SCRIPT_DIR/diagnose-502.sh" ]; then
    echo -e "${RED}✗ diagnose-502.sh not found in current directory${NC}"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/fix-nginx-backend.sh" ]; then
    echo -e "${RED}✗ fix-nginx-backend.sh not found in current directory${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All scripts found${NC}"

# Test SSH connection
echo ""
echo -e "${YELLOW}[2/5] Testing SSH connection...${NC}"
if ssh -o ConnectTimeout=5 -o BatchMode=yes $VPS_HOST "echo 'Connection successful'" 2>/dev/null; then
    echo -e "${GREEN}✓ SSH connection successful${NC}"
else
    echo -e "${YELLOW}⚠ SSH connection test failed (may require password)${NC}"
    echo "   You'll be prompted for password during copy"
fi

# Copy scripts to VPS
echo ""
echo -e "${YELLOW}[3/5] Copying scripts to VPS...${NC}"
echo "   Destination: $VPS_HOST:$VPS_PATH/"

scp "$SCRIPT_DIR/diagnose-502.sh" "$VPS_HOST:$VPS_PATH/" && \
    echo -e "${GREEN}✓ Copied diagnose-502.sh${NC}" || \
    { echo -e "${RED}✗ Failed to copy diagnose-502.sh${NC}"; exit 1; }

scp "$SCRIPT_DIR/fix-nginx-backend.sh" "$VPS_HOST:$VPS_PATH/" && \
    echo -e "${GREEN}✓ Copied fix-nginx-backend.sh${NC}" || \
    { echo -e "${RED}✗ Failed to copy fix-nginx-backend.sh${NC}"; exit 1; }

# Make scripts executable on VPS
echo ""
echo -e "${YELLOW}[4/5] Making scripts executable on VPS...${NC}"
ssh $VPS_HOST "chmod +x $VPS_PATH/diagnose-502.sh $VPS_PATH/fix-nginx-backend.sh" && \
    echo -e "${GREEN}✓ Scripts are now executable${NC}" || \
    { echo -e "${RED}✗ Failed to make scripts executable${NC}"; exit 1; }

# Verify scripts on VPS
echo ""
echo -e "${YELLOW}[5/5] Verifying scripts on VPS...${NC}"
if ssh $VPS_HOST "test -f $VPS_PATH/diagnose-502.sh && test -f $VPS_PATH/fix-nginx-backend.sh && test -x $VPS_PATH/diagnose-502.sh && test -x $VPS_PATH/fix-nginx-backend.sh"; then
    echo -e "${GREEN}✓ All scripts verified and executable${NC}"
else
    echo -e "${RED}✗ Verification failed${NC}"
    exit 1
fi

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Deployment Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Scripts are now available on your VPS:"
echo "  - $VPS_PATH/diagnose-502.sh"
echo "  - $VPS_PATH/fix-nginx-backend.sh"
echo ""
echo "To use them, SSH to your VPS and run:"
echo ""
echo -e "${YELLOW}  ssh $VPS_HOST${NC}"
echo -e "${YELLOW}  cd $VPS_PATH${NC}"
echo -e "${YELLOW}  ./diagnose-502.sh${NC}"
echo -e "${YELLOW}  ./fix-nginx-backend.sh${NC}"
echo ""
echo "Or run remotely:"
echo -e "${YELLOW}  ssh $VPS_HOST '$VPS_PATH/diagnose-502.sh'${NC}"
echo -e "${YELLOW}  ssh $VPS_HOST '$VPS_PATH/fix-nginx-backend.sh'${NC}"
echo ""



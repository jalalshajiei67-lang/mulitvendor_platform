#!/bin/bash

# Setup Automated Auction Deposit Forfeiture Check using Cron
# Run on VPS to configure automatic checking of expired auction deposits

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detect project directory
if [ -d "/opt/multivendor_platform" ]; then
    SCRIPT_DIR="/opt/multivendor_platform"
elif [ -d "/media/jalal/New Volume/project/mulitvendor_platform" ]; then
    SCRIPT_DIR="/media/jalal/New Volume/project/mulitvendor_platform"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

DJANGO_DIR="${SCRIPT_DIR}/multivendor_platform/multivendor_platform"
MANAGE_PY="${DJANGO_DIR}/manage.py"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Setup Auction Deposit Cron Job       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if manage.py exists
if [ ! -f "$MANAGE_PY" ]; then
    echo -e "${RED}manage.py not found at $MANAGE_PY${NC}"
    echo -e "${YELLOW}Please update SCRIPT_DIR in this script${NC}"
    exit 1
fi

echo -e "${YELLOW}Setting up hourly auction deposit check...${NC}"

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Python not found. Please install Python 3.${NC}"
    exit 1
fi

# Create cron job - runs every hour
# Format: minute hour day month weekday command
CRON_JOB="0 * * * * cd ${DJANGO_DIR} && ${PYTHON_CMD} manage.py check_auction_deposits >> /var/log/auction-deposits.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "check_auction_deposits"; then
    echo -e "${YELLOW}Cron job already exists. Updating...${NC}"
    (crontab -l 2>/dev/null | grep -v "check_auction_deposits"; echo "$CRON_JOB") | crontab -
else
    echo -e "${YELLOW}Adding new cron job...${NC}"
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi

echo -e "${GREEN}✓ Automated auction deposit check configured${NC}"
echo ""
echo -e "${YELLOW}Schedule:${NC}"
echo "  Frequency: Every hour (at :00 minutes)"
echo "  Command: check_auction_deposits"
echo "  Log: /var/log/auction-deposits.log"
echo ""
echo -e "${YELLOW}What it does:${NC}"
echo "  - Checks for auctions closed > 72 hours ago"
echo "  - Finds auctions where buyer hasn't selected a winner"
echo "  - Forfeits deposit and distributes to platform and bidders"
echo ""
echo -e "${YELLOW}Current cron jobs:${NC}"
crontab -l 2>/dev/null | grep -v "^#" | grep -E "(check_auction|auction)" || echo "  (none found)"
echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo -e "${YELLOW}To test manually (dry run):${NC}"
echo "  cd ${DJANGO_DIR}"
echo "  ${PYTHON_CMD} manage.py check_auction_deposits --dry-run"
echo ""
echo -e "${YELLOW}To test manually (actual run):${NC}"
echo "  cd ${DJANGO_DIR}"
echo "  ${PYTHON_CMD} manage.py check_auction_deposits"
echo ""
echo -e "${YELLOW}To view logs:${NC}"
echo "  tail -f /var/log/auction-deposits.log"
echo ""
echo -e "${YELLOW}To remove this cron job:${NC}"
echo "  crontab -e"
echo "  (then delete the line with check_auction_deposits)"


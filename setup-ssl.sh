#!/bin/bash

# SSL Setup Script using Let's Encrypt
# Usage: ./setup-ssl.sh yourdomain.com

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if domain is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Domain name required${NC}"
    echo "Usage: ./setup-ssl.sh yourdomain.com"
    exit 1
fi

DOMAIN=$1
EMAIL=${2:-"admin@${DOMAIN}"}

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setting up SSL for ${DOMAIN}${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}Step 1: Obtaining SSL certificate...${NC}"

# Create certbot directories
mkdir -p certbot/conf certbot/www

# Get SSL certificate
docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email ${EMAIL} \
    --agree-tos \
    --no-eff-email \
    -d ${DOMAIN} \
    -d www.${DOMAIN}

echo -e "${GREEN}✓ SSL certificate obtained${NC}"

echo -e "\n${YELLOW}Step 2: Updating nginx configuration...${NC}"

# Update SSL configuration
cp nginx/conf.d/ssl.conf.example nginx/conf.d/ssl.conf
sed -i "s/DOMAIN_NAME/${DOMAIN}/g" nginx/conf.d/ssl.conf

# Remove default HTTP-only config
mv nginx/conf.d/default.conf nginx/conf.d/default.conf.backup

echo -e "${GREEN}✓ Nginx configuration updated${NC}"

echo -e "\n${YELLOW}Step 3: Restarting nginx...${NC}"

docker-compose restart nginx

echo -e "${GREEN}✓ Nginx restarted${NC}"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}SSL Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\nYour site should now be accessible via HTTPS:"
echo "https://${DOMAIN}"
echo "https://www.${DOMAIN}"
echo ""
echo -e "${YELLOW}Certificate will auto-renew via the certbot container${NC}"




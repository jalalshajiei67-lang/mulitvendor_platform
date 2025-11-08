#!/bin/bash

# Server-side deployment script
# Run this script on the VPS after uploading files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Starting Server Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Step 1: Installing Docker and Docker Compose...${NC}"

# Update system packages
apt-get update

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io
    systemctl start docker
    systemctl enable docker
    echo -e "${GREEN}✓ Docker installed${NC}"
else
    echo -e "${GREEN}✓ Docker already installed${NC}"
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose installed${NC}"
else
    echo -e "${GREEN}✓ Docker Compose already installed${NC}"
fi

echo -e "\n${YELLOW}Step 2: Setting up firewall...${NC}"

# Install and configure UFW
if ! command -v ufw &> /dev/null; then
    apt-get install -y ufw
fi

ufw --force enable
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw status

echo -e "${GREEN}✓ Firewall configured${NC}"

echo -e "\n${YELLOW}Step 3: Building and starting containers...${NC}"

# Stop existing containers if any
docker-compose down 2>/dev/null || true

# Build and start containers
docker-compose up -d --build

echo -e "${GREEN}✓ Containers started${NC}"

echo -e "\n${YELLOW}Step 4: Waiting for services to be ready...${NC}"
sleep 10

echo -e "\n${YELLOW}Step 5: Running Django migrations...${NC}"

# Run Django migrations
docker-compose exec -T backend python manage.py migrate --noinput

echo -e "${GREEN}✓ Migrations completed${NC}"

echo -e "\n${YELLOW}Step 6: Collecting static files...${NC}"

# Collect static files
docker-compose exec -T backend python manage.py collectstatic --noinput

echo -e "${GREEN}✓ Static files collected${NC}"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}Container Status:${NC}"
docker-compose ps

echo -e "\n${YELLOW}Useful Commands:${NC}"
echo "View logs:                docker-compose logs -f"
echo "View specific service:    docker-compose logs -f backend"
echo "Restart services:         docker-compose restart"
echo "Stop services:            docker-compose down"
echo "Rebuild services:         docker-compose up -d --build"
echo ""
echo "Create superuser:         docker-compose exec backend python manage.py createsuperuser"
echo "Access Django shell:      docker-compose exec backend python manage.py shell"
echo "Access database:          docker-compose exec db psql -U postgres -d multivendor_db"
echo ""
echo -e "${YELLOW}Your application should now be accessible at:${NC}"
echo "http://$(curl -s ifconfig.me)"
echo ""
echo -e "${YELLOW}To enable HTTPS:${NC}"
echo "1. Ensure your domain DNS is pointing to this server"
echo "2. Run: ./setup-ssl.sh yourdomain.com"




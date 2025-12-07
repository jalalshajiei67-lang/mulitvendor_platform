#!/bin/bash

# Script to configure Docker registry mirror
# This helps bypass Docker Hub restrictions

echo "========================================"
echo "   Docker Registry Mirror Setup"
echo "========================================"
echo ""

# Check if Docker is installed via snap (common on Ubuntu)
if command -v snap &> /dev/null && snap list docker &> /dev/null; then
    echo "Detected Docker installed via snap"
    echo ""
    echo "Configuring registry mirror for snap Docker..."
    echo ""
    echo "Available mirror options:"
    echo "  1. Docker Mirror (Iran) - https://docker.arvancloud.ir"
    echo "  2. Docker Mirror (China) - https://docker.mirrors.ustc.edu.cn"
    echo "  3. Docker Mirror (China) - https://hub-mirror.c.163.com"
    echo ""
    read -p "Enter mirror URL (or press Enter for default: https://docker.arvancloud.ir): " MIRROR_URL
    MIRROR_URL=${MIRROR_URL:-https://docker.arvancloud.ir}
    
    echo ""
    echo "Setting Docker daemon configuration..."
    sudo snap set docker daemon-config='{"registry-mirrors": ["'$MIRROR_URL'"]}'
    
    echo "Restarting Docker..."
    sudo snap restart docker
    
    echo ""
    echo "✅ Docker registry mirror configured!"
    echo "   Mirror URL: $MIRROR_URL"
    echo ""
    echo "Waiting 5 seconds for Docker to restart..."
    sleep 5
    
elif [ -f /etc/docker/daemon.json ]; then
    echo "Found /etc/docker/daemon.json"
    echo "Backing up existing configuration..."
    sudo cp /etc/docker/daemon.json /etc/docker/daemon.json.bak
    
    echo "Adding registry mirror..."
    # This is a simplified version - might need manual editing
    echo "Please manually edit /etc/docker/daemon.json and add:"
    echo '  "registry-mirrors": ["https://docker.arvancloud.ir"]'
    echo ""
    echo "Then restart Docker: sudo systemctl restart docker"
    
else
    echo "Creating Docker daemon configuration..."
    echo ""
    echo "Available mirror options:"
    echo "  1. Docker Mirror (Iran) - https://docker.arvancloud.ir"
    echo "  2. Docker Mirror (China) - https://docker.mirrors.ustc.edu.cn"
    echo "  3. Docker Mirror (China) - https://hub-mirror.c.163.com"
    echo ""
    read -p "Enter mirror URL (or press Enter for default: https://docker.arvancloud.ir): " MIRROR_URL
    MIRROR_URL=${MIRROR_URL:-https://docker.arvancloud.ir}
    
    sudo mkdir -p /etc/docker
    echo "{\"registry-mirrors\": [\"$MIRROR_URL\"]}" | sudo tee /etc/docker/daemon.json
    
    echo "Restarting Docker..."
    sudo systemctl restart docker
    
    echo ""
    echo "✅ Docker registry mirror configured!"
    echo "   Mirror URL: $MIRROR_URL"
fi

echo ""
echo "Testing Docker..."
docker info | grep -i mirror || echo "Mirror configuration might need verification"

echo ""
echo "========================================"
echo "Next step: Run ./run-local-nohub.sh again"
echo "========================================"


























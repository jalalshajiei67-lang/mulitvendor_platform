#!/bin/bash

# Helper script to set up Docker permissions and start Docker service

echo "========================================"
echo "   Docker Setup Helper"
echo "========================================"
echo ""

# Check if user is in docker group
if groups | grep -q docker; then
    echo "[OK] User is in docker group"
else
    echo "[INFO] User is not in docker group"
    echo "Adding user to docker group..."
    echo ""
    echo "Please run the following commands:"
    echo "  sudo usermod -aG docker $USER"
    echo "  newgrp docker"
    echo ""
    echo "Or logout and login again."
    echo ""
    read -p "Have you added the user to docker group? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Please add your user to the docker group first."
        exit 1
    fi
fi

# Check if Docker service is running
if systemctl is-active --quiet docker; then
    echo "[OK] Docker service is running"
else
    echo "[INFO] Docker service is not running"
    echo "Attempting to start Docker service..."
    echo ""
    echo "Please run:"
    echo "  sudo systemctl start docker"
    echo "  sudo systemctl enable docker"
    echo ""
    read -p "Have you started Docker service? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Please start Docker service first."
        exit 1
    fi
fi

# Test Docker access
if docker info &> /dev/null; then
    echo "[OK] Docker is accessible"
    echo ""
    echo "You can now run: ./run-local.sh"
else
    echo "[ERROR] Cannot access Docker"
    echo ""
    echo "Troubleshooting:"
    echo "1. Make sure Docker service is running: sudo systemctl status docker"
    echo "2. Add user to docker group: sudo usermod -aG docker $USER"
    echo "3. Logout and login again, or run: newgrp docker"
    echo "4. Try: docker info"
    exit 1
fi












#!/bin/bash
# Fix Port 80 Conflict for Staging Deployment

echo "🔍 Checking what's using port 80..."

# Check for Traefik containers
echo "Checking for Traefik containers..."
docker ps -a | grep traefik

# Check for production containers
echo ""
echo "Checking for production containers..."
docker ps -a | grep multivendor | grep -v staging

# Stop production if running
echo ""
echo "Stopping production containers..."
docker-compose down 2>/dev/null || echo "Production not running or no docker-compose.yml"

# Stop any Traefik containers
echo ""
echo "Stopping any Traefik containers..."
docker ps -a | grep traefik | awk '{print $1}' | xargs -r docker stop 2>/dev/null
docker ps -a | grep traefik | awk '{print $1}' | xargs -r docker rm -f 2>/dev/null

# Check what's using port 80 (requires sudo)
echo ""
echo "Checking what's using port 80 (requires sudo)..."
sudo lsof -i :80 2>/dev/null || sudo netstat -tlnp | grep :80 || echo "Cannot check port 80 without sudo"

echo ""
echo "✅ Cleanup complete. Now try starting staging:"
echo "   docker-compose -f docker-compose.staging.yml up -d --build"


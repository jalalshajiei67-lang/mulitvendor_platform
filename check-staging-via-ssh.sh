#!/bin/bash
# SSH commands to check and fix staging deployment
# Run this on your VPS or via SSH

echo "🔍 Checking Staging Deployment Status"
echo "======================================"
echo ""

# Check if network exists
echo "1. Checking Traefik network..."
if docker network inspect multivendor_network >/dev/null 2>&1; then
    echo "   ✅ Network 'multivendor_network' exists"
    docker network inspect multivendor_network --format '{{.Name}} - {{len .Containers}} containers connected'
else
    echo "   ❌ Network 'multivendor_network' NOT found"
    echo "   Creating network..."
    docker network create multivendor_network --driver bridge
    echo "   ✅ Network created"
fi

echo ""
echo "2. Checking production Traefik..."
if docker ps | grep -q "traefik"; then
    echo "   ✅ Production Traefik is running"
    docker ps --filter "name=traefik" --format "   {{.Names}} - {{.Status}}"
else
    echo "   ⚠️  Production Traefik is NOT running"
    echo "   (This is okay if staging deploys independently)"
fi

echo ""
echo "3. Checking staging containers..."
if docker ps -a | grep -q "staging"; then
    echo "   ✅ Staging containers found:"
    docker ps -a --filter "name=staging" --format "   {{.Names}} - {{.Status}}"
else
    echo "   ⚠️  No staging containers found"
fi

echo ""
echo "4. Checking staging compose file..."
if [ -f "docker-compose.staging.yml" ]; then
    echo "   ✅ docker-compose.staging.yml exists"
else
    echo "   ❌ docker-compose.staging.yml NOT found"
    echo "   Current directory: $(pwd)"
fi

echo ""
echo "======================================"
echo "✅ Diagnostic complete!"
echo ""
echo "To fix network issue, run:"
echo "  docker network create multivendor_network --driver bridge"
echo ""
echo "To deploy staging, run:"
echo "  docker-compose -f docker-compose.staging.yml up -d --build"
echo ""


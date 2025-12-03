#!/bin/bash
# Deploy staging - ensures network exists first

set -e

echo "🚀 Deploying Staging Environment"
echo "================================"
echo ""

# Ensure Traefik network exists
if [ -f "./ensure-traefik-network.sh" ]; then
    ./ensure-traefik-network.sh
else
    # Fallback: create network if it doesn't exist
    if ! docker network inspect multivendor_network >/dev/null 2>&1; then
        echo "Creating multivendor_network..."
        docker network create multivendor_network --driver bridge
    fi
fi

echo ""
echo "Starting staging services..."
docker-compose -f docker-compose.staging.yml up -d --build

echo ""
echo "✅ Staging deployment complete!"
echo ""
echo "Check status:"
echo "  docker-compose -f docker-compose.staging.yml ps"
echo ""
echo "View logs:"
echo "  docker-compose -f docker-compose.staging.yml logs -f"
echo ""


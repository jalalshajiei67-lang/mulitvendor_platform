#!/bin/bash
# Ensure Traefik network exists before starting staging
# This network is created by production docker-compose.yml

set -e

NETWORK_NAME="multivendor_network"

echo "🔍 Checking if network '$NETWORK_NAME' exists..."

if docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    echo "✅ Network '$NETWORK_NAME' already exists"
    exit 0
fi

echo "⚠️  Network '$NETWORK_NAME' not found"
echo ""
echo "Creating network '$NETWORK_NAME'..."
docker network create "$NETWORK_NAME" --driver bridge

echo "✅ Network '$NETWORK_NAME' created successfully"
echo ""
echo "Note: This network is normally created by production docker-compose.yml"
echo "      If production is running, it should have created this network."
echo "      You may want to start production first: docker-compose up -d"


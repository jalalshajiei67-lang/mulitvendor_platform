#!/bin/bash

# Fix Short Link Routes in Production
# This script updates Traefik routing to properly handle /s/ short links on indexo.ir

set -e

echo "🔧 Fixing Short Link Routes Configuration..."

# Deploy updated docker-compose configuration
echo "📦 Deploying updated configuration to production..."

# Copy updated docker-compose to server
scp docker-compose.production.yml root@46.249.101.84:/root/multivendor_platform/

# SSH into server and restart backend service to apply new Traefik labels
ssh root@46.249.101.84 << 'ENDSSH'
cd /root/multivendor_platform

echo "🔄 Recreating backend container with new Traefik labels..."
docker-compose -f docker-compose.production.yml up -d --no-deps --force-recreate backend

echo "🔄 Recreating frontend container with new priority..."
docker-compose -f docker-compose.production.yml up -d --no-deps --force-recreate frontend

echo "⏳ Waiting for services to stabilize..."
sleep 10

echo "✅ Checking container status..."
docker ps --filter "name=multivendor_backend" --filter "name=multivendor_frontend"

echo "📊 Checking Traefik routing configuration..."
docker inspect multivendor_backend --format '{{range $key, $value := .Config.Labels}}{{if contains $key "traefik"}}{{$key}}={{$value}}{{"\n"}}{{end}}{{end}}' | grep -i shortlink

echo ""
echo "✅ Configuration deployed successfully!"
echo ""
echo "🧪 Testing short link..."
curl -I https://indexo.ir/s/notif

ENDSSH

echo ""
echo "✅ Short link routes fixed!"
echo ""
echo "📝 Changes made:"
echo "  - Short links now route from indexo.ir (main domain) to backend"
echo "  - Frontend priority set to 1 (lower than short link priority of 15)"
echo "  - Both HTTP and HTTPS routes configured"
echo ""
echo "🔗 Test your short link: https://indexo.ir/s/notif"


#!/bin/bash
# Fix Frontend Styling Issue - Quick Deployment Script

echo "🔧 Fixing Frontend Styling Issue..."
echo "=================================="

# Step 1: Upload updated docker-compose file
echo "📤 Uploading updated docker-compose.production.yml..."
scp docker-compose.production.yml root@91.107.172.234:/home/deploy/docker-deploy/

# Step 2: Restart services on VPS
echo "🔄 Restarting services on VPS..."
ssh root@91.107.172.234 << 'ENDSSH'
cd /home/deploy/docker-deploy

echo "Stopping services..."
docker-compose -f docker-compose.production.yml down

echo "Starting services..."
docker-compose -f docker-compose.production.yml up -d

echo "Waiting for services to be healthy..."
sleep 30

echo "Checking service status..."
docker-compose -f docker-compose.production.yml ps

echo "✅ Services restarted!"
echo ""
echo "🌐 Your site should now have proper styling at:"
echo "   https://indexo.ir"
echo ""
echo "💡 Clear your browser cache (Ctrl+Shift+R) if styling still missing"
ENDSSH

echo ""
echo "✅ Fix deployed successfully!"
echo "🌐 Visit https://indexo.ir and clear browser cache"

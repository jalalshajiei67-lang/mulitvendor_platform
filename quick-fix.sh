#!/bin/bash
# Quick fix for MEDIA_URL issue

echo "🔧 Fixing MEDIA_URL configuration..."

sshpass -p 'VgHmP7J3xfra' ssh root@91.107.172.234 << 'ENDSSH'
cd /home/deploy/docker-deploy

# Add MEDIA_URL to .env
echo "" >> .env
echo "# Media Files Configuration" >> .env
echo "MEDIA_URL=/media/" >> .env
echo "MEDIA_ROOT=/app/media" >> .env

# Restart backend
docker-compose -f docker-compose.production.yml restart backend

echo "✅ Configuration updated and backend restarted"
echo "Waiting 30 seconds for backend to start..."
sleep 30

docker-compose -f docker-compose.production.yml ps
ENDSSH

echo "✅ Fix applied!"

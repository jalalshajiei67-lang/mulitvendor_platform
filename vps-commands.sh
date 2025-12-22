#!/bin/bash
# Run these commands on your VPS

cd /home/deploy/docker-deploy

# Add MEDIA_URL to .env
echo "" >> .env
echo "# Media Files Configuration" >> .env
echo "MEDIA_URL=/media/" >> .env
echo "MEDIA_ROOT=/app/media" >> .env

# Restart backend
docker-compose -f docker-compose.production.yml restart backend

# Wait and check status
sleep 30
docker-compose -f docker-compose.production.yml ps

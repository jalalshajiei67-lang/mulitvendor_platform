#!/bin/bash
echo "📤 Uploading fixed docker-compose.production.yml..."
scp docker-compose.production.yml root@91.107.172.234:/home/deploy/docker-deploy/

echo "🔄 Restarting services..."
ssh root@91.107.172.234 << 'ENDSSH'
cd /home/deploy/docker-deploy
docker-compose -f docker-compose.production.yml up -d --force-recreate backend
sleep 40
docker-compose -f docker-compose.production.yml ps
echo ""
echo "📋 Backend logs:"
docker logs multivendor_backend --tail=30
ENDSSH

echo "✅ Done!"

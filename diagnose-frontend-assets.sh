#!/bin/bash
# Diagnostic script to check frontend assets and MIME type issues

echo "=== Frontend Container Diagnostics ==="
echo ""

echo "1. Checking if frontend container is running..."
docker ps | grep multivendor_frontend || echo "❌ Frontend container is not running!"

echo ""
echo "2. Checking frontend container logs (last 20 lines)..."
docker logs --tail 20 multivendor_frontend

echo ""
echo "3. Checking if _nuxt directory exists in build output..."
docker exec multivendor_frontend ls -la /app/.output/public/_nuxt/ 2>/dev/null || echo "❌ _nuxt directory not found!"

echo ""
echo "4. Checking _nuxt assets count..."
NUXT_COUNT=$(docker exec multivendor_frontend find /app/.output/public/_nuxt -type f 2>/dev/null | wc -l)
echo "Found $NUXT_COUNT files in _nuxt directory"

echo ""
echo "5. Checking sample asset files..."
docker exec multivendor_frontend ls -la /app/.output/public/_nuxt/assets/ 2>/dev/null | head -5 || echo "❌ No assets found!"

echo ""
echo "6. Testing direct asset request from container..."
docker exec multivendor_frontend curl -I http://localhost:3000/_nuxt/ 2>/dev/null || echo "❌ Cannot reach _nuxt endpoint"

echo ""
echo "7. Checking Traefik routing for frontend..."
docker exec traefik cat /etc/traefik/traefik.yml 2>/dev/null || echo "Traefik config not accessible"

echo ""
echo "8. Testing frontend health..."
docker exec multivendor_frontend curl -s http://localhost:3000/ | head -20 || echo "❌ Frontend not responding"

echo ""
echo "=== Diagnostics Complete ==="
echo ""
echo "If _nuxt directory is missing or empty, you need to rebuild the frontend:"
echo "  docker-compose -f docker-compose.production.yml build frontend"
echo "  docker-compose -f docker-compose.production.yml up -d frontend"


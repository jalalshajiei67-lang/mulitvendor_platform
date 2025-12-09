#!/bin/bash
# Fix SSL certificate issues for staging
# Run this on your VPS: bash fix-ssl-staging.sh

set -e

echo "🔒 Fixing SSL certificate issues for staging..."

cd /root/indexo-staging || exit 1

echo ""
echo "1️⃣ Checking Traefik logs for certificate errors..."
docker logs traefik_staging --tail 50 | grep -i "certificate\|acme\|error" || echo "No certificate errors found in recent logs"

echo ""
echo "2️⃣ Checking if letsencrypt directory exists and has correct permissions..."
if [ -d "./letsencrypt" ]; then
    echo "✅ letsencrypt directory exists"
    ls -la ./letsencrypt/
    
    # Fix permissions if needed
    chmod 600 ./letsencrypt/acme.json 2>/dev/null || echo "acme.json doesn't exist yet (this is normal for first run)"
else
    echo "⚠️  letsencrypt directory doesn't exist, creating it..."
    mkdir -p ./letsencrypt
    chmod 755 ./letsencrypt
fi

echo ""
echo "3️⃣ Checking DNS configuration..."
echo "Testing if domains resolve correctly:"
nslookup api-staging.indexo.ir || echo "⚠️  DNS lookup failed - check your DNS settings"
nslookup staging.indexo.ir || echo "⚠️  DNS lookup failed - check your DNS settings"

echo ""
echo "4️⃣ Checking if Traefik container is running..."
if docker ps | grep -q traefik_staging; then
    echo "✅ Traefik container is running"
else
    echo "❌ Traefik container is not running!"
    echo "   Starting Traefik..."
    docker compose -f docker-compose.staging.yml up -d traefik
    sleep 5
fi

echo ""
echo "5️⃣ Checking Traefik API for certificate status..."
# Try to access Traefik API (if enabled)
docker exec traefik_staging wget -qO- http://localhost:8080/api/http/routers 2>/dev/null | head -20 || echo "⚠️  Traefik API not accessible (this is normal if api.insecure=false)"

echo ""
echo "6️⃣ Testing HTTPS connection..."
echo "Testing https://api-staging.indexo.ir..."
curl -k -I https://api-staging.indexo.ir 2>&1 | head -5 || echo "⚠️  HTTPS connection failed"

echo ""
echo "7️⃣ Recommendations:"
echo ""
echo "If certificates are not being generated, try:"
echo ""
echo "  Option A: Use HTTP challenge instead of TLS challenge (better for some setups)"
echo "    Edit docker-compose.staging.yml and change:"
echo "      - '--certificatesresolvers.myresolver.acme.tlschallenge=true'"
echo "    To:"
echo "      - '--certificatesresolvers.myresolver.acme.httpchallenge=true'"
echo "      - '--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web'"
echo ""
echo "  Option B: Check DNS is pointing to this server:"
echo "    api-staging.indexo.ir should point to: $(curl -s ifconfig.me 2>/dev/null || echo 'your-server-ip')"
echo ""
echo "  Option C: Restart Traefik to retry certificate generation:"
echo "    docker compose -f docker-compose.staging.yml restart traefik"
echo ""
echo "  Option D: Check Traefik logs for detailed errors:"
echo "    docker logs traefik_staging --tail 100 | grep -i acme"
echo ""


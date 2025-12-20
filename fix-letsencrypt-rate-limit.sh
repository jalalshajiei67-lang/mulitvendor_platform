#!/bin/bash
# Fix Let's Encrypt rate limit issue for staging
# Run this on your VPS: bash fix-letsencrypt-rate-limit.sh

set -e

echo "🔒 Fixing Let's Encrypt rate limit issue..."

cd /root/indexo-staging || exit 1

echo ""
echo "📋 Current situation:"
echo "   - Let's Encrypt rate limit: 5 certificates per domain per week"
echo "   - You've hit the limit for api-staging.indexo.ir"
echo "   - Retry after: 2025-12-09 15:00:41 UTC (check logs for exact time)"
echo ""

echo "🔍 Checking for existing certificates..."
if [ -f "./letsencrypt/acme.json" ]; then
    echo "✅ acme.json exists"
    CERT_SIZE=$(stat -f%z ./letsencrypt/acme.json 2>/dev/null || stat -c%s ./letsencrypt/acme.json 2>/dev/null || echo "0")
    if [ "$CERT_SIZE" -gt 100 ]; then
        echo "   Certificate file has content (${CERT_SIZE} bytes)"
        echo "   Checking if certificate is valid..."
        docker exec traefik_staging cat /letsencrypt/acme.json 2>/dev/null | grep -i "api-staging" && echo "   ✅ Certificate for api-staging found" || echo "   ⚠️  No certificate for api-staging found"
    else
        echo "   ⚠️  Certificate file is empty or too small"
    fi
else
    echo "❌ acme.json does not exist"
fi

echo ""
echo "💡 Solutions:"
echo ""
echo "Option 1: Use Let's Encrypt STAGING endpoint (Recommended for testing)"
echo "   - Won't count against rate limits"
echo "   - Certificates won't be trusted by browsers (you'll see warning)"
echo "   - Good for testing until rate limit resets"
echo ""
echo "Option 2: Wait for rate limit to reset"
echo "   - Retry after the time shown in logs"
echo "   - Usually 7 days from first request"
echo ""
echo "Option 3: Use existing certificate if available"
echo "   - Check if certificate was already generated"
echo "   - Reuse it instead of requesting new one"
echo ""

read -p "Do you want to switch to Let's Encrypt STAGING endpoint? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔄 Switching to Let's Encrypt staging endpoint..."
    
    # Backup current docker-compose
    cp docker-compose.staging.yml docker-compose.staging.yml.backup.$(date +%Y%m%d_%H%M%S)
    
    # Update to use staging endpoint
    sed -i 's|https://acme-v02.api.letsencrypt.org/directory|https://acme-staging-v02.api.letsencrypt.org/directory|g' docker-compose.staging.yml
    
    echo "✅ Updated docker-compose.staging.yml to use staging endpoint"
    echo ""
    echo "⚠️  IMPORTANT: Staging certificates will show browser warnings!"
    echo "   This is normal and safe for testing."
    echo ""
    echo "🔄 Restarting Traefik..."
    docker compose -f docker-compose.staging.yml restart traefik
    
    echo ""
    echo "⏳ Waiting 10 seconds for Traefik to start..."
    sleep 10
    
    echo ""
    echo "🔍 Checking Traefik logs..."
    docker logs traefik_staging --tail 20 | grep -i "acme\|certificate" || echo "No certificate messages yet"
    
    echo ""
    echo "✅ Done! Certificates should be generated now (with browser warnings)."
    echo ""
    echo "📝 To switch back to production certificates later:"
    echo "   1. Wait for rate limit to reset (check logs for retry time)"
    echo "   2. Run: sed -i 's|https://acme-staging-v02.api.letsencrypt.org/directory|https://acme-v02.api.letsencrypt.org/directory|g' docker-compose.staging.yml"
    echo "   3. Restart: docker compose -f docker-compose.staging.yml restart traefik"
else
    echo ""
    echo "ℹ️  Keeping production endpoint. You'll need to wait for rate limit to reset."
    echo "   Check Traefik logs for the exact retry time."
fi


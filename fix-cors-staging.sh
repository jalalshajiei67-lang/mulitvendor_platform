#!/bin/bash
# Quick fix script for CORS issues on staging
# Run this on your VPS: bash fix-cors-staging.sh

set -e

echo "🔧 Fixing CORS configuration for staging..."

cd /root/indexo-staging || exit 1

# Backup current .env.staging
cp .env.staging .env.staging.backup.$(date +%Y%m%d_%H%M%S)

# Remove duplicate CORS_ALLOW_ALL_ORIGINS line and ensure CORS_ALLOW_CREDENTIALS is set
sed -i '/^CORS_ALLOW_ALL_ORIGINS=/d' .env.staging

# Add/update CORS settings
if grep -q "^CORS_ALLOW_CREDENTIALS=" .env.staging; then
    sed -i 's/^CORS_ALLOW_CREDENTIALS=.*/CORS_ALLOW_CREDENTIALS=True/' .env.staging
else
    # Add after CORS_ALLOWED_ORIGINS line
    sed -i '/^CORS_ALLOWED_ORIGINS=/a CORS_ALLOW_CREDENTIALS=True' .env.staging
fi

# Ensure CORS_ALLOW_ALL_ORIGINS is set (only once)
if ! grep -q "^CORS_ALLOW_ALL_ORIGINS=" .env.staging; then
    sed -i '/^CORS_ALLOWED_ORIGINS=/a CORS_ALLOW_ALL_ORIGINS=False' .env.staging
fi

# Ensure CORS_ALLOWED_ORIGINS is correct
if ! grep -q "^CORS_ALLOWED_ORIGINS=https://staging.indexo.ir" .env.staging; then
    sed -i 's/^CORS_ALLOWED_ORIGINS=.*/CORS_ALLOWED_ORIGINS=https:\/\/staging.indexo.ir,https:\/\/api-staging.indexo.ir/' .env.staging
fi

echo "✅ Updated .env.staging file"
echo ""
echo "Current CORS settings:"
grep "^CORS_" .env.staging
echo ""

# Copy to .env
cp .env.staging .env
echo "✅ Copied .env.staging to .env"
echo ""

# Restart containers
echo "🔄 Restarting containers..."
docker compose -f docker-compose.staging.yml down
docker compose -f docker-compose.staging.yml up -d --build

echo ""
echo "⏳ Waiting for containers to start..."
sleep 10

echo ""
echo "🔍 Verifying CORS environment variables in container:"
docker exec multivendor_backend_staging printenv | grep CORS || echo "⚠️  Container might not be ready yet. Wait a few seconds and run:"
echo "   docker exec multivendor_backend_staging printenv | grep CORS"
echo ""
echo "✅ Done! Check the logs if issues persist:"
echo "   docker logs multivendor_backend_staging --tail 50"


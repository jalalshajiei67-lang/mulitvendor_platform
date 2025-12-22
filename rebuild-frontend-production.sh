#!/bin/bash
# Rebuild Frontend on Production Server
# Run this script on your production VPS: 91.107.172.234

echo "=== Rebuilding Frontend Container ==="

# Navigate to project directory (adjust path if needed)
cd ~/indexo-production 2>/dev/null || cd ~/indexo-staging 2>/dev/null || cd /home/deploy 2>/dev/null || pwd

# Find docker-compose file
COMPOSE_FILE=$(find . -maxdepth 2 -name "docker-compose.production.yml" -o -name "docker-compose.yml" | head -1)

if [ -z "$COMPOSE_FILE" ]; then
    echo "ERROR: docker-compose.production.yml not found!"
    echo "Current directory: $(pwd)"
    echo "Files:"
    ls -la
    exit 1
fi

echo "Using: $COMPOSE_FILE"
echo "Directory: $(dirname $COMPOSE_FILE)"

cd "$(dirname $COMPOSE_FILE)"

# Rebuild frontend with no cache
echo ""
echo "=== Step 1: Rebuilding frontend (this will take 5-10 minutes) ==="
docker compose -f "$(basename $COMPOSE_FILE)" build --no-cache frontend

if [ $? -ne 0 ]; then
    echo "ERROR: Build failed!"
    exit 1
fi

# Restart frontend container
echo ""
echo "=== Step 2: Restarting frontend container ==="
docker compose -f "$(basename $COMPOSE_FILE)" up -d frontend

# Wait a moment for container to start
sleep 5

# Verify assets are generated
echo ""
echo "=== Step 3: Verifying assets are generated ==="
echo "Checking for CSS files:"
docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.css" 2>/dev/null | head -5

echo ""
echo "Checking for JS files:"
docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.js" 2>/dev/null | head -5

echo ""
echo "=== Step 4: Testing asset serving ==="
# Get a sample asset name
SAMPLE_CSS=$(docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.css" 2>/dev/null | head -1 | xargs basename 2>/dev/null)
if [ ! -z "$SAMPLE_CSS" ]; then
    echo "Testing: /_nuxt/assets/$SAMPLE_CSS"
    docker exec multivendor_frontend curl -I "http://localhost:3000/_nuxt/assets/$SAMPLE_CSS" 2>/dev/null | head -5
fi

echo ""
echo "=== Build Complete! ==="
echo "Check the browser - assets should now load correctly."


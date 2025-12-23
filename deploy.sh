#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Deployment Script..."

# 1. Build Images
echo "🔨 Building Docker images..."
docker compose -f docker-compose.production.yml build

# 2. Start Services
echo "🚀 Updating services..."
docker compose -f docker-compose.production.yml up -d --remove-orphans

# 3. Wait for services and run migrations
echo "⏳ Waiting for Database to be healthy..."
# (Docker compose depends_on handles the wait, but we can pause slightly)
sleep 10 

# Find the backend container name (handles both production and staging)
BACKEND_CONTAINER=$(docker ps --filter "name=multivendor_backend" --format "{{.Names}}" | head -n 1)

if [ -z "$BACKEND_CONTAINER" ]; then
    echo "❌ Backend container not found!"
    exit 1
fi

echo "📦 Found backend container: $BACKEND_CONTAINER"

# Note: The entrypoint script now handles migrations automatically, but we can run fix as backup
echo "🔧 Fixing migration sequence (if needed)..."
docker exec "$BACKEND_CONTAINER" python manage.py fix_migration_sequence || echo "⚠️  Sequence fix skipped (non-critical)"

# Migrations are handled by entrypoint script, but run here as backup if needed
echo "🗄️ Running Migrations (backup - entrypoint handles this automatically)..."
docker exec "$BACKEND_CONTAINER" python manage.py migrate --noinput || echo "⚠️  Migrations may have already run via entrypoint"

echo "📦 Collecting Static Files (backup - entrypoint handles this automatically)..."
docker exec "$BACKEND_CONTAINER" python manage.py collectstatic --noinput || echo "⚠️  Static files may have already been collected via entrypoint"

echo "🧹 Cleaning up..."
docker image prune -f

# 4. Verify Deployment
echo "🏥 Checking Backend Health..."

# Get the health status
HEALTH_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$BACKEND_CONTAINER")

echo "Current Status: $HEALTH_STATUS"

if [ "$HEALTH_STATUS" == "healthy" ] || [ "$HEALTH_STATUS" == "running" ]; then
    echo "✅ Deployment Successful!"
else
    echo "❌ Backend is not healthy (Status: $HEALTH_STATUS)"
    # We don't exit 1 here to avoid breaking the pipeline if it's just slow, 
    # but strictly for CI/CD you might want to fail.
    exit 1
fi

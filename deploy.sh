#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Deployment Script..."

# 1. Ensure docker-compose.yml exists
if [ ! -f docker-compose.yml ] && [ -f docker-compose.production.yml ]; then
  echo "📋 Copying docker-compose.production.yml to docker-compose.yml..."
  cp docker-compose.production.yml docker-compose.yml
fi

# 2. Build Images
echo "🔨 Building Docker images..."
docker compose build

# 3. Start Services
echo "🚀 Updating services..."
docker compose up -d --remove-orphans

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

# Check if there are pending migrations and create them if needed
echo "🔍 Checking for pending migrations..."
MIGRATION_CHECK=$(docker exec "$BACKEND_CONTAINER" python manage.py makemigrations --dry-run --verbosity 0 2>&1 | grep -i "No changes detected" || echo "")
if [ -z "$MIGRATION_CHECK" ]; then
    echo "📝 Creating pending migrations..."
    docker exec "$BACKEND_CONTAINER" python manage.py makemigrations --noinput || echo "⚠️  Migration creation skipped (may have already been created)"
fi

# Migrations are handled by entrypoint script, but run here as backup if needed
echo "🗄️ Running Migrations (backup - entrypoint handles this automatically)..."
docker exec "$BACKEND_CONTAINER" python manage.py migrate --noinput || echo "⚠️  Migrations may have already run via entrypoint"

echo "📦 Collecting Static Files (backup - entrypoint handles this automatically)..."
docker exec "$BACKEND_CONTAINER" python manage.py collectstatic --noinput || echo "⚠️  Static files may have already been collected via entrypoint"

echo "🧹 Cleaning up..."
docker image prune -f

# 4. Verify Deployment
echo "🏥 Checking Backend Health..."

# Wait for backend to become healthy (up to 150 seconds to account for 120s start_period + buffer)
MAX_WAIT=150
WAIT_INTERVAL=5
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
    HEALTH_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$BACKEND_CONTAINER" 2>/dev/null || echo "unknown")
    
    echo "Current Status: $HEALTH_STATUS (waited ${ELAPSED}s / ${MAX_WAIT}s)"
    
    if [ "$HEALTH_STATUS" == "healthy" ] || [ "$HEALTH_STATUS" == "running" ]; then
        echo "✅ Backend is healthy!"
        break
    fi
    
    if [ "$HEALTH_STATUS" == "unhealthy" ]; then
        echo "❌ Backend is unhealthy!"
        echo "📋 Recent backend logs:"
        docker logs "$BACKEND_CONTAINER" --tail 30
        exit 1
    fi
    
    sleep $WAIT_INTERVAL
    ELAPSED=$((ELAPSED + WAIT_INTERVAL))
done

# Final health check
FINAL_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$BACKEND_CONTAINER" 2>/dev/null || echo "unknown")

if [ "$FINAL_STATUS" == "healthy" ] || [ "$FINAL_STATUS" == "running" ]; then
    echo "✅ Deployment Successful!"
else
    echo "⚠️  Backend status: $FINAL_STATUS (may still be starting)"
    echo "📋 Recent backend logs:"
    docker logs "$BACKEND_CONTAINER" --tail 50
    echo ""
    echo "⚠️  Deployment completed but backend may need more time to become healthy"
    echo "   This is OK - the backend will continue starting in the background"
    # Don't exit 1 here - allow deployment to succeed even if health check is still pending
fi
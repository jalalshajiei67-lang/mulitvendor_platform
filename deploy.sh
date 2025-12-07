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

# 3. Run Migrations
echo "⏳ Waiting for Database to be healthy..."
# (Docker compose depends_on handles the wait, but we can pause slightly)
sleep 10 

echo "🗄️ Running Migrations..."
docker exec multivendor_backend python manage.py migrate --noinput

echo "📦 Collecting Static Files..."
docker exec multivendor_backend python manage.py collectstatic --noinput

echo "🧹 Cleaning up..."
docker image prune -f

# 4. Verify Deployment
echo "🏥 Checking Backend Health..."

# Get the health status
HEALTH_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' multivendor_backend)

echo "Current Status: $HEALTH_STATUS"

if [ "$HEALTH_STATUS" == "healthy" ] || [ "$HEALTH_STATUS" == "running" ]; then
    echo "✅ Deployment Successful!"
else
    echo "❌ Backend is not healthy (Status: $HEALTH_STATUS)"
    # We don't exit 1 here to avoid breaking the pipeline if it's just slow, 
    # but strictly for CI/CD you might want to fail.
    exit 1
fi
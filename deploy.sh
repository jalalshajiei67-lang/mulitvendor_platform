#!/bin/bash
set -e

echo "🚀 Starting Deployment Script..."

# 1. Build Images
# We use --no-cache for the final build stage to ensure latest code is picked up
echo "🔨 Building Docker images..."
docker compose build

# 2. Update Containers
echo "🚀 Updating services..."
docker compose up -d --remove-orphans

# 3. Wait for Database
echo "⏳ Waiting for Database to be healthy..."
until [ "$(docker inspect -f '{{.State.Health.Status}}' multivendor_db)" == "healthy" ]; do
    sleep 2
    echo "Waiting..."
done

# 4. Migrations & Static Files
echo "🗄️ Running Migrations..."
docker exec multivendor_backend python manage.py migrate --noinput

echo "📦 Collecting Static Files..."
docker exec multivendor_backend python manage.py collectstatic --noinput

# 5. Health Check
echo "🏥 Checking Health..."

if [ "$(docker inspect -f '{{.State.Health.Status}}' multivendor_backend)" != "healthy" ]; then
    echo "❌ Backend is unhealthy!"
    docker compose logs --tail=50
    exit 1
fi

echo "✅ Deployment Successful! Cleaning up..."
docker image prune -f

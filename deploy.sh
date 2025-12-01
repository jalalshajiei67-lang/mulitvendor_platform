#!/bin/bash
set -e

echo "🚀 Starting Deployment..."

# Build images
echo "🔨 Building Docker images..."
docker compose build --no-cache

# Stop old containers
echo "🛑 Stopping old containers..."
docker compose down

# Start new containers
echo "▶️ Starting services..."
docker compose up -d --remove-orphans

# Wait for database
echo "⏳ Waiting for database..."
until [ "$(docker inspect -f '{{.State.Health.Status}}' multivendor_db 2>/dev/null)" == "healthy" ]; do
    sleep 2
done

# Run migrations
echo "🗄️ Running migrations..."
docker compose exec -T backend python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
docker compose exec -T backend python manage.py collectstatic --noinput

# Cleanup
echo "🧹 Cleaning up..."
docker image prune -f

# Show status
echo "✅ Deployment Complete!"
docker compose ps

#!/bin/bash

# 1. Build Images
echo "🐳 Building Docker images..."
docker compose build

# 2. Start Services (Zero Downtime)
echo "🚀 Starting services..."
docker compose up -d --remove-orphans

# 3. Wait for DB to be ready before migrating
echo "⏳ Waiting for Database..."
sleep 10

# 4. Run Migrations
echo "🔄 Running Migrations..."
docker exec multivendor_backend python manage.py migrate --noinput

# 5. Collect Static Files
echo "📦 Collecting Static Files..."
docker exec multivendor_backend python manage.py collectstatic --noinput

# 6. Clean up
echo "🧹 Cleaning up unused images..."
docker image prune -f

echo "✅ Deployment Complete!"

#!/bin/bash

# Local Docker Testing Script - No Docker Hub Required
# Uses SQLite and builds images from Ubuntu base

set -e

echo "========================================"
echo "   Local Docker Testing (No Docker Hub)"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "[ERROR] Docker is not running!"
    echo "Please start Docker service:"
    echo "  sudo systemctl start docker"
    exit 1
fi

echo "[OK] Docker is running"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "[ERROR] docker-compose is not installed!"
    exit 1
fi

# Use docker compose (v2) if available, otherwise docker-compose (v1)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo "Starting services..."
echo ""
echo "This will:"
echo "  - Build Django backend from Ubuntu base (no external images)"
echo "  - Build Vue.js frontend from Ubuntu base (no external images)"
echo "  - Use SQLite database (no PostgreSQL container needed)"
echo ""
echo "⚠️  First build may take 10-15 minutes (downloading Ubuntu packages)"
echo ""
echo "Access your application at:"
echo "  Frontend: http://localhost:8080"
echo "  Backend:  http://localhost:8000"
echo "  API:      http://localhost:8000/api/"
echo "  Admin:    http://localhost:8000/admin/"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start services (no need for .env.local since we set env vars in docker-compose)
$DOCKER_COMPOSE -f docker-compose.local-nohub.yml up --build


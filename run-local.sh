#!/bin/bash

# Local Docker Testing Script for Linux
# This script starts your multivendor platform locally with Docker

set -e

echo "========================================"
echo "   Local Docker Testing"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed!"
    echo "Please install Docker first:"
    echo "  Ubuntu/Debian: sudo apt-get update && sudo apt-get install docker.io docker-compose"
    echo "  Or visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "[ERROR] Docker is not running!"
    echo "Please start Docker service:"
    echo "  sudo systemctl start docker"
    echo "  sudo systemctl enable docker"
    echo ""
    echo "Or if using Docker Desktop, please start it."
    exit 1
fi

echo "[OK] Docker is running"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "[ERROR] docker-compose is not installed!"
    echo "Please install docker-compose"
    exit 1
fi

# Use docker compose (v2) if available, otherwise docker-compose (v1)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cat > .env.local << EOF
# Local Development Environment Variables
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=local_dev_password_123
DB_HOST=db
DB_PORT=5432
SECRET_KEY=local-dev-secret-key-change-in-production-12345678910
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend
CORS_ALLOWED_ORIGINS=http://localhost,http://localhost:8080,http://localhost:3000
CORS_ALLOW_ALL_ORIGINS=True
EOF
    echo "[OK] Created .env.local"
    echo ""
fi

echo "Starting services..."
echo ""
echo "This will:"
echo "  - Start PostgreSQL database"
echo "  - Build and start Django backend"
echo "  - Build and start Vue.js frontend"
echo ""
echo "Access your application at:"
echo "  Frontend: http://localhost:8080"
echo "  Backend:  http://localhost:8000"
echo "  API:      http://localhost:8000/api/"
echo "  Admin:    http://localhost:8000/admin/"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start services
$DOCKER_COMPOSE --env-file .env.local -f docker-compose.local.yml up --build




#!/bin/bash

# ============================================
# Nuxt Deployment Script
# ============================================

set -e  # Exit on error

echo "🚀 Starting Nuxt Deployment..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cp ENV_VARIABLES_GUIDE.md .env.example
    print_error "Please configure .env file before deploying!"
    exit 1
fi

print_success ".env file found"

# Check Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

print_success "Docker is installed"

# Check Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Docker Compose is installed"

echo ""
echo "📦 Building containers..."
echo ""

# Stop existing containers
print_warning "Stopping existing containers..."
docker-compose down

# Build frontend with no cache
print_warning "Building Nuxt frontend (this may take a few minutes)..."
docker-compose build --no-cache frontend

print_success "Frontend built successfully"

# Build backend if needed
read -p "Do you want to rebuild backend as well? (y/N): " rebuild_backend
if [[ $rebuild_backend =~ ^[Yy]$ ]]; then
    print_warning "Building Django backend..."
    docker-compose build --no-cache backend
    print_success "Backend built successfully"
fi

echo ""
echo "🚀 Starting services..."
echo ""

# Start all services
docker-compose up -d

print_success "All services started"

echo ""
echo "⏳ Waiting for services to be healthy..."
echo ""

# Wait for services to be healthy
sleep 10

# Check service status
if docker-compose ps | grep -q "Up"; then
    print_success "Services are running"
else
    print_error "Some services failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo ""
echo "🔍 Service Status:"
echo ""
docker-compose ps

echo ""
echo "📊 Checking service health..."
echo ""

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend is responding on port 3000"
else
    print_warning "Frontend not responding yet (may still be starting)"
fi

# Check backend
if curl -f http://localhost:8000/api/ > /dev/null 2>&1; then
    print_success "Backend API is responding"
else
    print_warning "Backend API not responding yet"
fi

# Check Nginx
if curl -f http://localhost > /dev/null 2>&1; then
    print_success "Nginx proxy is working"
else
    print_warning "Nginx proxy not responding yet"
fi

echo ""
echo "📝 Useful Commands:"
echo ""
echo "  View logs:           docker-compose logs -f"
echo "  View frontend logs:  docker-compose logs -f frontend"
echo "  View backend logs:   docker-compose logs -f backend"
echo "  Stop services:       docker-compose down"
echo "  Restart frontend:    docker-compose restart frontend"
echo ""

print_success "Deployment complete!"
echo ""
echo "🌐 Access your application:"
echo "  Frontend: http://localhost"
echo "  Backend API: http://localhost/api/"
echo "  Admin Panel: http://localhost/admin/"
echo ""

# Ask if user wants to view logs
read -p "Do you want to view logs now? (y/N): " view_logs
if [[ $view_logs =~ ^[Yy]$ ]]; then
    docker-compose logs -f
fi











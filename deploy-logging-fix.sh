#!/bin/bash
# Quick Fix Deployment Script
# Fixes the logging configuration issue and deploys

set -e

echo "================================================"
echo "🔧 Deploying Logging Configuration Fix"
echo "================================================"
echo ""

PROJECT_DIR="/media/jalal/New Volume/project/mulitvendor_platform"

# Check if we're in the right directory
if [ ! -f "docker-compose.production.yml" ]; then
    echo "❌ Error: docker-compose.production.yml not found"
    echo "   Please run this script from: $PROJECT_DIR"
    exit 1
fi

echo "📍 Working directory: $(pwd)"
echo ""

# Stop backend service
echo "🛑 Stopping backend service..."
docker-compose -f docker-compose.production.yml stop backend
echo "✅ Backend stopped"
echo ""

# Rebuild backend
echo "🔨 Rebuilding backend with fixes..."
docker-compose -f docker-compose.production.yml build --no-cache backend
echo "✅ Backend rebuilt"
echo ""

# Start backend
echo "🚀 Starting backend service..."
docker-compose -f docker-compose.production.yml up -d backend
echo "✅ Backend started"
echo ""

# Wait for backend to initialize
echo "⏳ Waiting for backend to initialize (30 seconds)..."
sleep 30
echo ""

# Check backend status
echo "🏥 Checking backend health..."
STATUS=$(docker-compose -f docker-compose.production.yml ps backend | grep backend | awk '{print $4}' || echo "unknown")
echo "   Status: $STATUS"
echo ""

# Show recent logs
echo "📋 Recent backend logs:"
echo "----------------------------------------"
docker-compose -f docker-compose.production.yml logs --tail=50 backend
echo "----------------------------------------"
echo ""

# Final check
if docker-compose -f docker-compose.production.yml ps backend | grep -q "Up"; then
    echo "✅ Backend is running!"
    echo ""
    echo "Next steps:"
    echo "1. Monitor logs: docker-compose -f docker-compose.production.yml logs -f backend"
    echo "2. Check health: docker-compose -f docker-compose.production.yml ps"
    echo "3. Test API: curl -I http://localhost:8000/api/"
else
    echo "⚠️  Backend may still be starting or has issues"
    echo "   Check logs: docker-compose -f docker-compose.production.yml logs backend"
fi

echo ""
echo "================================================"
echo "✅ Deployment Complete"
echo "================================================"


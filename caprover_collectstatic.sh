#!/bin/bash
# CapRover Static Files Collection Script

echo "🔍 Finding CapRover backend container..."

# Find the backend container (CapRover naming: captain--appname)
CONTAINER=$(docker ps | grep "captain.*backend" | awk '{print $1}' | head -1)

if [ -z "$CONTAINER" ]; then
    echo "Trying alternative pattern..."
    CONTAINER=$(docker ps | grep "multivendor" | grep -v "frontend" | awk '{print $1}' | head -1)
fi

if [ -z "$CONTAINER" ]; then
    echo "❌ Backend container not found. Available containers:"
    docker ps --format "table {{.Names}}\t{{.Image}}"
    exit 1
fi

CONTAINER_NAME=$(docker ps --filter "id=$CONTAINER" --format "{{.Names}}")
echo "✅ Found container: $CONTAINER_NAME (ID: $CONTAINER)"
echo ""

echo "📦 Collecting static files..."
docker exec $CONTAINER python manage.py collectstatic --noinput --clear

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Static files collected successfully!"
    echo ""
    echo "🔄 Restarting container..."
    docker restart $CONTAINER
    echo ""
    echo "✅ Done! Wait 30 seconds then:"
    echo "   1. Clear browser cache (Ctrl+Shift+Delete)"
    echo "   2. Hard refresh admin page (Ctrl+F5)"
    echo "   3. Check Network tab - CSS files should load with 200 OK"
else
    echo ""
    echo "❌ Error collecting static files. Check the output above."
fi


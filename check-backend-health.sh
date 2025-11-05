#!/bin/bash
# Quick health check script for backend

echo "🔍 Checking Backend Health..."
echo ""

# Check if app is responding
echo "1. Testing API endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://multivendor-backend.indexo.ir/api/departments/)
if [ "$HTTP_CODE" == "200" ]; then
    echo "✅ API is responding (HTTP $HTTP_CODE)"
elif [ "$HTTP_CODE" == "502" ]; then
    echo "❌ 502 Bad Gateway - Backend container is not responding"
    echo "   → Check CapRover Dashboard → App Logs"
elif [ "$HTTP_CODE" == "503" ]; then
    echo "⚠️  503 Service Unavailable - Backend is starting up"
else
    echo "⚠️  Unexpected status: HTTP $HTTP_CODE"
fi

echo ""
echo "2. Testing health endpoint (if available)..."
HEALTH_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://multivendor-backend.indexo.ir/health/ 2>/dev/null || echo "000")
if [ "$HEALTH_CODE" == "200" ]; then
    echo "✅ Health endpoint is responding"
else
    echo "ℹ️  Health endpoint not available (this is OK)"
fi

echo ""
echo "📋 Next steps:"
echo "   - Check CapRover Dashboard → multivendor-backend → App Logs"
echo "   - Verify app status is 'Running' (green)"
echo "   - Check environment variables are set correctly"
echo "   - Verify database is running and accessible"


#!/bin/bash
# Quick deployment status checker

echo "🔍 Checking Deployment Status..."
echo "=================================="
echo ""

echo "📋 Recent Git Commits:"
git log --oneline -3
echo ""

echo "🌐 Testing API Endpoints:"
echo ""

echo "1️⃣ Categories API:"
response=$(curl -s -o /dev/null -w "%{http_code}" https://multivendor-backend.indexo.ir/api/categories/)
echo "   Status: $response"
if [ "$response" = "200" ]; then
    echo "   ✅ API is working!"
elif [ "$response" = "403" ]; then
    echo "   ❌ Still getting 403 - Old container running or deployment failed"
else
    echo "   ⚠️  Unexpected status code"
fi
echo ""

echo "2️⃣ Products API:"
response=$(curl -s -o /dev/null -w "%{http_code}" "https://multivendor-backend.indexo.ir/api/products/?page=1&page_size=12")
echo "   Status: $response"
if [ "$response" = "200" ]; then
    echo "   ✅ API is working!"
elif [ "$response" = "403" ]; then
    echo "   ❌ Still getting 403 - Old container running or deployment failed"
else
    echo "   ⚠️  Unexpected status code"
fi
echo ""

echo "=================================="
echo ""
echo "📝 Next Steps:"
echo ""
if [ "$response" = "403" ]; then
    echo "The API is still returning 403. Please:"
    echo ""
    echo "1. Check GitHub Actions:"
    echo "   https://github.com/jalalshajiei67-lang/mulitvendor_platform/actions"
    echo "   - Make sure the deployment workflow completed successfully"
    echo ""
    echo "2. Check CapRover Backend Logs:"
    echo "   https://captain.indexo.ir/"
    echo "   - Go to multivendor-backend app"
    echo "   - Check if you see the new startup sequence with [1/7] through [7/7]"
    echo ""
    echo "3. If deployment succeeded but still 403:"
    echo "   - Go to CapRover dashboard"
    echo "   - Click on multivendor-backend"
    echo "   - Click 'Force Rebuild'"
    echo "   - OR manually restart the container"
    echo ""
else
    echo "✅ API is responding correctly!"
    echo "Your website should now be working at https://indexo.ir/"
fi
















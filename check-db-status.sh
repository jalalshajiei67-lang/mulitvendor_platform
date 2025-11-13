#!/bin/bash
# Check Database Status via CapRover

echo "🔍 Checking Database Status..."
echo "=================================="
echo ""

echo "📊 Testing API Endpoints:"
echo ""

echo "1️⃣ Departments List (should work):"
curl -s https://multivendor-backend.indexo.ir/api/departments/ | jq -r '.count // "Error"'
echo ""

echo "2️⃣ Departments Detail WITHOUT token (should work):"
curl -s https://multivendor-backend.indexo.ir/api/departments/1/ | jq -r '.name // "Error or 403"'
echo ""

echo "3️⃣ Departments Detail WITH invalid token (will fail):"
curl -s -H "Authorization: Token 7670d04d8faf85dd2a5c47127626213fa906f5f2" \
  https://multivendor-backend.indexo.ir/api/departments/1/ | jq -r '.detail // .name // "Success"'
echo ""

echo "4️⃣ Categories count:"
curl -s https://multivendor-backend.indexo.ir/api/categories/ | jq -r '.count // "Error"'
echo ""

echo "5️⃣ Products count:"
curl -s https://multivendor-backend.indexo.ir/api/products/ | jq -r '.count // "Error"'
echo ""

echo "=================================="
echo ""
echo "📝 Analysis:"
echo ""
echo "If detail endpoint WITHOUT token works: ✅ Backend is fine"
echo "If detail endpoint WITH token fails: ❌ Frontend sending invalid token"
echo ""
echo "💡 Solution: Clear browser localStorage"
echo "   1. Open browser console (F12)"
echo "   2. Run: localStorage.clear(); location.reload();"







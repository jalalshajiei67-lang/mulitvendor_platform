#!/bin/bash
# Quick Debug: Test if API is accessible

echo "🔍 Testing API accessibility..."
echo ""

# Test 1: Direct curl (no CSRF)
echo "1️⃣ Testing with curl (no CSRF token):"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:8000/api/categories/
echo ""

# Test 2: With Origin header
echo "2️⃣ Testing with Origin header:"
curl -s -o /dev/null -w "Status: %{http_code}\n" -H "Origin: http://localhost:3000" http://localhost:8000/api/categories/
echo ""

# Test 3: Check CORS preflight
echo "3️⃣ Testing CORS preflight (OPTIONS):"
curl -s -o /dev/null -w "Status: %{http_code}\n" -X OPTIONS -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET" http://localhost:8000/api/categories/
echo ""

# Test 4: Full request
echo "4️⃣ Full test with all headers:"
curl -i -H "Origin: http://localhost:3000" http://localhost:8000/api/categories/ | head -20
echo ""

echo "📊 Analysis:"
echo "  - If all show 403: Check DRF permissions or view-level restrictions"
echo "  - If curl works but browser doesn't: CORS/CSRF issue"
echo "  - If OPTIONS works but GET doesn't: Authentication/permission issue"


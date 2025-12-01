#!/bin/bash

echo "=== Testing Traefik Configuration ==="
echo ""

# Get VPS IP
VPS_IP=$(hostname -I | awk '{print $1}')
echo "VPS IP: $VPS_IP"
echo ""

# Test 1: Traefik Dashboard
echo "1. Testing Traefik Dashboard (port 8080):"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:8080/dashboard/
echo ""

# Test 2: Backend API through Traefik (port 80)
echo "2. Testing Backend API through Traefik:"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost/api/
echo ""

# Test 3: Frontend through Traefik with Host header
echo "3. Testing Frontend through Traefik (with indexo.ir host):"
curl -s -o /dev/null -w "Status: %{http_code}\n" -H "Host: indexo.ir" http://localhost/
echo ""

# Test 4: Direct container access (bypass Traefik)
echo "4. Testing Direct Backend (port 8000):"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:8000/api/
echo ""

echo "5. Testing Direct Frontend (port 3000):"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:3000/
echo ""

# Test 6: Show active routes
echo "6. Traefik Active Routes:"
curl -s http://localhost:8080/api/http/routers | python3 -m json.tool | grep -E '"name"|"rule"|"status"' | head -20
echo ""

echo "=== Test Complete ==="

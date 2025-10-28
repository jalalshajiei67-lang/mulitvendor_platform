#!/bin/bash
# Frontend Diagnostic Script

echo "=========================================="
echo "🔍 FRONTEND DIAGNOSTIC"
echo "=========================================="

echo ""
echo "1️⃣ Checking frontend HTTP response:"
curl -I https://indexo.ir 2>&1 | head -20

echo ""
echo "2️⃣ Checking what's being served:"
curl https://indexo.ir 2>&1 | head -50

echo ""
echo "3️⃣ Checking if backend API is accessible from frontend:"
curl https://multivendor-backend.indexo.ir/api/ 2>&1 | head -10

echo ""
echo "=========================================="
echo "✅ Diagnostic complete!"
echo "=========================================="


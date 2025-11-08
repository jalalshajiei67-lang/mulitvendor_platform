#!/bin/bash
# Diagnostic script to check what's being served

echo "=========================================="
echo "🔍 FRONTEND DIAGNOSTICS"
echo "=========================================="

echo ""
echo "1️⃣ Checking HTTP headers:"
curl -I https://indexo.ir 2>&1

echo ""
echo "=========================================="
echo "2️⃣ Checking actual content (first 100 lines):"
curl -s https://indexo.ir 2>&1 | head -100

echo ""
echo "=========================================="
echo "3️⃣ Checking content length:"
CONTENT=$(curl -s https://indexo.ir)
echo "Content length: ${#CONTENT} characters"

if [[ "$CONTENT" == *"Nothing here yet"* ]]; then
  echo "❌ PROBLEM: Still showing 'Nothing here yet :/' "
elif [[ "$CONTENT" == *"<!DOCTYPE html>"* ]] && [[ "$CONTENT" == *"<div id=\"app\""* ]]; then
  echo "✅ GOOD: Vue.js HTML structure detected!"
elif [[ "$CONTENT" == *"<html"* ]]; then
  echo "⚠️  HTML detected but might not be Vue.js app"
else
  echo "❌ PROBLEM: Not serving HTML"
fi

echo ""
echo "=========================================="
echo "4️⃣ Checking if assets exist:"
curl -I https://indexo.ir/assets/ 2>&1 | head -5

echo ""
echo "=========================================="
echo "5️⃣ Backend API check:"
curl -s https://multivendor-backend.indexo.ir/api/ 2>&1 | head -10

echo ""
echo "=========================================="
echo "✅ Diagnostic complete!"
echo "=========================================="


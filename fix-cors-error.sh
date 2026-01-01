#!/bin/bash
# Fix CORS error and clean Python cache

echo "🔧 Fixing CORS_REPLACE_HTTPS_REFERER error..."
echo ""

cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform"

echo "1️⃣ Cleaning Python bytecode cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo "✅ Cache cleaned"
echo ""

echo "2️⃣ Verifying settings.py..."
if grep -q "CORS_REPLACE_HTTPS_REFERER" multivendor_platform/settings.py; then
    echo "⚠️  Found deprecated setting, removing it..."
    sed -i '/CORS_REPLACE_HTTPS_REFERER/d' multivendor_platform/settings.py
    echo "✅ Removed CORS_REPLACE_HTTPS_REFERER"
else
    echo "✅ No deprecated setting found (already clean)"
fi
echo ""

echo "3️⃣ Running Django system check..."
python manage.py check
echo ""

if [ $? -eq 0 ]; then
    echo "✅ All checks passed!"
    echo ""
    echo "🚀 Now you can start Django:"
    echo "   python manage.py runserver"
else
    echo "⚠️  There are still some issues"
    echo "   Check the errors above"
fi


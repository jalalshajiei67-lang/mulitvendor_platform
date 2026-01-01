#!/bin/bash
# Fix 403 Forbidden Errors in Local Development

echo "🔧 Fixing 403 Forbidden errors for local development..."
echo ""

cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform"

# Create or update .env.local file
cat > .env.local << 'EOF'
# Local Development Settings - Fix 403 Errors
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080
SECRET_KEY=dev-secret-key-for-local-development-only
EOF

echo "✅ Created .env.local file"
echo ""
echo "📋 To apply these settings:"
echo "   1. Stop your Django development server (Ctrl+C)"
echo "   2. Export environment variables:"
echo "      export \$(cat .env.local | xargs)"
echo "   3. Restart Django:"
echo "      python manage.py runserver"
echo ""
echo "Or simply restart your Django server - Django will pick up .env.local automatically if you're using django-environ"


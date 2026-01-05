#!/bin/bash
# Disable Rate Limiting for Local Development

echo "🔧 Disabling rate limiting for local development..."
echo ""

cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform"

# Export environment variables to disable throttling
cat >> .env.local << 'EOF'

# Disable rate limiting for development
DRF_ANON_RATE=10000/hour
DRF_USER_RATE=10000/hour
EOF

echo "✅ Rate limiting disabled in .env.local"
echo ""
echo "🔄 Now restart Django:"
echo "   Stop Django (Ctrl+C)"
echo "   Restart: python manage.py runserver"
echo ""
echo "Or just export the variables now:"
echo "   export DRF_ANON_RATE=10000/hour"
echo "   export DRF_USER_RATE=10000/hour"



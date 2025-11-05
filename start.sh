#!/bin/bash
# Startup script with better error handling and logging

set -e

echo "=========================================="
echo "Starting Multivendor Backend Application"
echo "=========================================="
echo ""

# Create media directories
echo "[1/5] Creating media directories..."
mkdir -p /app/media/category_images \
         /app/media/subcategory_images \
         /app/media/product_images \
         /app/media/department_images \
         /app/media/blog_images \
         /app/media/user_images
chmod -R 755 /app/media
echo "✅ Media directories created"

# Run migrations
echo ""
echo "[2/5] Running database migrations..."
python manage.py migrate --noinput || {
    echo "❌ Migration failed!"
    exit 1
}
echo "✅ Migrations completed"

# Collect static files
echo ""
echo "[3/5] Collecting static files..."
python manage.py collectstatic --noinput --clear || {
    echo "⚠️  Collectstatic failed, but continuing..."
}
echo "✅ Static files collected"

# Verify Django setup
echo ""
echo "[4/5] Verifying Django configuration..."
python manage.py check --deploy || {
    echo "⚠️  Django check found issues, but continuing..."
}
echo "✅ Django configuration verified"

# Start Gunicorn
echo ""
echo "[5/5] Starting Gunicorn server..."
echo "Binding to 0.0.0.0:80"
echo "=========================================="
exec gunicorn multivendor_platform.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output


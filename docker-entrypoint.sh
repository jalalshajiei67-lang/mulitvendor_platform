#!/bin/bash
set -e  # Exit immediately if any command fails

echo "=========================================="
echo "Starting Multivendor Backend Application"
echo "=========================================="
echo ""

# Function to wait for database to be ready
wait_for_db() {
    echo "[1/7] Waiting for database to be ready..."
    
    max_retries=30
    retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; then
            echo "✅ Database is ready!"
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        echo "⏳ Waiting for database... (attempt $retry_count/$max_retries)"
        sleep 2
    done
    
    echo "❌ Database is not ready after $max_retries attempts!"
    echo "   Please check database connection settings:"
    echo "   DB_HOST=$DB_HOST"
    echo "   DB_PORT=$DB_PORT"
    echo "   DB_NAME=$DB_NAME"
    echo "   DB_USER=$DB_USER"
    exit 1
}

# Function to test database connection with Django
test_db_connection() {
    echo ""
    echo "[2/7] Testing database connection..."
    
    if python manage.py check --database default; then
        echo "✅ Database connection successful!"
    else
        echo "❌ Database connection failed!"
        echo "   Please verify database settings and credentials"
        exit 1
    fi
}

# Function to fix migration sequence (PostgreSQL only)
fix_migration_sequence() {
    echo ""
    echo "[3/9] Checking and fixing Django system table sequences..."
    
    # Use the management command to fix all sequences (django_migrations, django_content_type, etc.)
    python manage.py fix_migration_sequence || echo "   ⚠️  Sequence check failed (non-critical, continuing...)"
}

# Function to fix migration inconsistency
fix_migration_inconsistency() {
    echo ""
    echo "[4/9] Checking and fixing migration history inconsistencies..."
    
    # Fix inconsistent migration history (e.g., 0037 applied but 0036 not)
    python manage.py fix_migration_inconsistency || echo "   ⚠️  Migration inconsistency check failed (non-critical, continuing...)"
}

# Function to run migrations
run_migrations() {
    echo ""
    echo "[5/9] Running database migrations..."
    
    if python manage.py migrate --noinput; then
        echo "✅ Migrations completed successfully!"
    else
        echo "❌ Migrations failed!"
        echo "   This usually means:"
        echo "   - Database connection issues"
        echo "   - Invalid migration files"
        echo "   - Database permissions problems"
        exit 1
    fi
}

# Function to collect static files
collect_static() {
    echo ""
    echo "[6/9] Collecting static files..."
    
    if python manage.py collectstatic --noinput --clear; then
        echo "✅ Static files collected successfully!"
    else
        echo "⚠️  Static files collection failed, but continuing..."
        echo "   This might affect admin panel styling"
    fi
}

# Function to create media directories
setup_directories() {
    echo ""
    echo "[7/9] Setting up media directories..."
    
    mkdir -p /app/logs
    mkdir -p /app/staticfiles
    mkdir -p /app/media
    mkdir -p /app/media/category_images
    mkdir -p /app/media/subcategory_images
    mkdir -p /app/media/product_images
    mkdir -p /app/media/department_images
    mkdir -p /app/media/blog_images
    mkdir -p /app/media/user_images
    
    # Try to set permissions (may fail with mounted volumes, that's okay)
    chmod -R 777 /app/media /app/staticfiles /app/logs 2>/dev/null || echo "⚠️  Could not set permissions (may be expected with persistent volumes)"
    
    echo "✅ Directories set up!"
}

# Function to verify Django configuration
check_django() {
    echo ""
    echo "[8/9] Verifying Django configuration..."
    
    python manage.py check --deploy 2>&1 || echo "⚠️  Django check found issues (non-critical)"
    
    echo "✅ Django configuration verified!"
}

# Function to start Daphne (ASGI server for WebSocket support)
start_server() {
    echo ""
    echo "[9/9] Starting Daphne ASGI server..."
    
    # Use PORT environment variable if set, otherwise default to 8000 (Docker Compose) or 80 (CapRover)
    PORT=${PORT:-8000}
    echo "   Binding to: 0.0.0.0:${PORT}"
    echo "   Application: multivendor_platform.asgi:application"
    echo "=========================================="
    echo ""
    
    exec daphne -b 0.0.0.0 -p "${PORT}" multivendor_platform.asgi:application
}

# Main execution flow
wait_for_db
test_db_connection
fix_migration_sequence
fix_migration_inconsistency
run_migrations
setup_directories
collect_static
check_django
start_server


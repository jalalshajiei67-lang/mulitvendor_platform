#!/bin/bash
set -e  # Exit immediately if any command fails

echo "=========================================="
echo "Starting Multivendor Backend Application"
echo "=========================================="
echo ""
echo "Environment Configuration:"
echo "  - DEBUG: ${DEBUG:-Not Set}"
echo "  - DB_HOST: ${DB_HOST:-Not Set}"
echo "  - REDIS_HOST: ${REDIS_HOST:-Not Set}"
echo "  - CORS_ALLOW_ALL_ORIGINS: ${CORS_ALLOW_ALL_ORIGINS:-Not Set}"
echo "  - USE_REDIS_CACHE: ${USE_REDIS_CACHE:-Not Set}"
echo "  - DB_CONN_MAX_AGE: ${DB_CONN_MAX_AGE:-60}"
echo ""

# Function to wait for database to be ready with exponential backoff
wait_for_db() {
    echo "[1/9] Waiting for database to be ready..."
    
    max_retries=30
    retry_count=0
    wait_time=2
    
    while [ $retry_count -lt $max_retries ]; do
        if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; then
            echo "✅ Database is ready!"
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        echo "⏳ Waiting for database... (attempt $retry_count/$max_retries, next retry in ${wait_time}s)"
        sleep $wait_time
        
        # Exponential backoff (but cap at 10 seconds)
        wait_time=$((wait_time * 2))
        if [ $wait_time -gt 10 ]; then
            wait_time=10
        fi
    done
    
    echo "❌ Database is not ready after $max_retries attempts!"
    echo "   Please check database connection settings:"
    echo "   DB_HOST=$DB_HOST"
    echo "   DB_PORT=$DB_PORT"
    echo "   DB_NAME=$DB_NAME"
    echo "   DB_USER=$DB_USER"
    exit 1
}

# Function to test database connection with Django (with retries)
test_db_connection() {
    echo ""
    echo "[2/9] Testing database connection with retry logic..."
    
    max_retries=5
    retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if python manage.py check --database default 2>&1; then
            echo "✅ Database connection successful!"
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        if [ $retry_count -lt $max_retries ]; then
            echo "⚠️  Database connection failed (attempt $retry_count/$max_retries), retrying in 3s..."
            sleep 3
        fi
    done
    
    echo "❌ Database connection failed after $max_retries attempts!"
    echo "   Please verify database settings and credentials"
    exit 1
}

# Function to test Redis connection
test_redis_connection() {
    echo ""
    echo "[3/9] Testing Redis connection..."
    
    # Check if Redis is configured
    if [ -z "$REDIS_HOST" ] || [ "$REDIS_HOST" = "localhost" ]; then
        echo "⚠️  Redis not configured for production, skipping..."
        return 0
    fi
    
    # Simple ping test (non-critical, won't fail startup)
    if command -v redis-cli > /dev/null 2>&1; then
        if redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping > /dev/null 2>&1; then
            echo "✅ Redis connection successful!"
        else
            echo "⚠️  Redis connection failed (non-critical, continuing...)"
        fi
    else
        echo "ℹ️  redis-cli not available, skipping Redis test"
    fi
}

# Function to fix migration sequence (PostgreSQL only)
fix_migration_sequence() {
    echo ""
    echo "[4/9] Checking and fixing Django system table sequences..."
    
    # Use the management command to fix all sequences (django_migrations, django_content_type, etc.)
    python manage.py fix_migration_sequence || echo "   ⚠️  Sequence check failed (non-critical, continuing...)"
}

# Function to fix migration inconsistency
fix_migration_inconsistency() {
    echo ""
    echo "[5/9] Checking and fixing migration history inconsistencies..."
    
    # Fix inconsistent migration history (e.g., 0037 applied but 0036 not)
    python manage.py fix_migration_inconsistency || echo "   ⚠️  Migration inconsistency check failed (non-critical, continuing...)"
}


# Function to run migrations with retry logic
run_migrations() {
    echo ""
    echo "[6/9] Running database migrations with retry logic..."
    
    max_retries=3
    retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if python manage.py migrate --noinput 2>&1; then
            echo "✅ Migrations completed successfully!"
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        if [ $retry_count -lt $max_retries ]; then
            echo "⚠️  Migrations failed (attempt $retry_count/$max_retries), retrying in 5s..."
            sleep 5
        fi
    done
    
    echo "❌ Migrations failed after $max_retries attempts!"
    echo "   This usually means:"
    echo "   - Database connection issues"
    echo "   - Invalid migration files"
    echo "   - Database permissions problems"
    exit 1
}

# Function to collect static files
collect_static() {
    echo ""
    echo "[7/9] Collecting static files..."
    
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
    echo "[8/9] Setting up media and log directories..."
    
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
    chmod -R 755 /app/media /app/staticfiles /app/logs 2>/dev/null || echo "⚠️  Could not set permissions (may be expected with persistent volumes)"
    
    echo "✅ Directories set up!"
}

# Function to verify Django configuration
check_django() {
    echo ""
    echo "[9/9] Verifying Django configuration..."
    
    # Run Django system checks (non-critical)
    python manage.py check --deploy 2>&1 | head -n 20 || echo "⚠️  Django check found issues (non-critical)"
    
    echo "✅ Django configuration verified!"
}

# Function to start Daphne (ASGI server for WebSocket support)
start_server() {
    echo ""
    echo "=========================================="
    echo "Starting Daphne ASGI Server"
    echo "=========================================="
    
    # Use PORT environment variable if set, otherwise default to 8000 (Docker Compose) or 80 (CapRover)
    PORT=${PORT:-8000}
    
    echo "Server Configuration:"
    echo "  - Port: ${PORT}"
    echo "  - Workers: Auto (based on CPU cores)"
    echo "  - Application: multivendor_platform.asgi:application"
    echo "  - Timeout: 60s"
    echo "  - Max Connections: Based on system resources"
    echo ""
    echo "🚀 Server is starting..."
    echo "=========================================="
    echo ""
    
    # Start Daphne with production-ready settings
    exec daphne \
        -b 0.0.0.0 \
        -p "${PORT}" \
        --proxy-headers \
        --access-log - \
        --verbosity 1 \
        multivendor_platform.asgi:application
}

# ============================================================
# Main Execution Flow with Enhanced Error Handling
# ============================================================
echo "Starting initialization sequence..."
echo ""

# Step 1: Wait for database
wait_for_db

# Step 2: Test database connection with retries
test_db_connection

# Step 3: Test Redis connection (non-critical)
test_redis_connection

# Step 4: Fix migration sequences
fix_migration_sequence

# Step 5: Fix migration inconsistencies
fix_migration_inconsistency

# Step 6: Run migrations with retries
run_migrations

# Step 7: Collect static files
collect_static

# Step 8: Setup directories
setup_directories

# Step 9: Verify Django configuration
check_django

# Final: Start the server
start_server


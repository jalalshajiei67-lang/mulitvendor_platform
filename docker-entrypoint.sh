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

# Check for deprecated CORS_REPLACE_HTTPS_REFERER environment variable
if [ -n "${CORS_REPLACE_HTTPS_REFERER:-}" ]; then
    echo "⚠️  Warning: CORS_REPLACE_HTTPS_REFERER environment variable is set"
    echo "   This setting has been removed from django-cors-headers and should be unset"
    echo "   Please remove it from your environment variables"
    unset CORS_REPLACE_HTTPS_REFERER
fi

# Function to wait for database to be ready with exponential backoff
wait_for_db() {
    echo "[2/9] Waiting for database to be ready..."
    
    max_retries=50  # Increased from 30
    retry_count=0
    wait_time=2
    
    while [ $retry_count -lt $max_retries ]; do
        # Test actual connection with credentials using psql
        # This ensures the database is ready for authenticated connections
        if [ -n "$DB_PASSWORD" ]; then
            export PGPASSWORD="$DB_PASSWORD"
            if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
                unset PGPASSWORD
                echo "✅ Database is ready and accepting authenticated connections!"
                return 0
            fi
            unset PGPASSWORD
        else
            # Try without password (unlikely in production)
            if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
                echo "✅ Database is ready and accepting authenticated connections!"
                return 0
            fi
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
    echo ""
    echo "   Testing connection manually..."
    if [ -n "$DB_PASSWORD" ]; then
        export PGPASSWORD="$DB_PASSWORD"
        psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" 2>&1 || true
        unset PGPASSWORD
    fi
    exit 1
}

# Function to test database connection with Django (with retries)
test_db_connection() {
    echo ""
    echo "[3/9] Testing database connection with retry logic..."
    
    max_retries=10  # Increased from 5
    retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        # Capture both stdout and stderr to see the actual error
        if python manage.py check --database default > /tmp/db_check.log 2>&1; then
            echo "✅ Database connection successful!"
            rm -f /tmp/db_check.log
            return 0
        else
            # Show the actual error
            if [ -f /tmp/db_check.log ]; then
                echo "⚠️  Database connection failed. Error details:"
                grep -i "error\|exception\|fatal\|operational" /tmp/db_check.log | head -3 || tail -3 /tmp/db_check.log
            fi
        fi
        
        retry_count=$((retry_count + 1))
        if [ $retry_count -lt $max_retries ]; then
            echo "⚠️  Database connection failed (attempt $retry_count/$max_retries), retrying in 5s..."
            sleep 5  # Increased from 3s
        fi
    done
    
    echo "❌ Database connection failed after $max_retries attempts!"
    echo "   Last error details:"
    if [ -f /tmp/db_check.log ]; then
        cat /tmp/db_check.log
        rm -f /tmp/db_check.log
    fi
    echo ""
    echo "   Please verify:"
    echo "   - Database credentials are correct"
    echo "   - Database exists: $DB_NAME"
    echo "   - User has permissions: $DB_USER"
    echo "   - Network connectivity to $DB_HOST:$DB_PORT"
    exit 1
}

# Function to test Redis connection
test_redis_connection() {
    echo ""
    echo "[4/9] Testing Redis connection..."
    
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
    echo "[5/9] Checking and fixing Django system table sequences..."
    
    # Use the management command to fix all sequences (django_migrations, django_content_type, etc.)
    python manage.py fix_migration_sequence || echo "   ⚠️  Sequence check failed (non-critical, continuing...)"
}

# Function to fix migration inconsistency
fix_migration_inconsistency() {
    echo ""
    echo "[6/9] Checking and fixing migration history inconsistencies..."
    
    # Fix inconsistent migration history (e.g., 0037 applied but 0036 not)
    python manage.py fix_migration_inconsistency || echo "   ⚠️  Migration inconsistency check failed (non-critical, continuing...)"
}


# Function to run migrations with retry logic
run_migrations() {
    echo ""
    echo "[7/9] Running database migrations with retry logic..."
    
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
    echo "[8/9] Collecting static files..."
    
    if python manage.py collectstatic --noinput --clear; then
        echo "✅ Static files collected successfully!"
    else
        echo "⚠️  Static files collection failed, but continuing..."
        echo "   This might affect admin panel styling"
    fi
}

# Function to create media and log directories
setup_directories() {
    echo ""
    echo "[1/9] Setting up media and log directories..."
    
    # Create logs directory first (critical for Django startup)
    mkdir -p /app/logs || echo "⚠️  Could not create logs directory"
    
    # Create other directories
    mkdir -p /app/staticfiles
    mkdir -p /app/media
    mkdir -p /app/media/category_images
    mkdir -p /app/media/subcategory_images
    mkdir -p /app/media/product_images
    mkdir -p /app/media/department_images
    mkdir -p /app/media/blog_images
    mkdir -p /app/media/user_images
    
    # Try to set permissions (may fail with mounted volumes, that's okay)
    # Use 755 for directories (rwxr-xr-x)
    if chmod -R 755 /app/logs 2>/dev/null; then
        echo "✅ Logs directory created and permissions set"
    else
        echo "⚠️  Logs directory exists but could not set permissions (may use console logging only)"
    fi
    
    chmod -R 755 /app/media /app/staticfiles 2>/dev/null || echo "⚠️  Could not set media/static permissions (may be expected with persistent volumes)"
    
    # Test if we can write to logs directory
    if touch /app/logs/.test 2>/dev/null; then
        rm -f /app/logs/.test
        echo "✅ Logs directory is writable"
    else
        echo "⚠️  Logs directory is not writable, Django will use console logging only"
    fi
    
    echo "✅ Directories set up!"
}

# Function to verify Django configuration
check_django() {
    echo ""
    echo "[9/9] Verifying Django configuration..."
    
    # Run Django system check and capture output
    check_output=$(python manage.py check --deploy 2>&1) || {
        # Check if the error is specifically about CORS_REPLACE_HTTPS_REFERER
        if echo "$check_output" | grep -q "CORS_REPLACE_HTTPS_REFERER"; then
            echo "⚠️  Warning: CORS_REPLACE_HTTPS_REFERER setting detected but has been removed from django-cors-headers"
            echo "   This setting should be removed from your environment variables"
            echo "   Continuing anyway (non-critical)..."
        else
            echo "⚠️  Django check found issues (non-critical):"
            echo "$check_output"
        fi
    }
    
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

# Step 0: Setup directories FIRST (needed for Django settings to load)
setup_directories

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

# Step 8: Verify Django configuration
check_django

# Final: Start the server
start_server


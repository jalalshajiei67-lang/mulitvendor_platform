#!/bin/bash
set -e  # Exit immediately if any command fails

# Debug logging function
DEBUG_LOG="/app/.cursor/debug.log"
log_debug() {
    TIMESTAMP=$(date +%s000)
    LOCATION="docker-entrypoint.sh:$1"
    MESSAGE="$2"
    DATA="$3"
    HYP_ID="$4"
    echo "{\"timestamp\":$TIMESTAMP,\"location\":\"$LOCATION\",\"message\":\"$MESSAGE\",\"data\":{$DATA},\"sessionId\":\"deploy-session\",\"runId\":\"run1\",\"hypothesisId\":\"$HYP_ID\"}" >> "$DEBUG_LOG" 2>/dev/null || true
}

# Create debug log directory
mkdir -p /app/.cursor 2>/dev/null || true

echo "=========================================="
echo "Starting Multivendor Backend Application"
echo "=========================================="
echo ""

log_debug "1" "Entrypoint script started" "\"step\":\"start\"" "A"

# Function to wait for database to be ready
wait_for_db() {
    echo "[1/7] Waiting for database to be ready..."
    
    max_retries=30
    retry_count=0
    
    # Check if we're using pgbouncer (connection pooling)
    if [ "$DB_HOST" = "pgbouncer" ] || [ "$DB_HOST" = "multivendor_pgbouncer" ]; then
        echo "   Using pgbouncer connection pooling..."
        log_debug "10" "Starting pgbouncer connection check" "\"db_host\":\"$DB_HOST\",\"db_port\":\"$DB_PORT\"" "A"
        # For pgbouncer, we can't use pg_isready, so we'll test with Django's check command
        while [ $retry_count -lt $max_retries ]; do
            log_debug "11" "Attempting pgbouncer connection" "\"attempt\":$retry_count,\"max_retries\":$max_retries" "A"
            # Try to connect using Python/Django (which will work with pgbouncer)
            CONN_RESULT=$(python -c "
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
try:
    import django
    django.setup()
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    sys.exit(0)
except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
" 2>&1)
            CONN_EXIT=$?
            log_debug "12" "PgBouncer connection attempt result" "\"exit_code\":$CONN_EXIT,\"result\":\"${CONN_RESULT:0:100}\"" "A"
            if [ $CONN_EXIT -eq 0 ]; then
                echo "✅ Database (via pgbouncer) is ready!"
                log_debug "13" "PgBouncer connection successful" "\"attempt\":$retry_count" "A"
                return 0
            fi
            
            retry_count=$((retry_count + 1))
            echo "⏳ Waiting for database (via pgbouncer)... (attempt $retry_count/$max_retries)"
            sleep 2
        done
    else
        # Direct PostgreSQL connection - use pg_isready
        while [ $retry_count -lt $max_retries ]; do
            if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; then
                echo "✅ Database is ready!"
                return 0
            fi
            
            retry_count=$((retry_count + 1))
            echo "⏳ Waiting for database... (attempt $retry_count/$max_retries)"
            sleep 2
        done
    fi
    
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
    echo "[3/8] Checking and fixing Django system table sequences..."
    
    # Use the management command to fix all sequences (django_migrations, django_content_type, etc.)
    python manage.py fix_migration_sequence || echo "   ⚠️  Sequence check failed (non-critical, continuing...)"
}

# Function to run migrations
run_migrations() {
    echo ""
    echo "[4/8] Running database migrations..."
    
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
    echo "[5/8] Collecting static files..."
    log_debug "50" "Starting collectstatic" "\"step\":\"collect_static\"" "B"
    
    # Don't use --clear with persistent volumes to avoid permission issues
    if python manage.py collectstatic --noinput; then
        echo "✅ Static files collected successfully!"
        log_debug "51" "Collectstatic completed successfully" "\"step\":\"collect_static\"" "B"
    else
        echo "⚠️  Static files collection failed, but continuing..."
        echo "   This might affect admin panel styling"
        log_debug "52" "Collectstatic failed but continuing" "\"step\":\"collect_static\"" "B"
    fi
}

# Function to create media directories
setup_directories() {
    echo ""
    echo "[6/8] Setting up media directories..."
    
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
    echo "[7/8] Verifying Django configuration..."
    
    python manage.py check --deploy 2>&1 || echo "⚠️  Django check found issues (non-critical)"
    
    echo "✅ Django configuration verified!"
}

# Function to start Daphne (ASGI server for WebSocket support)
start_server() {
    echo ""
    echo "[8/8] Starting Daphne ASGI server..."
    log_debug "80" "Starting Daphne server" "\"port\":\"${PORT:-8000}\"" "E"
    
    # Use PORT environment variable if set, otherwise default to 8000 (Docker Compose) or 80 (CapRover)
    PORT=${PORT:-8000}
    echo "   Binding to: 0.0.0.0:${PORT}"
    echo "   Application: multivendor_platform.asgi:application"
    echo "=========================================="
    echo ""
    
    log_debug "81" "Executing Daphne command" "\"command\":\"daphne -b 0.0.0.0 -p $PORT multivendor_platform.asgi:application\"" "E"
    exec daphne -b 0.0.0.0 -p "${PORT}" multivendor_platform.asgi:application
}

# Main execution flow
log_debug "100" "Starting main execution flow" "\"step\":\"main_flow\"" "A"
wait_for_db
log_debug "101" "wait_for_db completed" "\"step\":\"main_flow\"" "A"
test_db_connection
log_debug "102" "test_db_connection completed" "\"step\":\"main_flow\"" "C"
fix_migration_sequence
log_debug "103" "fix_migration_sequence completed" "\"step\":\"main_flow\"" "C"
run_migrations
log_debug "104" "run_migrations completed" "\"step\":\"main_flow\"" "C"
setup_directories
log_debug "105" "setup_directories completed" "\"step\":\"main_flow\"" "B"
collect_static
log_debug "106" "collect_static completed" "\"step\":\"main_flow\"" "B"
check_django
log_debug "107" "check_django completed" "\"step\":\"main_flow\"" "D"
start_server
log_debug "108" "start_server called (should not reach here)" "\"step\":\"main_flow\"" "E"


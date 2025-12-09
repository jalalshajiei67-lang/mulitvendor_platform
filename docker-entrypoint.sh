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

# Function to fix all database sequences (PostgreSQL only)
fix_migration_sequence() {
    echo ""
    echo "[3/8] Checking and fixing database sequences..."
    
    # Use Python to fix all sequences (checks DB engine automatically)
    python << 'PYTHON_EOF'
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings'))
django.setup()

from django.db import connection
from django.conf import settings

try:
    # Check if we're using PostgreSQL
    db_engine = settings.DATABASES['default']['ENGINE']
    
    if 'postgresql' not in db_engine.lower():
        print("   Skipping sequence check (not PostgreSQL)")
        sys.exit(0)
    
    print("   Detected PostgreSQL, checking all sequences...")
    
    with connection.cursor() as cursor:
        # Get all sequences and their associated tables
        # This query works with PostgreSQL 9.1+ (more compatible than pg_sequences)
        cursor.execute("""
            SELECT 
                t.oid::regclass::text as table_name,
                a.attname as column_name,
                pg_get_serial_sequence(t.oid::regclass::text, a.attname) as sequence_name
            FROM pg_class t
            JOIN pg_attribute a ON a.attrelid = t.oid
            JOIN pg_namespace n ON n.oid = t.relnamespace
            WHERE n.nspname = 'public'
            AND a.attnum > 0
            AND NOT a.attisdropped
            AND a.attname = 'id'
            AND pg_get_serial_sequence(t.oid::regclass::text, a.attname) IS NOT NULL
            ORDER BY t.relname;
        """)
        
        sequences = cursor.fetchall()
        fixed_count = 0
        
        for table_name, column_name, sequence_name in sequences:
            try:
                # Get max ID from the table
                cursor.execute(f'SELECT MAX("{column_name}") FROM {table_name};')
                max_id_result = cursor.fetchone()
                max_id = max_id_result[0] if max_id_result else None
                
                if max_id is None:
                    # Table is empty, set sequence to 1
                    cursor.execute(f"SELECT setval('{sequence_name}', 1, false);")
                    continue
                
                # Get current sequence value
                cursor.execute(f"SELECT last_value, is_called FROM {sequence_name};")
                seq_result = cursor.fetchone()
                current_seq = seq_result[0] if seq_result else 0
                is_called = seq_result[1] if seq_result else False
                
                # Calculate what the next value would be
                if is_called:
                    next_seq = current_seq + 1
                else:
                    next_seq = current_seq
                
                if next_seq <= max_id:
                    new_seq_value = max_id + 1
                    cursor.execute(f"SELECT setval('{sequence_name}', {new_seq_value}, false);")
                    print(f"   ✓ Fixed {sequence_name}: {next_seq} → {new_seq_value} (max_id: {max_id})")
                    fixed_count += 1
                # else: sequence is correct, no need to print
            except Exception as e:
                # Some tables might have issues, skip silently
                pass
        
        if fixed_count == 0:
            print("   ✓ All sequences are correct")
        else:
            print(f"   ✓ Fixed {fixed_count} sequence(s)")
            
except Exception as e:
    print(f"   ⚠️  Could not check sequences (non-critical): {e}")
    # Don't exit with error - this is a non-critical check
    sys.exit(0)
PYTHON_EOF
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
run_migrations
setup_directories
collect_static
check_django
start_server


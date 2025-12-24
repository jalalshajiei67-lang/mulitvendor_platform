#!/bin/bash
# Quick fix script to reset PostgreSQL password on VPS
# Run this on your VPS: bash quick-fix-vps-password.sh

set -e

echo "=========================================="
echo "🔧 Quick Fix: Database Password Reset"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.production.yml" ]; then
    echo "❌ Error: docker-compose.production.yml not found!"
    echo "   Please run this script from /home/multivendor_platform directory"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    exit 1
fi

# Read password from .env
DB_PASSWORD=$(grep "^DB_PASSWORD=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
DB_USER=$(grep "^DB_USER=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
DB_NAME=$(grep "^DB_NAME=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)

DB_USER=${DB_USER:-postgres}
DB_NAME=${DB_NAME:-multivendor_db}

if [ -z "$DB_PASSWORD" ]; then
    echo "❌ Error: DB_PASSWORD not found in .env file"
    exit 1
fi

echo "✅ Found configuration:"
echo "   DB_USER: $DB_USER"
echo "   DB_NAME: $DB_NAME"
echo "   DB_PASSWORD: ${DB_PASSWORD:0:5}***"
echo ""

# Check if database container is running
DB_CONTAINER=$(docker ps --filter "name=multivendor_db" --format "{{.Names}}" | head -n 1)

if [ -z "$DB_CONTAINER" ]; then
    echo "❌ Error: Database container not running!"
    echo "   Starting database container..."
    docker compose -f docker-compose.production.yml up -d db
    sleep 5
    DB_CONTAINER=$(docker ps --filter "name=multivendor_db" --format "{{.Names}}" | head -n 1)
    if [ -z "$DB_CONTAINER" ]; then
        echo "❌ Error: Could not start database container"
        exit 1
    fi
fi

echo "✅ Database container: $DB_CONTAINER"
echo ""

# Test current password
echo "🔍 Testing current password..."
if docker exec -e PGPASSWORD="$DB_PASSWORD" "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Password is already correct! No need to reset."
    exit 0
fi

echo "⚠️  Password mismatch detected. Resetting password..."
echo ""

# Method 1: Try to reset using trust authentication (if pg_hba allows)
echo "📋 Attempting password reset..."

# Stop the container temporarily to modify pg_hba.conf
echo "   1. Stopping database container..."
docker stop "$DB_CONTAINER"

# Get volume name
VOLUME_NAME=$(docker inspect "$DB_CONTAINER" --format '{{ range .Mounts }}{{ if eq .Destination "/var/lib/postgresql/data" }}{{ .Name }}{{ end }}{{ end }}')

if [ -z "$VOLUME_NAME" ]; then
    echo "❌ Could not find PostgreSQL data volume"
    echo "   Trying alternative method..."
    docker start "$DB_CONTAINER"
    sleep 3
    
    # Try direct password reset (might work if trust is enabled for local)
    echo "   2. Attempting direct password reset..."
    if docker exec "$DB_CONTAINER" psql -U "$DB_USER" -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null; then
        echo "✅ Password reset successful!"
    else
        echo "❌ Direct reset failed. Need to modify pg_hba.conf"
        echo ""
        echo "Please run the full fix script:"
        echo "   ./fix-production-db-password.sh"
        exit 1
    fi
else
    echo "   2. Modifying pg_hba.conf to enable trust authentication..."
    
    # Create temporary container to modify pg_hba.conf
    docker run --rm \
        -v "$VOLUME_NAME:/var/lib/postgresql/data" \
        postgres:15-alpine \
        sh -c "
            cp /var/lib/postgresql/data/pg_hba.conf /var/lib/postgresql/data/pg_hba.conf.backup 2>/dev/null || true
            echo 'local   all             all                                     trust' > /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             127.0.0.1/32            trust' >> /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             ::1/128                 trust' >> /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/postgresql/data/pg_hba.conf
        "
    
    echo "   3. Starting database container..."
    docker start "$DB_CONTAINER"
    
    echo "   4. Waiting for database to be ready..."
    sleep 5
    for i in {1..30}; do
        if docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" > /dev/null 2>&1; then
            break
        fi
        echo "      Waiting... ($i/30)"
        sleep 1
    done
    
    echo "   5. Resetting password..."
    docker exec "$DB_CONTAINER" psql -U "$DB_USER" -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" || {
        echo "❌ Failed to reset password"
        exit 1
    }
    
    echo "   6. Restoring pg_hba.conf..."
    docker stop "$DB_CONTAINER"
    
    docker run --rm \
        -v "$VOLUME_NAME:/var/lib/postgresql/data" \
        postgres:15-alpine \
        sh -c "
            if [ -f /var/lib/postgresql/data/pg_hba.conf.backup ]; then
                cp /var/lib/postgresql/data/pg_hba.conf.backup /var/lib/postgresql/data/pg_hba.conf
            else
                echo 'local   all             all                                     md5' > /var/lib/postgresql/data/pg_hba.conf
                echo 'host    all             all             127.0.0.1/32            md5' >> /var/lib/postgresql/data/pg_hba.conf
                echo 'host    all             all             ::1/128                 md5' >> /var/lib/postgresql/data/pg_hba.conf
                echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/postgresql/data/pg_hba.conf
            fi
        "
    
    echo "   7. Starting database with new password..."
    docker start "$DB_CONTAINER"
    sleep 3
fi

# Verify password
echo ""
echo "🔍 Verifying new password..."
if docker exec -e PGPASSWORD="$DB_PASSWORD" "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Password reset successful!"
    echo ""
    echo "🔄 Restarting backend container to apply changes..."
    BACKEND_CONTAINER=$(docker ps --filter "name=multivendor_backend" --format "{{.Names}}" | head -n 1)
    if [ -n "$BACKEND_CONTAINER" ]; then
        docker restart "$BACKEND_CONTAINER"
        echo "✅ Backend container restarted"
    fi
    echo ""
    echo "✅ All done! The deployment should work now."
else
    echo "⚠️  Could not verify password automatically"
    echo "   Please check manually: docker exec -e PGPASSWORD=\"\$DB_PASSWORD\" $DB_CONTAINER psql -U $DB_USER -c \"SELECT 1;\""
fi


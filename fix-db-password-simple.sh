#!/bin/bash
# Simple script to fix database password on VPS
# Run: bash fix-db-password-simple.sh

set -e

echo "=========================================="
echo "🔧 Fixing Database Password"
echo "=========================================="
echo ""

# Get password from .env
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    exit 1
fi

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
    echo ""
    echo "🔄 Restarting backend container..."
    BACKEND_CONTAINER=$(docker ps --filter "name=multivendor_backend" --format "{{.Names}}" | head -n 1)
    if [ -n "$BACKEND_CONTAINER" ]; then
        docker restart "$BACKEND_CONTAINER"
        echo "✅ Backend container restarted"
    fi
    exit 0
fi

echo "⚠️  Password mismatch detected. Resetting password..."
echo ""

# Stop database
echo "1. Stopping database container..."
docker stop "$DB_CONTAINER"

# Get volume name
VOLUME_NAME=$(docker inspect "$DB_CONTAINER" --format '{{ range .Mounts }}{{ if eq .Destination "/var/lib/postgresql/data" }}{{ .Name }}{{ end }}{{ end }}')

if [ -z "$VOLUME_NAME" ]; then
    echo "❌ Could not find PostgreSQL data volume"
    exit 1
fi

echo "✅ Found volume: $VOLUME_NAME"
echo ""

# Modify pg_hba.conf to enable trust
echo "2. Temporarily enabling trust authentication..."
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

# Start database
echo "3. Starting database container..."
docker start "$DB_CONTAINER"

# Wait for database to be ready
echo "4. Waiting for database to be ready..."
sleep 5
for i in {1..30}; do
    if docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" > /dev/null 2>&1; then
        break
    fi
    echo "   Waiting... ($i/30)"
    sleep 1
done

# Reset password
echo "5. Resetting password..."
docker exec "$DB_CONTAINER" psql -U "$DB_USER" -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" || {
    echo "❌ Failed to reset password"
    exit 1
}

# Restore pg_hba.conf
echo "6. Restoring secure authentication..."
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

# Start database
echo "7. Starting database with new password..."
docker start "$DB_CONTAINER"
sleep 3

# Verify password
echo "8. Verifying new password..."
if docker exec -e PGPASSWORD="$DB_PASSWORD" "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Password reset successful!"
    echo ""
    echo "🔄 Restarting backend container..."
    BACKEND_CONTAINER=$(docker ps --filter "name=multivendor_backend" --format "{{.Names}}" | head -n 1)
    if [ -n "$BACKEND_CONTAINER" ]; then
        docker restart "$BACKEND_CONTAINER"
        echo "✅ Backend container restarted"
    fi
    echo ""
    echo "✅ All done! The deployment should work now."
else
    echo "⚠️  Could not verify password automatically"
    echo "   Please check manually:"
    echo "   docker exec -e PGPASSWORD=\"\$DB_PASSWORD\" $DB_CONTAINER psql -U $DB_USER -c \"SELECT 1;\""
fi


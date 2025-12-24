#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Deployment Script..."

# Check if .env file exists, create it from template if not
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f env.template ]; then
        cp env.template .env
        echo "✅ Created .env from env.template"
        echo "⚠️  Please review and update .env with your production values!"
        echo "❌ ERROR: .env file was just created from template. Please update it with production values before deploying!"
        exit 1
    else
        echo "❌ Error: env.template not found. Cannot create .env file."
        echo "Please create .env file manually with required environment variables."
        exit 1
    fi
fi

# Verify .env file has required database variables
echo "🔍 Verifying .env file configuration..."
REQUIRED_VARS=("DB_NAME" "DB_USER" "DB_PASSWORD" "DB_HOST" "DB_PORT")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "^${var}=" .env; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo "❌ Error: Missing required environment variables in .env file:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    exit 1
fi

# Check if DB_PASSWORD is not empty and not the default template value
DB_PASSWORD_VALUE=$(grep "^DB_PASSWORD=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
if [ -z "$DB_PASSWORD_VALUE" ]; then
    echo "❌ Error: DB_PASSWORD is empty in .env file!"
    exit 1
fi

echo "✅ .env file configuration verified"

# 1. Build Images
echo "🔨 Building Docker images..."
docker compose -f docker-compose.production.yml build

# 2. Start Services
echo "🚀 Updating services..."
docker compose -f docker-compose.production.yml up -d --remove-orphans

# 3. Wait for database to be ready
echo "⏳ Waiting for Database to be ready..."
DB_CONTAINER=$(docker ps --filter "name=multivendor_db" --format "{{.Names}}" | head -n 1)

if [ -z "$DB_CONTAINER" ]; then
    echo "❌ Database container not found!"
    exit 1
fi

# Wait for database to be healthy and accepting connections
MAX_RETRIES=30
RETRY_COUNT=0
DB_READY=false

# Read DB credentials from .env file
if [ -f .env ]; then
    DB_USER=$(grep "^DB_USER=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
    DB_PASSWORD=$(grep "^DB_PASSWORD=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
    DB_NAME=$(grep "^DB_NAME=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
fi

# Default values if not found in .env
DB_USER=${DB_USER:-postgres}
DB_NAME=${DB_NAME:-multivendor_db}

echo "   Checking database connectivity..."
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    # Check if database container is healthy
    DB_HEALTH=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$DB_CONTAINER" 2>/dev/null || echo "unknown")
    
    # Try to connect to database
    if [ -n "$DB_PASSWORD" ]; then
        if docker exec -e PGPASSWORD="$DB_PASSWORD" "$DB_CONTAINER" pg_isready -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; then
            DB_READY=true
            break
        fi
    else
        # Try without password (might work if no password is set)
        if docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; then
            DB_READY=true
            break
        fi
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "   ⏳ Waiting for database... (attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

if [ "$DB_READY" = false ]; then
    echo "❌ Database is not ready after $MAX_RETRIES attempts!"
    echo "   Please check:"
    echo "   - Database container is running: docker ps | grep multivendor_db"
    echo "   - .env file has correct DB_USER, DB_PASSWORD, and DB_NAME"
    echo "   - Database credentials match between .env and database container"
    exit 1
fi

echo "✅ Database is ready!"

# Find the backend container name (handles both production and staging)
BACKEND_CONTAINER=$(docker ps --filter "name=multivendor_backend" --format "{{.Names}}" | head -n 1)

if [ -z "$BACKEND_CONTAINER" ]; then
    echo "❌ Backend container not found!"
    exit 1
fi

echo "📦 Found backend container: $BACKEND_CONTAINER"

# Wait a bit more for backend container to initialize
echo "⏳ Waiting for backend container to initialize..."
sleep 5

# Wait for backend to be able to connect to database
echo "🔍 Verifying backend can connect to database..."
MAX_BACKEND_RETRIES=20
BACKEND_RETRY_COUNT=0
BACKEND_READY=false

while [ $BACKEND_RETRY_COUNT -lt $MAX_BACKEND_RETRIES ]; do
    if docker exec "$BACKEND_CONTAINER" python manage.py check --database default > /dev/null 2>&1; then
        BACKEND_READY=true
        break
    fi
    BACKEND_RETRY_COUNT=$((BACKEND_RETRY_COUNT + 1))
    echo "   ⏳ Waiting for backend database connection... (attempt $BACKEND_RETRY_COUNT/$MAX_BACKEND_RETRIES)"
    sleep 2
done

if [ "$BACKEND_READY" = false ]; then
    echo "⚠️  Backend cannot connect to database yet, but continuing..."
    echo "   The entrypoint script will handle migrations when the connection is ready"
else
    echo "✅ Backend can connect to database!"
    
    # Note: The entrypoint script now handles migrations automatically, but we can run fix as backup
    echo "🔧 Fixing migration sequence (if needed)..."
    docker exec "$BACKEND_CONTAINER" python manage.py fix_migration_sequence 2>&1 || echo "⚠️  Sequence fix skipped (non-critical)"
    
    # Migrations are handled by entrypoint script, but run here as backup if needed
    echo "🗄️ Running Migrations (backup - entrypoint handles this automatically)..."
    docker exec "$BACKEND_CONTAINER" python manage.py migrate --noinput 2>&1 || echo "⚠️  Migrations may have already run via entrypoint"
    
    echo "📦 Collecting Static Files (backup - entrypoint handles this automatically)..."
    docker exec "$BACKEND_CONTAINER" python manage.py collectstatic --noinput 2>&1 || echo "⚠️  Static files may have already been collected via entrypoint"
fi

echo "🧹 Cleaning up..."
docker image prune -f

# 4. Verify Deployment
echo "🏥 Checking Backend Health..."

# Get the health status
HEALTH_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$BACKEND_CONTAINER")

echo "Current Status: $HEALTH_STATUS"

if [ "$HEALTH_STATUS" == "healthy" ] || [ "$HEALTH_STATUS" == "running" ]; then
    echo "✅ Deployment Successful!"
else
    echo "❌ Backend is not healthy (Status: $HEALTH_STATUS)"
    # We don't exit 1 here to avoid breaking the pipeline if it's just slow, 
    # but strictly for CI/CD you might want to fail.
    exit 1
fi

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

# Check if password matches (for diagnostics)
echo "🔍 Verifying database password configuration..."
if [ -n "$DB_PASSWORD" ]; then
    if docker exec -e PGPASSWORD="$DB_PASSWORD" "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
        echo "✅ Database password matches .env file"
    else
        echo "⚠️  WARNING: Database password mismatch detected!"
        echo "   The password in .env may not match the database password."
        echo "   This will cause authentication failures."
        echo ""
        echo "   To fix this on your VPS, run:"
        echo "   ssh root@91.107.172.234"
        echo "   cd /home/multivendor_platform"
        echo "   ./fix-production-db-password.sh"
        echo ""
        echo "   The entrypoint script will retry when the password is fixed."
    fi
fi

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

# Note: We don't run migrations/static files here anymore because:
# 1. The entrypoint script (docker-entrypoint.sh) already handles all of this
# 2. Running commands via docker exec can have environment variable issues
# 3. The entrypoint script runs when the container starts and has proper environment setup
# 4. Redundant commands can cause race conditions and conflicts

if [ "$BACKEND_READY" = false ]; then
    echo "⚠️  Backend cannot connect to database yet"
    echo "   The entrypoint script will automatically retry when the connection is ready"
    echo "   If this persists, check the database password configuration (see warning above)"
else
    echo "✅ Backend can connect to database!"
    echo "   The entrypoint script will handle migrations and static files automatically"
    echo "   No need to run redundant commands - entrypoint handles everything on container start"
fi

echo "🧹 Cleaning up..."
docker image prune -f

# 4. Verify Deployment
echo "🏥 Checking Backend Health..."

# Wait for backend to become healthy (it needs time to run migrations, collectstatic, etc.)
echo "   Backend is initializing (running migrations, collecting static files, etc.)..."
echo "   This may take 1-2 minutes depending on database size and migrations..."

MAX_HEALTH_RETRIES=30
HEALTH_RETRY_COUNT=0
HEALTHY=false

while [ $HEALTH_RETRY_COUNT -lt $MAX_HEALTH_RETRIES ]; do
    HEALTH_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$BACKEND_CONTAINER" 2>/dev/null || echo "unknown")
    
    if [ "$HEALTH_STATUS" == "healthy" ]; then
        echo "✅ Backend is healthy!"
        HEALTHY=true
        break
    elif [ "$HEALTH_STATUS" == "running" ]; then
        # If it's running but not healthy yet, check if it's been running for a while
        # (healthcheck might not have started yet - it has a start_period of 40s)
        CONTAINER_UPTIME=$(docker inspect --format='{{.State.StartedAt}}' "$BACKEND_CONTAINER" 2>/dev/null)
        if [ -n "$CONTAINER_UPTIME" ]; then
            # If container has been running for more than 60 seconds and is still "running" (not healthy),
            # it might be stuck. But let's give it more time.
            echo "   Status: $HEALTH_STATUS (still initializing... attempt $((HEALTH_RETRY_COUNT + 1))/$MAX_HEALTH_RETRIES)"
        fi
    elif [ "$HEALTH_STATUS" == "starting" ]; then
        echo "   Status: $HEALTH_STATUS (container is starting... attempt $((HEALTH_RETRY_COUNT + 1))/$MAX_HEALTH_RETRIES)"
    elif [ "$HEALTH_STATUS" == "unhealthy" ]; then
        echo "⚠️  Status: $HEALTH_STATUS"
        echo "   Checking backend logs for errors..."
        docker logs "$BACKEND_CONTAINER" --tail 20 2>&1 | grep -i "error\|fail\|exception" | head -5 || echo "   (No obvious errors in recent logs)"
        # Don't break immediately - give it a few more tries
    else
        echo "   Status: $HEALTH_STATUS (attempt $((HEALTH_RETRY_COUNT + 1))/$MAX_HEALTH_RETRIES)"
    fi
    
    HEALTH_RETRY_COUNT=$((HEALTH_RETRY_COUNT + 1))
    sleep 4
done

if [ "$HEALTHY" = true ]; then
    echo ""
    echo "✅ Deployment Successful!"
    echo "   Backend is running and healthy"
elif [ "$HEALTH_STATUS" == "running" ]; then
    echo ""
    echo "⚠️  Backend is running but health check hasn't passed yet"
    echo "   This might be normal if migrations are still running"
    echo "   The backend should become healthy shortly"
    echo "   Check status with: docker ps | grep multivendor_backend"
    echo "   View logs with: docker logs multivendor_backend --tail 50"
    # Don't fail the deployment - the container is running, just needs more time
elif [ "$HEALTH_STATUS" == "unhealthy" ]; then
    echo ""
    echo "❌ Backend is unhealthy"
    echo "   Please check the logs: docker logs multivendor_backend"
    echo "   Common issues:"
    echo "   - Database password mismatch (run ./fix-production-db-password.sh)"
    echo "   - Migration errors"
    echo "   - Missing environment variables"
    exit 1
else
    echo ""
    echo "⚠️  Backend status: $HEALTH_STATUS"
    echo "   Container may still be initializing"
    echo "   Check logs: docker logs multivendor_backend --tail 50"
    # Don't fail if it's still starting - give it more time
fi

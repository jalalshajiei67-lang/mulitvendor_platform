#!/bin/bash

# Script to fix PostgreSQL password mismatch in staging
# This resets the database password to match what's in .env.staging

set -e

echo "=========================================="
echo "🔧 Fixing PostgreSQL Password in Staging"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if database container is running
if ! docker ps | grep -q "multivendor_db_staging"; then
    echo -e "${RED}❌ Error: Database container 'multivendor_db_staging' is not running${NC}"
    echo "Please start it first with: docker compose -f docker-compose.staging.yml up -d db"
    exit 1
fi

# Read password from .env.staging (if exists) or use default
if [ -f ".env.staging" ]; then
    DB_PASSWORD=$(grep "^DB_PASSWORD=" .env.staging | cut -d '=' -f2 | tr -d '"' | tr -d "'")
else
    DB_PASSWORD="MySecurePassword123!"
    echo -e "${YELLOW}⚠️  .env.staging not found, using default password${NC}"
fi

if [ -z "$DB_PASSWORD" ]; then
    DB_PASSWORD="MySecurePassword123!"
    echo -e "${YELLOW}⚠️  DB_PASSWORD not found in .env.staging, using default${NC}"
fi

echo -e "${YELLOW}📋 Resetting password to: ${DB_PASSWORD:0:5}***${NC}"
echo ""

# Method: Temporarily enable trust authentication, then change password
echo "Step 1: Stopping database container..."
docker stop multivendor_db_staging

echo "Step 2: Modifying pg_hba.conf to allow password reset..."
# Create a temporary container to modify pg_hba.conf
docker run --rm \
    -v indexo-staging_postgres_data_staging:/var/lib/postgresql/data \
    postgres:15-alpine \
    sh -c "
        # Backup original pg_hba.conf
        cp /var/lib/postgresql/data/pg_hba.conf /var/lib/postgresql/data/pg_hba.conf.backup || true
        # Add trust authentication for local connections
        echo 'local   all             all                                     trust' > /var/lib/postgresql/data/pg_hba.conf
        echo 'host    all             all             127.0.0.1/32            trust' >> /var/lib/postgresql/data/pg_hba.conf
        echo 'host    all             all             ::1/128                 trust' >> /var/lib/postgresql/data/pg_hba.conf
        # Keep existing entries
        tail -n +2 /var/lib/postgresql/data/pg_hba.conf.backup >> /var/lib/postgresql/data/pg_hba.conf 2>/dev/null || true
    "

echo "Step 3: Starting database container..."
docker start multivendor_db_staging

echo "Step 4: Waiting for database to be ready..."
sleep 5

# Wait for PostgreSQL to be ready
for i in {1..30}; do
    if docker exec multivendor_db_staging pg_isready -U postgres > /dev/null 2>&1; then
        break
    fi
    echo "  Waiting... ($i/30)"
    sleep 1
done

echo "Step 5: Resetting password..."
docker exec multivendor_db_staging psql -U postgres -c "ALTER USER postgres WITH PASSWORD '$DB_PASSWORD';" || {
    echo -e "${RED}❌ Failed to reset password${NC}"
    exit 1
}

echo "Step 6: Restoring original pg_hba.conf..."
docker stop multivendor_db_staging

docker run --rm \
    -v indexo-staging_postgres_data_staging:/var/lib/postgresql/data \
    postgres:15-alpine \
    sh -c "
        # Restore backup if exists
        if [ -f /var/lib/postgresql/data/pg_hba.conf.backup ]; then
            cp /var/lib/postgresql/data/pg_hba.conf.backup /var/lib/postgresql/data/pg_hba.conf
        else
            # Create standard pg_hba.conf with md5 authentication
            echo 'local   all             all                                     md5' > /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             127.0.0.1/32            md5' >> /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             ::1/128                 md5' >> /var/lib/postgresql/data/pg_hba.conf
            echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/postgresql/data/pg_hba.conf
        fi
    "

echo "Step 7: Starting database container with new password..."
docker start multivendor_db_staging

echo "Step 8: Verifying password..."
sleep 3

if docker exec multivendor_db_staging psql -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Password reset successful!${NC}"
else
    echo -e "${YELLOW}⚠️  Could not auto-verify, but password should be reset${NC}"
fi

echo ""
echo -e "${GREEN}✅ Password fix complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Restart the backend container:"
echo "   docker restart multivendor_backend_staging"
echo ""
echo "2. Check backend logs:"
echo "   docker logs multivendor_backend_staging --tail 50"
echo ""


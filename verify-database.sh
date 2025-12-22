#!/bin/bash
# Quick database verification script

echo "=== Database Verification ==="
echo ""

# Check if database container is running
echo "1. Checking database container status..."
docker ps | grep multivendor_db
echo ""

# Check database connection
echo "2. Testing database connection..."
docker exec multivendor_db pg_isready -U postgres
echo ""

# List all databases
echo "3. Listing all databases..."
docker exec multivendor_db psql -U postgres -c "\l"
echo ""

# Check current database name from .env
echo "4. Checking database name from environment..."
docker exec multivendor_backend env | grep DB_NAME
echo ""

# Try to connect to the database
echo "5. Attempting to connect to database..."
DB_NAME=$(docker exec multivendor_backend env | grep DB_NAME | cut -d'=' -f2)
echo "Database name from backend: $DB_NAME"
echo ""

# Check if database exists
echo "6. Checking if database '$DB_NAME' exists..."
docker exec multivendor_db psql -U postgres -c "SELECT datname FROM pg_database WHERE datname = '$DB_NAME';"
echo ""

# Try to list tables in the database
echo "7. Listing tables in database '$DB_NAME'..."
docker exec multivendor_db psql -U postgres -d "$DB_NAME" -c "\dt" 2>&1
echo ""

# Check table count
echo "8. Counting tables..."
TABLE_COUNT=$(docker exec multivendor_db psql -U postgres -d "$DB_NAME" -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs)
echo "Number of tables: $TABLE_COUNT"
echo ""

# Check if migrations have been run
echo "9. Checking Django migrations..."
docker exec multivendor_backend python manage.py showmigrations 2>&1 | head -20
echo ""

# Check database size
echo "10. Database size..."
docker exec multivendor_db psql -U postgres -d "$DB_NAME" -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));" 2>/dev/null | xargs
echo ""

echo "=== Verification Complete ==="


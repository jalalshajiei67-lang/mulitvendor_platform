#!/bin/bash
# Database Connection Diagnostic Script
# Run this from your server to diagnose database connection issues

echo "=== Database Connection Diagnostic ==="
echo ""

# Check if we can connect to PostgreSQL container
echo "1. Checking PostgreSQL container..."
docker exec srv-captain--postgres-db psql --version 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ PostgreSQL container is running"
else
    echo "✗ Cannot connect to PostgreSQL container"
    exit 1
fi

echo ""
echo "2. Checking PostgreSQL environment variables..."
docker exec srv-captain--postgres-db env | grep POSTGRES
echo ""

echo "3. Checking database existence..."
docker exec srv-captain--postgres-db psql -U postgres -lqt | cut -d \| -f 1 | grep -qw multivendor-db
if [ $? -eq 0 ]; then
    echo "✓ Database 'multivendor-db' exists"
else
    echo "✗ Database 'multivendor-db' does NOT exist"
    echo "  Available databases:"
    docker exec srv-captain--postgres-db psql -U postgres -lqt | cut -d \| -f 1 | sed 's/^/  - /'
fi

echo ""
echo "4. Testing password authentication..."
docker exec srv-captain--postgres-db psql -U postgres -d postgres -c "SELECT version();" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Password authentication works"
else
    echo "✗ Password authentication failed"
fi

echo ""
echo "5. Checking backend app environment variables..."
echo "  (Run 'caprover env multivendor-backend' to see full list)"
echo ""

echo "=== Recommendations ==="
echo ""
echo "If database doesn't exist, create it:"
echo "  docker exec -it srv-captain--postgres-db psql -U postgres"
echo "  CREATE DATABASE \"multivendor-db\";"
echo "  \\q"
echo ""
echo "If password authentication fails, verify:"
echo "  1. POSTGRES_PASSWORD in PostgreSQL app matches DB_PASSWORD in backend app"
echo "  2. Both are exactly: thisIsAsimplePassword09"
echo ""










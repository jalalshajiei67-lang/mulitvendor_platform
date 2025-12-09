#!/bin/bash

# Database Connection Diagnostic Script
# Run on VPS to diagnose database connection issues

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Database Connection Diagnostic Tool          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Check if database container is running
echo -e "${YELLOW}[1/6] Checking database container...${NC}"
if docker ps --filter "name=multivendor_db" --format "{{.Names}}" | grep -q multivendor_db; then
    echo -e "${GREEN}✓ Database container is running${NC}"
    DB_STATUS=$(docker inspect --format='{{.State.Status}}' multivendor_db)
    echo -e "  Status: ${DB_STATUS}"
else
    echo -e "${RED}✗ Database container is not running!${NC}"
    exit 1
fi

# 2. Check database health
echo ""
echo -e "${YELLOW}[2/6] Checking database health...${NC}"
DB_HEALTH=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' multivendor_db)
echo -e "  Health: ${DB_HEALTH}"

# 3. Check if database is accessible
echo ""
echo -e "${YELLOW}[3/6] Testing database connection...${NC}"
if docker exec multivendor_db pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Database is accepting connections${NC}"
else
    echo -e "${RED}✗ Database is not accepting connections!${NC}"
    exit 1
fi

# 4. Check if database exists
echo ""
echo -e "${YELLOW}[4/6] Checking if database 'multivendor_db' exists...${NC}"
DB_EXISTS=$(docker exec multivendor_db psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='multivendor_db'" 2>/dev/null || echo "")
if [ "$DB_EXISTS" = "1" ]; then
    echo -e "${GREEN}✓ Database 'multivendor_db' exists${NC}"
    
    # Check table count
    TABLE_COUNT=$(docker exec multivendor_db psql -U postgres -d multivendor_db -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'" 2>/dev/null || echo "0")
    echo -e "  Tables: ${TABLE_COUNT}"
    
    if [ "$TABLE_COUNT" = "0" ]; then
        echo -e "${RED}⚠ WARNING: Database exists but has no tables!${NC}"
    fi
else
    echo -e "${RED}✗ Database 'multivendor_db' does not exist!${NC}"
    echo -e "${YELLOW}  Available databases:${NC}"
    docker exec multivendor_db psql -U postgres -c "\l" | grep -E "Name|multivendor"
fi

# 5. Check backend container environment variables
echo ""
echo -e "${YELLOW}[5/6] Checking backend database configuration...${NC}"
if docker ps --filter "name=multivendor_backend" --format "{{.Names}}" | grep -q multivendor_backend; then
    echo -e "${GREEN}✓ Backend container is running${NC}"
    
    DB_HOST=$(docker exec multivendor_backend printenv DB_HOST 2>/dev/null || echo "not set")
    DB_NAME=$(docker exec multivendor_backend printenv DB_NAME 2>/dev/null || echo "not set")
    DB_USER=$(docker exec multivendor_backend printenv DB_USER 2>/dev/null || echo "not set")
    DB_PORT=$(docker exec multivendor_backend printenv DB_PORT 2>/dev/null || echo "not set")
    
    echo -e "  DB_HOST: ${DB_HOST}"
    echo -e "  DB_NAME: ${DB_NAME}"
    echo -e "  DB_USER: ${DB_USER}"
    echo -e "  DB_PORT: ${DB_PORT}"
    
    if [ "$DB_HOST" = "not set" ] || [ "$DB_NAME" = "not set" ]; then
        echo -e "${RED}⚠ WARNING: Database environment variables are not set!${NC}"
    fi
    
    # Check if backend can connect
    echo ""
    echo -e "${YELLOW}[6/6] Testing backend connection to database...${NC}"
    if docker exec multivendor_backend python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()
from django.db import connection
connection.ensure_connection()
print('SUCCESS')
" 2>&1 | grep -q "SUCCESS"; then
        echo -e "${GREEN}✓ Backend can connect to database${NC}"
    else
        echo -e "${RED}✗ Backend cannot connect to database!${NC}"
        echo -e "${YELLOW}  Checking backend logs...${NC}"
        docker logs multivendor_backend --tail 50 | grep -i "database\|error\|connection" | tail -10 || echo "No relevant errors found"
    fi
else
    echo -e "${RED}✗ Backend container is not running!${NC}"
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Diagnostic Complete                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"

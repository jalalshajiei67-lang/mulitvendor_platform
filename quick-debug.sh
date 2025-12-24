#!/bin/bash
# Quick debugging - run all checks at once
# Usage: ssh root@46.249.101.84 "bash -s" < quick-debug.sh

echo "=========================================="
echo "🔍 Quick VPS Debug Report"
echo "=========================================="
echo ""

cd ~/multivendor_platform 2>/dev/null || cd /home/multivendor_platform 2>/dev/null || { echo "❌ Project directory not found"; exit 1; }

echo "1️⃣  Container Status:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.HealthStatus}}" | grep -E "multivendor|traefik|nginx|NAME" || echo "No containers found"
echo ""

echo "2️⃣  Backend Health Check:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
BACKEND_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' multivendor_backend 2>/dev/null || echo "not found")
echo "Status: $BACKEND_STATUS"
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' https://multivendor-backend.indexo.ir/api/ 2>/dev/null || echo "000")
echo "HTTP Response: $HTTP_CODE"
echo ""

echo "3️⃣  Database Connection Test:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f .env ]; then
    DB_PASSWORD=$(grep "^DB_PASSWORD=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'" | xargs)
    if docker exec -e PGPASSWORD="$DB_PASSWORD" multivendor_db psql -U postgres -d multivendor_db -c "SELECT 1;" > /dev/null 2>&1; then
        echo "✅ Database connection: SUCCESS"
    else
        echo "❌ Database connection: FAILED (password mismatch?)"
    fi
else
    echo "⚠️  .env file not found"
fi
echo ""

echo "4️⃣  Recent Backend Errors:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker logs multivendor_backend 2>&1 | grep -i "error\|exception\|fail\|traceback" | tail -5 || echo "No recent errors found"
echo ""

echo "5️⃣  Backend Logs (last 10 lines):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker logs multivendor_backend --tail 10 2>&1
echo ""

echo "6️⃣  Database Configuration:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
grep -E "^DB_(NAME|USER|PASSWORD|HOST|PORT)=" .env 2>/dev/null | sed 's/PASSWORD=.*/PASSWORD=***/' || echo ".env file not found"
echo ""

echo "=========================================="
echo "✅ Debug report complete"
echo "=========================================="


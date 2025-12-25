#!/bin/bash
# VPS Debugging Commands
# Run these commands directly to debug your VPS
# Example: ssh root@46.249.101.84 "bash -s" < vps-debug-commands.sh

VPS_HOST="root@46.249.101.84"
PROJECT_DIR="~/multivendor_platform"

echo "=========================================="
echo "🔍 VPS Debugging Commands"
echo "=========================================="
echo ""
echo "Run these commands to debug your VPS:"
echo ""

cat << 'EOF'
# 1. Check if backend is responding
ssh root@46.249.101.84 "curl -s https://multivendor-backend.indexo.ir/admin/login/ 2>&1 | grep -i 'django\|login\|username\|password' | head -5"

# 2. Check backend container status
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker ps --filter 'name=multivendor_backend' --format 'table {{.Names}}\t{{.Status}}\t{{.HealthStatus}}'"

# 3. Check database container status
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker ps --filter 'name=multivendor_db' --format 'table {{.Names}}\t{{.Status}}\t{{.HealthStatus}}'"

# 4. Check backend logs (last 30 lines)
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker logs multivendor_backend --tail 30 2>&1"

# 5. Check database logs (last 20 lines)
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker logs multivendor_db --tail 20 2>&1"

# 6. Test database connection with current .env password
ssh root@46.249.101.84 "cd ~/multivendor_platform && DB_PASSWORD=\$(grep '^DB_PASSWORD=' .env | cut -d '=' -f2 | tr -d '\"' | tr -d \"'\" | xargs) && docker exec -e PGPASSWORD=\"\$DB_PASSWORD\" multivendor_db psql -U postgres -d multivendor_db -c 'SELECT 1;' 2>&1"

# 7. Check .env file database configuration
ssh root@46.249.101.84 "cd ~/multivendor_platform && grep -E '^DB_(NAME|USER|PASSWORD|HOST|PORT)=' .env"

# 8. Check if backend can connect to database (from inside container)
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker exec multivendor_backend python manage.py check --database default 2>&1 | head -10"

# 9. Check backend health endpoint
ssh root@46.249.101.84 "curl -s -o /dev/null -w '%{http_code}' https://multivendor-backend.indexo.ir/api/ 2>&1"

# 10. Check all container statuses
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -E 'multivendor|traefik|nginx'"

# 11. Check backend environment variables
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker exec multivendor_backend env | grep -E '^DB_|^SECRET_KEY|^DEBUG' | head -10"

# 12. Check if migrations are needed
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker exec multivendor_backend python manage.py showmigrations --plan 2>&1 | tail -20"

# 13. Check database connection from backend container
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker exec multivendor_backend python -c \"import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings'); import django; django.setup(); from django.db import connection; connection.ensure_connection(); print('✅ Database connection successful')\" 2>&1"

# 14. Check recent backend errors
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker logs multivendor_backend 2>&1 | grep -i 'error\|exception\|fail\|traceback' | tail -10"

# 15. Check if database is accepting connections
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker exec multivendor_db pg_isready -U postgres 2>&1"

# 16. Run the comprehensive debug script
ssh root@46.249.101.84 "cd ~/multivendor_platform && git pull origin main 2>&1 && chmod +x debug-and-fix-vps.sh && ./debug-and-fix-vps.sh"

# 17. Fix database password (if needed)
ssh root@46.249.101.84 "cd ~/multivendor_platform && chmod +x fix-db-password-simple.sh && ./fix-db-password-simple.sh"

# 18. Restart backend container
ssh root@46.249.101.84 "cd ~/multivendor_platform && docker restart multivendor_backend && sleep 5 && docker logs multivendor_backend --tail 20"

# 19. Check disk space
ssh root@46.249.101.84 "df -h | grep -E 'Filesystem|/$|/var'"

# 20. Check Docker system info
ssh root@46.249.101.84 "docker system df"

EOF

echo ""
echo "=========================================="
echo "Quick Debug Commands (Copy & Paste)"
echo "=========================================="
echo ""

cat << 'EOF'
# Quick status check
ssh root@46.249.101.84 "cd ~/multivendor_platform && echo '=== Containers ===' && docker ps --format 'table {{.Names}}\t{{.Status}}' | grep multivendor && echo '' && echo '=== Backend Logs (last 10) ===' && docker logs multivendor_backend --tail 10 2>&1"

# Quick database test
ssh root@46.249.101.84 "cd ~/multivendor_platform && DB_PASSWORD=\$(grep '^DB_PASSWORD=' .env | cut -d '=' -f2 | tr -d '\"' | tr -d \"'\" | xargs) && docker exec -e PGPASSWORD=\"\$DB_PASSWORD\" multivendor_db psql -U postgres -c 'SELECT version();' 2>&1 | head -3"

# Quick backend health
ssh root@46.249.101.84 "curl -s -o /dev/null -w 'HTTP Status: %{http_code}\n' https://multivendor-backend.indexo.ir/api/ && echo 'Backend is responding' || echo 'Backend is not responding'"
EOF


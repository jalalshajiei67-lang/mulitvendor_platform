#!/bin/bash

echo "🔍 Diagnosing API 404 Error on VPS"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "1️⃣ Checking Docker containers status..."
echo "----------------------------------------"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "NAME|multivendor|traefik"
echo ""

echo "2️⃣ Checking backend container health..."
echo "----------------------------------------"
BACKEND_CONTAINER=$(docker ps --filter "name=multivendor_backend" --format "{{.Names}}")
if [ -z "$BACKEND_CONTAINER" ]; then
    echo -e "${RED}❌ Backend container not found!${NC}"
else
    echo -e "${GREEN}✅ Backend container: $BACKEND_CONTAINER${NC}"
    echo "Checking health status..."
    docker inspect $BACKEND_CONTAINER --format='{{.State.Health.Status}}' 2>/dev/null || echo "No healthcheck configured"
    echo ""
    echo "Backend logs (last 10 lines):"
    docker logs --tail 10 $BACKEND_CONTAINER 2>&1 | tail -5
fi
echo ""

echo "3️⃣ Testing backend from inside container..."
echo "----------------------------------------"
if [ ! -z "$BACKEND_CONTAINER" ]; then
    echo "Testing http://localhost:8000/api/ from inside backend container..."
    docker exec $BACKEND_CONTAINER curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8000/api/ || echo "curl not available in container"
    echo ""
    echo "Testing /api/categories/ endpoint..."
    docker exec $BACKEND_CONTAINER curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8000/api/categories/ || echo "curl not available in container"
fi
echo ""

echo "4️⃣ Checking Traefik routing..."
echo "----------------------------------------"
TRAEFIK_CONTAINER=$(docker ps --filter "name=traefik" --format "{{.Names}}")
if [ -z "$TRAEFIK_CONTAINER" ]; then
    echo -e "${RED}❌ Traefik container not found!${NC}"
else
    echo -e "${GREEN}✅ Traefik container: $TRAEFIK_CONTAINER${NC}"
    echo "Checking Traefik API (if enabled)..."
    docker exec $TRAEFIK_CONTAINER wget -qO- http://localhost:8080/api/http/routers 2>/dev/null | head -20 || echo "Traefik API not accessible or not enabled"
fi
echo ""

echo "5️⃣ Testing external API endpoints..."
echo "----------------------------------------"
echo "Testing https://api.indexo.ir/api/..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://api.indexo.ir/api/ 2>&1)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
    echo -e "${GREEN}✅ api.indexo.ir/api/ returns: $HTTP_CODE${NC}"
else
    echo -e "${RED}❌ api.indexo.ir/api/ returns: $HTTP_CODE${NC}"
fi

echo ""
echo "Testing https://api.indexo.ir/api/categories/..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://api.indexo.ir/api/categories/ 2>&1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ api.indexo.ir/api/categories/ returns: $HTTP_CODE${NC}"
    echo "Sample response:"
    curl -s https://api.indexo.ir/api/categories/ | head -20
else
    echo -e "${RED}❌ api.indexo.ir/api/categories/ returns: $HTTP_CODE${NC}"
    echo "Full error response:"
    curl -s https://api.indexo.ir/api/categories/ | head -10
fi
echo ""

echo "6️⃣ Checking environment variables..."
echo "----------------------------------------"
if [ -f ".env" ]; then
    echo "API_DOMAIN from .env:"
    grep "^API_DOMAIN=" .env || echo "API_DOMAIN not found in .env"
    echo ""
    echo "ALLOWED_HOSTS from .env:"
    grep "^ALLOWED_HOSTS=" .env || echo "ALLOWED_HOSTS not found in .env"
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
fi
echo ""

echo "7️⃣ Checking frontend container environment..."
echo "----------------------------------------"
FRONTEND_CONTAINER=$(docker ps --filter "name=multivendor_frontend" --format "{{.Names}}")
if [ ! -z "$FRONTEND_CONTAINER" ]; then
    echo "NUXT_PUBLIC_API_BASE in frontend container:"
    docker exec $FRONTEND_CONTAINER env | grep NUXT_PUBLIC_API_BASE || echo "NUXT_PUBLIC_API_BASE not set"
else
    echo -e "${RED}❌ Frontend container not found!${NC}"
fi
echo ""

echo "8️⃣ Checking Traefik labels on backend..."
echo "----------------------------------------"
if [ ! -z "$BACKEND_CONTAINER" ]; then
    echo "Traefik labels:"
    docker inspect $BACKEND_CONTAINER --format='{{range $key, $value := .Config.Labels}}{{$key}}={{$value}}{{"\n"}}{{end}}' | grep traefik
fi
echo ""

echo "9️⃣ Checking DNS resolution..."
echo "----------------------------------------"
echo "Resolving api.indexo.ir..."
nslookup api.indexo.ir 2>/dev/null || dig api.indexo.ir +short 2>/dev/null || echo "DNS tools not available"
echo ""

echo "===================================="
echo "✅ Diagnosis complete!"
echo ""
echo "Next steps:"
echo "1. If backend container is not healthy, check backend logs: docker logs $BACKEND_CONTAINER"
echo "2. If Traefik routing is wrong, check docker-compose.production.yml Traefik labels"
echo "3. If DNS is wrong, verify api.indexo.ir points to this VPS IP"
echo "4. If backend is accessible but frontend still fails, rebuild frontend: docker-compose build --no-cache frontend && docker-compose up -d frontend"


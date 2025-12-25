#!/bin/bash
# Fix script for nginx-backend 502 errors on VPS
# This script updates the nginx config file on the host (not in container)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Nginx-Backend Connection Fix (VPS)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get backend IP address
echo -e "${YELLOW}[1/5] Getting backend IP address...${NC}"
BACKEND_IP=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' multivendor_backend 2>/dev/null)

if [ -z "$BACKEND_IP" ]; then
    echo -e "${RED}✗ Could not determine backend IP address${NC}"
    exit 1
fi

echo "   Backend IP: $BACKEND_IP"

# Find nginx config file location
echo -e "${YELLOW}[2/5] Finding nginx config file...${NC}"
NGINX_CONFIG="/root/multivendor_platform/nginx/nginx.conf"

if [ ! -f "$NGINX_CONFIG" ]; then
    # Try to find it from docker inspect
    NGINX_CONFIG=$(docker inspect multivendor_nginx 2>/dev/null | grep -oP 'Source.*nginx\.conf' | cut -d'"' -f4 | head -1)
    if [ -z "$NGINX_CONFIG" ] || [ ! -f "$NGINX_CONFIG" ]; then
        echo -e "${RED}✗ Could not find nginx config file${NC}"
        echo "   Expected location: /root/multivendor_platform/nginx/nginx.conf"
        exit 1
    fi
fi

echo "   Found config: $NGINX_CONFIG"

# Create backup
echo -e "${YELLOW}[3/5] Creating backup...${NC}"
cp "$NGINX_CONFIG" "${NGINX_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
echo -e "${GREEN}✓ Backup created${NC}"

# Read current config
CURRENT_CONFIG=$(cat "$NGINX_CONFIG")

# Check if upstream already has IP fallback
if echo "$CURRENT_CONFIG" | grep -q "server $BACKEND_IP:8000 backup"; then
    echo -e "${YELLOW}⚠ Config already has IP fallback, updating...${NC}"
fi

# Create improved config
echo -e "${YELLOW}[4/5] Creating improved nginx configuration...${NC}"

# Update upstream backend section to include IP fallback
if echo "$CURRENT_CONFIG" | grep -q "upstream backend"; then
    # Replace upstream backend section
    sed -i.tmp "/^upstream backend {/,/^}/ {
        /^upstream backend {/a\
    server backend:8000 max_fails=3 fail_timeout=30s;\
    server $BACKEND_IP:8000 backup;
        /^}/!d
    }" "$NGINX_CONFIG" 2>/dev/null || {
        # If sed fails, use a different approach
        python3 << PYTHON_SCRIPT
import re

with open('$NGINX_CONFIG', 'r') as f:
    content = f.read()

# Find and replace upstream backend
pattern = r'(upstream backend \{[^}]*server )backend:8000([^}]*\})'
replacement = r'\1backend:8000 max_fails=3 fail_timeout=30s;\n    server $BACKEND_IP:8000 backup;\n\2'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# If pattern didn't match, add IP fallback after existing server line
if new_content == content:
    pattern = r'(upstream backend \{)\s*(server backend:8000[^}]*)(\})'
    replacement = r'\1\n    \2 max_fails=3 fail_timeout=30s;\n    server $BACKEND_IP:8000 backup;\n\3'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('$NGINX_CONFIG', 'w') as f:
    f.write(new_content)
PYTHON_SCRIPT
    }
    
    # Replace $BACKEND_IP placeholder with actual IP
    sed -i "s/\$BACKEND_IP/$BACKEND_IP/g" "$NGINX_CONFIG"
    
    echo -e "${GREEN}✓ Updated upstream backend with IP fallback${NC}"
else
    echo -e "${YELLOW}⚠ Upstream backend section not found, adding it...${NC}"
    # Add upstream section at the beginning
    sed -i "1i upstream backend {\n    server backend:8000 max_fails=3 fail_timeout=30s;\n    server $BACKEND_IP:8000 backup;\n}\n" "$NGINX_CONFIG"
fi

# Add error handling to /api/ location if not present
if ! echo "$CURRENT_CONFIG" | grep -q "proxy_next_upstream"; then
    echo -e "${YELLOW}⚠ Adding error handling to /api/ location...${NC}"
    sed -i '/location \/api\/ {/,/}/ {
        /proxy_set_header X-Forwarded-Proto/a\
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;\
        proxy_next_upstream_tries 2;\
        proxy_next_upstream_timeout 10s;
    }' "$NGINX_CONFIG"
fi

# Test nginx configuration
echo -e "${YELLOW}[5/5] Testing nginx configuration...${NC}"
if docker exec multivendor_nginx nginx -t > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Nginx configuration is valid${NC}"
    
    # Reload nginx
    echo "   Reloading nginx..."
    docker exec multivendor_nginx nginx -s reload
    
    echo ""
    echo -e "${GREEN}✓ Nginx configuration updated and reloaded!${NC}"
    echo ""
    echo "The configuration now includes:"
    echo "  - Backend upstream with IP fallback ($BACKEND_IP:8000)"
    echo "  - Improved error handling and retries"
    echo ""
    echo "Test the connection:"
    echo "  curl -I http://localhost/api/health/"
    echo "  docker logs multivendor_nginx --tail 20"
else
    echo -e "${RED}✗ Nginx configuration has errors!${NC}"
    echo "   Restoring backup..."
    cp "${NGINX_CONFIG}.backup."* "$NGINX_CONFIG" 2>/dev/null || true
    docker exec multivendor_nginx nginx -t
    exit 1
fi

# Cleanup temp file
rm -f "${NGINX_CONFIG}.tmp"

echo ""
echo -e "${GREEN}Fix completed!${NC}"


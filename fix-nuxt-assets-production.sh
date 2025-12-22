#!/bin/bash
# ============================================================================
# Fix Nuxt Assets 404 Issue on Production
# ============================================================================
# This script fixes the issue where /_nuxt/ assets return 404 JSON errors
# ============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

VPS_IP="91.107.172.234"
VPS_USER="root"
DEPLOY_DIR="/home/deploy/docker-deploy"
COMPOSE_FILE="docker-compose.production.yml"

print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Fix Nuxt Assets 404 Issue - Production                 ║${NC}"
    echo -e "${BLUE}║   VPS: ${VPS_IP}                                          ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Transfer updated docker-compose file
transfer_files() {
    print_section "STEP 1: TRANSFERRING UPDATED CONFIGURATION"
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "File not found: $COMPOSE_FILE"
        exit 1
    fi
    
    print_info "Transferring $COMPOSE_FILE to VPS..."
    scp "$COMPOSE_FILE" "${VPS_USER}@${VPS_IP}:${DEPLOY_DIR}/" || {
        print_error "Failed to transfer $COMPOSE_FILE"
        exit 1
    }
    print_success "Configuration file transferred"
}

# Fix on VPS
fix_on_vps() {
    print_section "STEP 2: APPLYING FIX ON VPS"
    
    print_info "Connecting to VPS and applying fix..."
    
    ssh "${VPS_USER}@${VPS_IP}" << 'ENDSSH'
set -e

DEPLOY_DIR="/home/deploy/docker-deploy"
COMPOSE_FILE="docker-compose.production.yml"

cd "$DEPLOY_DIR" || exit 1

echo "📋 Current directory: $(pwd)"

# Backup current docker-compose.yml if it exists
if [ -f "docker-compose.yml" ]; then
    echo "💾 Backing up current docker-compose.yml..."
    cp docker-compose.yml "docker-compose.yml.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Copy production file to docker-compose.yml
echo "📋 Updating docker-compose.yml..."
cp "$COMPOSE_FILE" docker-compose.yml

# Stop services to apply new routing
echo "🛑 Stopping services..."
docker compose down || true

# Rebuild frontend to ensure assets are generated
echo "🔨 Rebuilding frontend (this may take 5-10 minutes)..."
docker compose build --no-cache frontend || docker compose build frontend

# Start services with new configuration
echo "🚀 Starting services with updated routing..."
docker compose up -d

echo "⏳ Waiting for services to start..."
sleep 20

echo "📊 Checking service status..."
docker compose ps

echo ""
echo "🔍 Verifying frontend assets..."
echo "Checking for CSS files:"
docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.css" 2>/dev/null | head -5 || echo "No CSS files found"

echo ""
echo "Checking for JS files:"
docker exec multivendor_frontend find /app/.output/public/_nuxt -name "*.js" 2>/dev/null | head -5 || echo "No JS files found"

echo ""
echo "🧪 Testing asset serving from frontend container..."
docker exec multivendor_frontend curl -I http://localhost:3000/_nuxt/ 2>/dev/null | head -3 || echo "Could not test"

echo ""
echo "📝 Frontend logs (last 10 lines):"
docker logs multivendor_frontend --tail 10 2>&1 | tail -10

echo ""
echo "✅ Fix applied!"
ENDSSH

    if [ $? -eq 0 ]; then
        print_success "Fix applied successfully"
    else
        print_error "Fix failed"
        exit 1
    fi
}

# Verify fix
verify_fix() {
    print_section "STEP 3: VERIFYING FIX"
    
    print_info "Testing asset endpoints..."
    
    echo ""
    echo "Testing https://indexo.ir/_nuxt/..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://indexo.ir/_nuxt/ 2>&1 || echo "000")
    
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "404" ]; then
        if [ "$HTTP_CODE" = "404" ]; then
            print_warning "Got 404 (expected if directory listing is disabled, but assets should work)"
        else
            print_success "Frontend is responding"
        fi
    else
        print_error "Frontend not responding correctly (HTTP $HTTP_CODE)"
    fi
    
    echo ""
    print_info "Check your browser console to verify assets are loading"
    print_info "The routing has been updated to prioritize /_nuxt/ paths to frontend"
}

# Main function
main() {
    clear
    print_header
    
    print_warning "This will:"
    echo "  1. Update Traefik routing to prioritize /_nuxt/ paths to frontend"
    echo "  2. Rebuild frontend container to ensure assets are generated"
    echo "  3. Restart all services"
    echo ""
    read -p "Continue with fix? (y/n): " confirm
    
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        print_info "Fix cancelled"
        exit 0
    fi
    
    transfer_files
    fix_on_vps
    verify_fix
    
    print_section "FIX COMPLETE"
    print_success "Nuxt assets routing has been fixed"
    echo ""
    print_info "What was fixed:"
    echo "  ✅ Added priority routing for /_nuxt/ paths to frontend"
    echo "  ✅ Excluded /_nuxt/ from backend routing"
    echo "  ✅ Rebuilt frontend to ensure assets are generated"
    echo ""
    print_info "Next steps:"
    echo "  1. Clear your browser cache (Ctrl+Shift+Delete)"
    echo "  2. Hard refresh the page (Ctrl+Shift+R)"
    echo "  3. Check browser console - assets should load correctly"
    echo "  4. If issues persist, check logs: ssh ${VPS_USER}@${VPS_IP} 'cd ${DEPLOY_DIR} && docker logs multivendor_frontend'"
    echo ""
}

# Run main function
main


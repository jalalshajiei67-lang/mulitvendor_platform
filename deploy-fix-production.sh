#!/bin/bash
# ============================================================================
# Deploy Fixed Production Configuration
# ============================================================================
# This script deploys the updated docker-compose.production.yml to fix
# the production website issues
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
    echo -e "${BLUE}║   Deploy Fixed Production Configuration                   ║${NC}"
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

# Transfer files to VPS
transfer_files() {
    print_section "STEP 1: TRANSFERRING FILES TO VPS"
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "File not found: $COMPOSE_FILE"
        exit 1
    fi
    
    print_info "Transferring $COMPOSE_FILE to VPS..."
    scp "$COMPOSE_FILE" "${VPS_USER}@${VPS_IP}:${DEPLOY_DIR}/" || {
        print_error "Failed to transfer $COMPOSE_FILE"
        exit 1
    }
    print_success "Files transferred successfully"
}

# Deploy on VPS
deploy_on_vps() {
    print_section "STEP 2: DEPLOYING ON VPS"
    
    print_info "Connecting to VPS and deploying..."
    
    ssh "${VPS_USER}@${VPS_IP}" << 'ENDSSH'
set -e

DEPLOY_DIR="/home/deploy/docker-deploy"
COMPOSE_FILE="docker-compose.production.yml"

cd "$DEPLOY_DIR" || exit 1

echo "📋 Current directory: $(pwd)"
echo "📋 Checking docker-compose file..."

if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ docker-compose.production.yml not found!"
    exit 1
fi

echo "✅ Found $COMPOSE_FILE"

# Backup current docker-compose.yml if it exists
if [ -f "docker-compose.yml" ]; then
    echo "💾 Backing up current docker-compose.yml..."
    cp docker-compose.yml "docker-compose.yml.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Copy production file to docker-compose.yml
echo "📋 Copying $COMPOSE_FILE to docker-compose.yml..."
cp "$COMPOSE_FILE" docker-compose.yml

echo "🔨 Pulling latest images..."
docker compose pull || true

echo "🔨 Building images..."
docker compose build --no-cache backend frontend || docker compose build backend frontend

echo "🛑 Stopping existing services..."
docker compose down || true

echo "🚀 Starting services with new configuration..."
docker compose up -d

echo "⏳ Waiting for services to start..."
sleep 15

echo "📊 Checking service status..."
docker compose ps

echo "✅ Deployment complete!"
ENDSSH

    if [ $? -eq 0 ]; then
        print_success "Deployment completed successfully"
    else
        print_error "Deployment failed"
        exit 1
    fi
}

# Verify deployment
verify_deployment() {
    print_section "STEP 3: VERIFYING DEPLOYMENT"
    
    print_info "Checking services on VPS..."
    
    ssh "${VPS_USER}@${VPS_IP}" << 'ENDSSH'
cd /home/deploy/docker-deploy

echo "📊 Container status:"
docker compose ps

echo ""
echo "🏥 Health checks:"
echo "Backend:"
docker inspect multivendor_backend --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' 2>/dev/null || echo "unknown"

echo "Database:"
docker exec multivendor_db pg_isready -U postgres 2>/dev/null && echo "✅ Ready" || echo "❌ Not ready"

echo "pgBouncer:"
docker exec multivendor_pgbouncer psql -h localhost -U pgbouncer -d pgbouncer -c 'SHOW POOLS;' > /dev/null 2>&1 && echo "✅ Ready" || echo "❌ Not ready"

echo ""
echo "📝 Recent backend logs:"
docker logs multivendor_backend --tail 20 2>&1 | tail -10
ENDSSH

    print_success "Verification complete"
}

# Main function
main() {
    clear
    print_header
    
    print_warning "This will update production with the fixed configuration"
    print_warning "Services will be restarted during deployment"
    echo ""
    read -p "Continue with deployment? (y/n): " confirm
    
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        print_info "Deployment cancelled"
        exit 0
    fi
    
    transfer_files
    deploy_on_vps
    verify_deployment
    
    print_section "DEPLOYMENT COMPLETE"
    print_success "Production has been updated with the fixed configuration"
    echo ""
    print_info "Next steps:"
    echo "  1. Test frontend: https://indexo.ir"
    echo "  2. Test API: https://api.indexo.ir/api/"
    echo "  3. Check logs: ssh ${VPS_USER}@${VPS_IP} 'cd ${DEPLOY_DIR} && docker compose logs -f'"
    echo ""
}

# Run main function
main


#!/bin/bash
# ============================================================================
# ONE-LINER CRISIS RECOVERY - Copy and paste this entire block to VPS
# ============================================================================
# Usage: Copy everything between the START and END markers and paste into VPS
# ============================================================================

# START COPY FROM HERE
cd /root && \
cat > crisis-recovery-production.sh << 'SCRIPT_END'
#!/bin/bash
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
COMPOSE_FILE="docker-compose.production.yml"
BACKUP_DIR="/root/crisis-backups-$(date +%Y%m%d-%H%M%S)"
print_section() { echo ""; echo -e "${BLUE}========================================${NC}"; echo -e "${BLUE}$1${NC}"; echo -e "${BLUE}========================================${NC}"; echo ""; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
preflight_checks() {
    print_section "STEP 1: PRE-FLIGHT CHECKS"
    if [ ! -f "$COMPOSE_FILE" ] && [ ! -f "docker-compose.yml" ]; then
        print_error "Docker compose file not found!"
        exit 1
    fi
    [ -f "docker-compose.yml" ] && COMPOSE_FILE="docker-compose.yml"
    print_success "Found docker-compose file: $COMPOSE_FILE"
    command -v docker > /dev/null || { print_error "Docker not installed!"; exit 1; }
    print_success "Docker is installed"
}
create_backup() {
    print_section "STEP 2: CREATING BACKUP"
    mkdir -p "$BACKUP_DIR"
    print_info "Backup directory: $BACKUP_DIR"
    docker exec multivendor_db pg_dump -U postgres multivendor_db > "$BACKUP_DIR/database.sql" 2>/dev/null && print_success "Database backed up" || print_warning "Could not backup database"
    docker volume ls > "$BACKUP_DIR/volumes-list.txt" 2>/dev/null || true
    print_success "Backup completed"
}
diagnose_issues() {
    print_section "STEP 3: DIAGNOSING ISSUES"
    print_info "Checking volumes..."
    docker volume ls --format "{{.Name}}" | grep -E "(postgres|static|media|redis)" || print_error "No volumes found"
    print_info "Checking network..."
    docker network ls | grep -q "multivendor_network" && print_success "Network exists" || print_error "Network NOT found"
    print_info "Checking database..."
    if docker ps -a --format "{{.Names}}" | grep -q "^multivendor_db$"; then
        DB_STATUS=$(docker inspect multivendor_db --format '{{.State.Status}}' 2>/dev/null || echo "not-found")
        [ "$DB_STATUS" = "running" ] && print_success "Database running" || print_error "Database status: $DB_STATUS"
        docker exec multivendor_db pg_isready -U postgres > /dev/null 2>&1 && print_success "Database accepting connections" || print_error "Database NOT accepting connections"
    else
        print_error "Database container NOT found"
    fi
    print_info "Checking backend..."
    if docker ps -a --format "{{.Names}}" | grep -q "^multivendor_backend$"; then
        BACKEND_STATUS=$(docker inspect multivendor_backend --format '{{.State.Status}}' 2>/dev/null || echo "not-found")
        [ "$BACKEND_STATUS" = "running" ] && print_success "Backend running" || print_error "Backend status: $BACKEND_STATUS"
    else
        print_error "Backend container NOT found"
    fi
    print_info "Checking volume mounts..."
    BACKEND_STATIC=$(docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/static"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")
    NGINX_STATIC=$(docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/static"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")
    [ "$BACKEND_STATIC" = "$NGINX_STATIC" ] && [ -n "$BACKEND_STATIC" ] && print_success "Static volumes match: $BACKEND_STATIC" || print_error "Static volume mismatch!"
    BACKEND_MEDIA=$(docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/media"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")
    NGINX_MEDIA=$(docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/media"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")
    [ "$BACKEND_MEDIA" = "$NGINX_MEDIA" ] && [ -n "$BACKEND_MEDIA" ] && print_success "Media volumes match: $BACKEND_MEDIA" || print_error "Media volume mismatch!"
}
fix_volumes() {
    print_section "STEP 4: FIXING VOLUMES"
    docker volume ls | grep -qE "^postgres_data$|multivendor.*postgres" || docker volume create postgres_data || docker volume create multivendor_postgres_data || true
    docker volume ls | grep -qE "^static_files$|multivendor.*static" || docker volume create static_files || docker volume create multivendor_static_files || true
    docker volume ls | grep -qE "^media_files$|multivendor.*media" || docker volume create media_files || docker volume create multivendor_media_files || true
    docker volume ls | grep -qE "^redis_data$|multivendor.*redis" || docker volume create redis_data || docker volume create multivendor_redis_data || true
    print_success "Volumes verified"
}
fix_network() {
    print_section "STEP 5: FIXING NETWORK"
    docker network ls | grep -q "multivendor_network" || docker network create multivendor_network
    print_success "Network verified"
}
verify_compose_config() {
    print_section "STEP 6: VERIFYING CONFIG"
    [ -f ".env" ] && print_success ".env exists" || { print_error ".env not found!"; return 1; }
    docker-compose -f "$COMPOSE_FILE" config > /dev/null 2>&1 && print_success "Config valid" || { print_error "Config invalid!"; return 1; }
}
restart_services() {
    print_section "STEP 7: RESTARTING SERVICES"
    docker-compose -f "$COMPOSE_FILE" down || true
    sleep 2
    print_info "Starting database..."
    docker-compose -f "$COMPOSE_FILE" up -d db
    for i in {1..30}; do
        docker exec multivendor_db pg_isready -U postgres > /dev/null 2>&1 && { print_success "Database ready!"; break; }
        [ $i -eq 30 ] && { print_error "Database failed to start!"; return 1; }
        echo -n "."
        sleep 2
    done
    echo ""
    docker-compose -f "$COMPOSE_FILE" up -d redis && sleep 3
    docker-compose -f "$COMPOSE_FILE" up -d backend && sleep 10
    docker-compose -f "$COMPOSE_FILE" up -d nginx && sleep 3
    docker-compose -f "$COMPOSE_FILE" up -d frontend && sleep 3
    docker-compose -f "$COMPOSE_FILE" up -d traefik && sleep 3
    print_success "All services started"
}
verify_connections() {
    print_section "STEP 8: VERIFYING CONNECTIONS"
    sleep 5
    docker exec multivendor_backend python manage.py check --database default > /dev/null 2>&1 && print_success "Backend DB connection OK" || print_error "Backend DB connection FAILED"
    STATIC_COUNT=$(docker exec multivendor_backend ls -1 /app/static 2>/dev/null | wc -l || echo "0")
    [ "$STATIC_COUNT" -gt 0 ] && print_success "Backend static files: $STATIC_COUNT" || print_warning "No static files in backend"
    NGINX_STATIC_COUNT=$(docker exec multivendor_nginx ls -1 /usr/share/nginx/html/static 2>/dev/null | wc -l || echo "0")
    [ "$NGINX_STATIC_COUNT" -gt 0 ] && print_success "Nginx static files: $NGINX_STATIC_COUNT" || print_warning "No static files in nginx"
    MEDIA_COUNT=$(docker exec multivendor_backend ls -1 /app/media 2>/dev/null | wc -l || echo "0")
    [ "$MEDIA_COUNT" -gt 0 ] && print_success "Backend media files: $MEDIA_COUNT" || print_warning "No media files in backend"
    NGINX_MEDIA_COUNT=$(docker exec multivendor_nginx ls -1 /usr/share/nginx/html/media 2>/dev/null | wc -l || echo "0")
    [ "$NGINX_MEDIA_COUNT" -gt 0 ] && print_success "Nginx media files: $NGINX_MEDIA_COUNT" || print_warning "No media files in nginx"
}
recollect_static_files() {
    print_section "STEP 9: RECOLLECTING STATIC FILES"
    docker exec multivendor_backend python manage.py collectstatic --noinput --clear && print_success "Static files collected" || print_error "Failed to collect static files"
}
final_status_check() {
    print_section "STEP 10: FINAL STATUS"
    docker ps --filter "name=multivendor" --format "table {{.Names}}\t{{.Status}}"
    docker exec multivendor_backend ping -c 1 db > /dev/null 2>&1 && print_success "Backend can reach DB" || print_error "Backend cannot reach DB"
    docker exec multivendor_backend ping -c 1 redis > /dev/null 2>&1 && print_success "Backend can reach Redis" || print_error "Backend cannot reach Redis"
}
main() {
    clear
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   CRISIS RECOVERY SCRIPT - PRODUCTION DEPLOYMENT            ║${NC}"
    echo -e "${GREEN}║   VPS: 91.107.172.234                                     ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    read -p "Proceed with recovery? (y/n): " confirm
    confirm_lower=$(echo "$confirm" | tr '[:upper:]' '[:lower:]')
    [ "$confirm_lower" != "yes" ] && [ "$confirm_lower" != "y" ] && { print_info "Cancelled."; exit 0; }
    preflight_checks
    create_backup
    diagnose_issues
    fix_volumes
    fix_network
    verify_compose_config || exit 1
    restart_services
    verify_connections
    recollect_static_files
    final_status_check
    print_section "RECOVERY COMPLETE"
    print_success "Backup: $BACKUP_DIR"
}
main
SCRIPT_END
chmod +x crisis-recovery-production.sh && echo "Script created at /root/crisis-recovery-production.sh"
# END COPY HERE


#!/bin/bash
# ============================================================================
# CRISIS RECOVERY SCRIPT - PRODUCTION DEPLOYMENT
# ============================================================================
# This script helps recover from connection issues between:
# - Database ↔ Backend
# - Static Files ↔ Backend ↔ Nginx
# - Media Files ↔ Backend ↔ Nginx
#
# VPS: ssh root@91.107.172.234
# Usage: Copy and paste this entire script into your VPS terminal
# ============================================================================

set -e  # Exit on error (we'll handle errors manually in some sections)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.production.yml"
PROJECT_NAME="multivendor"
BACKUP_DIR="/root/crisis-backups-$(date +%Y%m%d-%H%M%S)"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_section() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ============================================================================
# STEP 1: PRE-FLIGHT CHECKS
# ============================================================================

preflight_checks() {
    print_section "STEP 1: PRE-FLIGHT CHECKS"
    
    # Try to find the project directory
    if [ ! -f "$COMPOSE_FILE" ] && [ ! -f "docker-compose.yml" ]; then
        print_info "Docker compose file not found in current directory. Searching..."
        
        # Common locations to search
        SEARCH_DIRS=(
            "/home/deploy/docker-deploy"
            "/root"
            "/root/indexo-production"
            "/root/mulitvendor_platform"
            "/opt/mulitvendor_platform"
            "/home"
            "$(pwd)"
        )
        
        FOUND_DIR=""
        for dir in "${SEARCH_DIRS[@]}"; do
            if [ -d "$dir" ]; then
                if [ -f "$dir/docker-compose.production.yml" ] || [ -f "$dir/docker-compose.yml" ]; then
                    FOUND_DIR="$dir"
                    break
                fi
            fi
        done
        
        # Also search in subdirectories
        if [ -z "$FOUND_DIR" ]; then
            for dir in "${SEARCH_DIRS[@]}"; do
                if [ -d "$dir" ]; then
                    FOUND_SUBDIR=$(find "$dir" -maxdepth 3 -name "docker-compose.production.yml" -o -name "docker-compose.yml" 2>/dev/null | head -1 | xargs dirname 2>/dev/null || echo "")
                    if [ -n "$FOUND_SUBDIR" ]; then
                        FOUND_DIR="$FOUND_SUBDIR"
                        break
                    fi
                fi
            done
        fi
        
        if [ -n "$FOUND_DIR" ]; then
            print_success "Found project directory: $FOUND_DIR"
            cd "$FOUND_DIR"
            if [ -f "docker-compose.production.yml" ]; then
                COMPOSE_FILE="docker-compose.production.yml"
            elif [ -f "docker-compose.yml" ]; then
                COMPOSE_FILE="docker-compose.yml"
            fi
        else
            print_error "Could not find docker-compose.production.yml or docker-compose.yml!"
            print_info "Current directory: $(pwd)"
            print_info "Please navigate to the project directory manually:"
            print_info "  cd /home/deploy/docker-deploy"
            print_info "Or run: find / -name 'docker-compose.production.yml' 2>/dev/null"
            exit 1
        fi
    elif [ -f "docker-compose.yml" ] && [ ! -f "$COMPOSE_FILE" ]; then
        COMPOSE_FILE="docker-compose.yml"
        print_info "Using docker-compose.yml instead"
    fi
    
    print_success "Found docker-compose file: $COMPOSE_FILE"
    print_info "Working directory: $(pwd)"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed!"
        exit 1
    fi
    print_success "Docker is installed"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed!"
        exit 1
    fi
    print_success "Docker Compose is available"
    
    # Check if containers exist
    print_info "Checking existing containers..."
    docker ps -a --filter "name=multivendor" --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" || true
    echo ""
}

# ============================================================================
# STEP 2: CREATE BACKUP
# ============================================================================

create_backup() {
    print_section "STEP 2: CREATING BACKUP"
    
    mkdir -p "$BACKUP_DIR"
    print_info "Backup directory: $BACKUP_DIR"
    
    # Backup database
    print_info "Backing up database..."
    if docker exec multivendor_db pg_dump -U postgres multivendor_db > "$BACKUP_DIR/database.sql" 2>/dev/null; then
        print_success "Database backup created: $BACKUP_DIR/database.sql"
        DB_SIZE=$(du -h "$BACKUP_DIR/database.sql" | cut -f1)
        print_info "Database backup size: $DB_SIZE"
    else
        print_warning "Could not backup database (container might be stopped or database name different)"
        print_info "Trying to find correct database name..."
        # Try to list databases
        docker exec multivendor_db psql -U postgres -l 2>/dev/null || true
    fi
    
    # Backup volume information
    print_info "Backing up volume information..."
    docker volume ls > "$BACKUP_DIR/volumes-list.txt" 2>/dev/null || true
    docker inspect multivendor_db > "$BACKUP_DIR/db-container-info.json" 2>/dev/null || true
    docker inspect multivendor_backend > "$BACKUP_DIR/backend-container-info.json" 2>/dev/null || true
    docker inspect multivendor_nginx > "$BACKUP_DIR/nginx-container-info.json" 2>/dev/null || true
    
    # Backup static files (if accessible)
    print_info "Backing up static files metadata..."
    if docker exec multivendor_backend ls -la /app/static > "$BACKUP_DIR/static-files-list.txt" 2>/dev/null; then
        print_success "Static files list backed up"
    else
        print_warning "Could not list static files"
    fi
    
    # Backup media files metadata
    print_info "Backing up media files metadata..."
    if docker exec multivendor_backend ls -la /app/media > "$BACKUP_DIR/media-files-list.txt" 2>/dev/null; then
        print_success "Media files list backed up"
    else
        print_warning "Could not list media files"
    fi
    
    print_success "Backup completed: $BACKUP_DIR"
    echo ""
}

# ============================================================================
# STEP 3: DIAGNOSE ISSUES
# ============================================================================

diagnose_issues() {
    print_section "STEP 3: DIAGNOSING ISSUES"
    
    # Check volumes
    print_info "Checking Docker volumes..."
    echo ""
    echo "Required volumes:"
    echo "  - postgres_data (or multivendor_postgres_data)"
    echo "  - static_files (or multivendor_static_files)"
    echo "  - media_files (or multivendor_media_files)"
    echo "  - redis_data (or multivendor_redis_data)"
    echo ""
    
    VOLUMES=$(docker volume ls --format "{{.Name}}" | grep -E "(postgres_data|static_files|media_files|redis_data|multivendor)" || true)
    if [ -z "$VOLUMES" ]; then
        print_error "No production volumes found!"
    else
        print_success "Found volumes:"
        echo "$VOLUMES" | while read vol; do
            VOL_SIZE=$(docker volume inspect "$vol" --format '{{.Mountpoint}}' 2>/dev/null | xargs du -sh 2>/dev/null | cut -f1 || echo "unknown")
            echo "  - $vol (size: $VOL_SIZE)"
        done
    fi
    echo ""
    
    # Check network
    print_info "Checking Docker network..."
    if docker network ls | grep -q "multivendor_network"; then
        print_success "Network 'multivendor_network' exists"
        # Check which containers are on the network
        NETWORK_CONTAINERS=$(docker network inspect multivendor_network --format '{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null || echo "")
        if [ -n "$NETWORK_CONTAINERS" ]; then
            print_info "Containers on network: $NETWORK_CONTAINERS"
        else
            print_warning "No containers connected to network"
        fi
    else
        print_error "Network 'multivendor_network' NOT found!"
    fi
    echo ""
    
    # Check database container
    print_info "Checking database container..."
    if docker ps -a --format "{{.Names}}" | grep -q "^multivendor_db$"; then
        DB_STATUS=$(docker inspect multivendor_db --format '{{.State.Status}}' 2>/dev/null || echo "not-found")
        if [ "$DB_STATUS" = "running" ]; then
            print_success "Database container is running"
            
            # Test database connection
            print_info "Testing database connection..."
            if docker exec multivendor_db pg_isready -U postgres > /dev/null 2>&1; then
                print_success "Database is accepting connections"
                
                # Check database size
                print_info "Checking database size..."
                DB_SIZE=$(docker exec multivendor_db psql -U postgres -t -c "SELECT pg_size_pretty(pg_database_size(current_database()));" 2>/dev/null | xargs || echo "unknown")
                print_info "Database size: $DB_SIZE"
                
                # Check table count
                TABLE_COUNT=$(docker exec multivendor_db psql -U postgres -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs || echo "unknown")
                print_info "Tables in database: $TABLE_COUNT"
            else
                print_error "Database is NOT accepting connections!"
            fi
        else
            print_error "Database container status: $DB_STATUS"
        fi
    else
        print_error "Database container 'multivendor_db' NOT found!"
    fi
    echo ""
    
    # Check backend container
    print_info "Checking backend container..."
    if docker ps -a --format "{{.Names}}" | grep -q "^multivendor_backend$"; then
        BACKEND_STATUS=$(docker inspect multivendor_backend --format '{{.State.Status}}' 2>/dev/null || echo "not-found")
        if [ "$BACKEND_STATUS" = "running" ]; then
            print_success "Backend container is running"
            
            # Check backend logs for errors
            print_info "Checking recent backend logs for errors..."
            ERROR_COUNT=$(docker logs multivendor_backend --tail 50 2>&1 | grep -i "error\|fail\|exception\|traceback" | wc -l || echo "0")
            if [ "$ERROR_COUNT" -gt 0 ]; then
                print_warning "Found $ERROR_COUNT potential errors in recent logs"
                docker logs multivendor_backend --tail 20 2>&1 | grep -i "error\|fail\|exception" | head -5 || true
            else
                print_success "No obvious errors in recent logs"
            fi
        else
            print_error "Backend container status: $BACKEND_STATUS"
        fi
    else
        print_error "Backend container 'multivendor_backend' NOT found!"
    fi
    echo ""
    
    # Check nginx container
    print_info "Checking nginx container..."
    if docker ps -a --format "{{.Names}}" | grep -q "^multivendor_nginx$"; then
        NGINX_STATUS=$(docker inspect multivendor_nginx --format '{{.State.Status}}' 2>/dev/null || echo "not-found")
        if [ "$NGINX_STATUS" = "running" ]; then
            print_success "Nginx container is running"
        else
            print_error "Nginx container status: $NGINX_STATUS"
        fi
    else
        print_error "Nginx container 'multivendor_nginx' NOT found!"
    fi
    echo ""
    
    # Check volume mounts
    print_info "Checking volume mounts..."
    
    # Check backend static files mount
    BACKEND_STATIC_MOUNT=$(docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/static"}}{{.Source}}{{end}}{{end}}' 2>/dev/null || echo "")
    if [ -n "$BACKEND_STATIC_MOUNT" ]; then
        print_success "Backend has static files mounted from: $BACKEND_STATIC_MOUNT"
        # Check if files exist
        STATIC_COUNT=$(docker exec multivendor_backend ls -1 /app/static 2>/dev/null | wc -l || echo "0")
        if [ "$STATIC_COUNT" -gt 0 ]; then
            print_success "  → Found $STATIC_COUNT items in /app/static"
        else
            print_warning "  → Directory exists but is empty"
        fi
    else
        print_error "Backend is NOT mounting static files!"
    fi
    
    # Check backend media files mount
    BACKEND_MEDIA_MOUNT=$(docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/media"}}{{.Source}}{{end}}{{end}}' 2>/dev/null || echo "")
    if [ -n "$BACKEND_MEDIA_MOUNT" ]; then
        print_success "Backend has media files mounted from: $BACKEND_MEDIA_MOUNT"
        # Check if files exist
        MEDIA_COUNT=$(docker exec multivendor_backend ls -1 /app/media 2>/dev/null | wc -l || echo "0")
        if [ "$MEDIA_COUNT" -gt 0 ]; then
            print_success "  → Found $MEDIA_COUNT items in /app/media"
        else
            print_warning "  → Directory exists but is empty"
        fi
    else
        print_error "Backend is NOT mounting media files!"
    fi
    
    # Check nginx static files mount
    NGINX_STATIC_MOUNT=$(docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/static"}}{{.Source}}{{end}}{{end}}' 2>/dev/null || echo "")
    if [ -n "$NGINX_STATIC_MOUNT" ]; then
        print_success "Nginx has static files mounted from: $NGINX_STATIC_MOUNT"
        # Check if it's the same volume as backend
        if [ "$BACKEND_STATIC_MOUNT" = "$NGINX_STATIC_MOUNT" ]; then
            print_success "  → Same volume as backend (correct!)"
        else
            print_error "  → Different volume than backend (MISMATCH!)"
        fi
    else
        print_error "Nginx is NOT mounting static files!"
    fi
    
    # Check nginx media files mount
    NGINX_MEDIA_MOUNT=$(docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/media"}}{{.Source}}{{end}}{{end}}' 2>/dev/null || echo "")
    if [ -n "$NGINX_MEDIA_MOUNT" ]; then
        print_success "Nginx has media files mounted from: $NGINX_MEDIA_MOUNT"
        # Check if it's the same volume as backend
        if [ "$BACKEND_MEDIA_MOUNT" = "$NGINX_MEDIA_MOUNT" ]; then
            print_success "  → Same volume as backend (correct!)"
        else
            print_error "  → Different volume than backend (MISMATCH!)"
        fi
    else
        print_error "Nginx is NOT mounting media files!"
    fi
    echo ""
}

# ============================================================================
# STEP 4: FIX VOLUMES
# ============================================================================

fix_volumes() {
    print_section "STEP 4: FIXING VOLUMES"
    
    # Ensure volumes exist
    print_info "Ensuring volumes exist..."
    
    # Check and create postgres volume
    POSTGRES_VOL=$(docker volume ls --format "{{.Name}}" | grep -E "^postgres_data$|^multivendor.*postgres" | head -1 || echo "")
    if [ -z "$POSTGRES_VOL" ]; then
        print_warning "PostgreSQL volume not found. Creating..."
        docker volume create postgres_data || \
        docker volume create multivendor_postgres_data || true
        print_success "Created PostgreSQL volume"
    else
        print_success "PostgreSQL volume exists: $POSTGRES_VOL"
    fi
    
    # Check and create static files volume
    STATIC_VOL=$(docker volume ls --format "{{.Name}}" | grep -E "^static_files$|^multivendor.*static" | head -1 || echo "")
    if [ -z "$STATIC_VOL" ]; then
        print_warning "Static files volume not found. Creating..."
        docker volume create static_files || \
        docker volume create multivendor_static_files || true
        print_success "Created static files volume"
    else
        print_success "Static files volume exists: $STATIC_VOL"
    fi
    
    # Check and create media files volume
    MEDIA_VOL=$(docker volume ls --format "{{.Name}}" | grep -E "^media_files$|^multivendor.*media" | head -1 || echo "")
    if [ -z "$MEDIA_VOL" ]; then
        print_warning "Media files volume not found. Creating..."
        docker volume create media_files || \
        docker volume create multivendor_media_files || true
        print_success "Created media files volume"
    else
        print_success "Media files volume exists: $MEDIA_VOL"
    fi
    
    # Check and create redis volume
    REDIS_VOL=$(docker volume ls --format "{{.Name}}" | grep -E "^redis_data$|^multivendor.*redis" | head -1 || echo "")
    if [ -z "$REDIS_VOL" ]; then
        print_warning "Redis volume not found. Creating..."
        docker volume create redis_data || \
        docker volume create multivendor_redis_data || true
        print_success "Created redis volume"
    else
        print_success "Redis volume exists: $REDIS_VOL"
    fi
    
    echo ""
}

# ============================================================================
# STEP 5: FIX NETWORK
# ============================================================================

fix_network() {
    print_section "STEP 5: FIXING NETWORK"
    
    # Ensure network exists
    if ! docker network ls | grep -q "multivendor_network"; then
        print_warning "Network 'multivendor_network' not found. Creating..."
        docker network create multivendor_network
        print_success "Created multivendor_network"
    else
        print_success "Network 'multivendor_network' exists"
    fi
    echo ""
}

# ============================================================================
# STEP 6: VERIFY DOCKER COMPOSE CONFIGURATION
# ============================================================================

verify_compose_config() {
    print_section "STEP 6: VERIFYING DOCKER COMPOSE CONFIGURATION"
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        print_error ".env file not found!"
        print_info "Please ensure .env exists with required variables:"
        print_info "  - DB_NAME"
        print_info "  - DB_USER"
        print_info "  - DB_PASSWORD"
        print_info "  - DB_HOST (should be 'db' for production)"
        print_info "  - DB_PORT"
        print_info "  - SECRET_KEY"
        print_info "  - ALLOWED_HOSTS"
        print_info "  - API_DOMAIN"
        print_info "  - MAIN_DOMAIN"
        return 1
    else
        print_success ".env file exists"
    fi
    
    # Validate docker-compose file
    print_info "Validating docker-compose configuration..."
    if docker-compose -f "$COMPOSE_FILE" config > /dev/null 2>&1; then
        print_success "Docker Compose configuration is valid"
    else
        print_error "Docker Compose configuration has errors!"
        docker-compose -f "$COMPOSE_FILE" config
        return 1
    fi
    echo ""
}

# ============================================================================
# STEP 7: RESTART SERVICES (SAFE ORDER)
# ============================================================================

restart_services() {
    print_section "STEP 7: RESTARTING SERVICES (SAFE ORDER)"
    
    print_info "Stopping all production services..."
    docker-compose -f "$COMPOSE_FILE" down || true
    sleep 2
    
    print_info "Starting services in correct order..."
    echo ""
    
    # 1. Start database first
    print_info "[1/6] Starting database..."
    docker-compose -f "$COMPOSE_FILE" up -d db
    print_info "Waiting for database to be ready..."
    
    max_retries=30
    retry_count=0
    while [ $retry_count -lt $max_retries ]; do
        if docker exec multivendor_db pg_isready -U postgres > /dev/null 2>&1; then
            print_success "Database is ready!"
            break
        fi
        retry_count=$((retry_count + 1))
        echo -n "."
        sleep 2
    done
    echo ""
    
    if [ $retry_count -eq $max_retries ]; then
        print_error "Database failed to start!"
        return 1
    fi
    
    # 2. Start Redis
    print_info "[2/6] Starting Redis..."
    docker-compose -f "$COMPOSE_FILE" up -d redis
    sleep 3
    print_success "Redis started"
    
    # 3. Start backend
    print_info "[3/6] Starting backend..."
    docker-compose -f "$COMPOSE_FILE" up -d backend
    print_info "Waiting for backend to initialize..."
    sleep 10
    
    # Check backend logs
    print_info "Checking backend logs..."
    docker logs multivendor_backend --tail 30
    
    # 4. Start nginx
    print_info "[4/6] Starting nginx..."
    docker-compose -f "$COMPOSE_FILE" up -d nginx
    sleep 3
    print_success "Nginx started"
    
    # 5. Start frontend
    print_info "[5/6] Starting frontend..."
    docker-compose -f "$COMPOSE_FILE" up -d frontend
    sleep 3
    print_success "Frontend started"
    
    # 6. Start traefik
    print_info "[6/6] Starting traefik..."
    docker-compose -f "$COMPOSE_FILE" up -d traefik
    sleep 3
    print_success "Traefik started"
    
    echo ""
}

# ============================================================================
# STEP 8: VERIFY CONNECTIONS
# ============================================================================

verify_connections() {
    print_section "STEP 8: VERIFYING CONNECTIONS"
    
    # Wait a bit for services to stabilize
    sleep 5
    
    # Test database connection from backend
    print_info "Testing database connection from backend..."
    if docker exec multivendor_backend python manage.py check --database default > /dev/null 2>&1; then
        print_success "Backend can connect to database!"
        
        # Get database info
        print_info "Database connection details:"
        docker exec multivendor_backend python manage.py dbshell -c "\conninfo" 2>/dev/null || true
    else
        print_error "Backend CANNOT connect to database!"
        print_info "Backend logs:"
        docker logs multivendor_backend --tail 20
    fi
    echo ""
    
    # Check static files
    print_info "Checking static files..."
    STATIC_COUNT=$(docker exec multivendor_backend ls -1 /app/static 2>/dev/null | wc -l || echo "0")
    if [ "$STATIC_COUNT" -gt 0 ]; then
        print_success "Static files found in backend: $STATIC_COUNT files"
        # Show some examples
        print_info "Sample static files:"
        docker exec multivendor_backend ls -1 /app/static | head -5 | while read file; do
            echo "  - $file"
        done
    else
        print_warning "No static files in backend. They will be collected on next startup."
    fi
    
    NGINX_STATIC_COUNT=$(docker exec multivendor_nginx ls -1 /usr/share/nginx/html/static 2>/dev/null | wc -l || echo "0")
    if [ "$NGINX_STATIC_COUNT" -gt 0 ]; then
        print_success "Static files found in nginx: $NGINX_STATIC_COUNT files"
    else
        print_warning "No static files in nginx"
    fi
    
    # Verify volume connection
    BACKEND_STATIC_VOL=$(docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/static"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")
    NGINX_STATIC_VOL=$(docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/static"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")
    if [ "$BACKEND_STATIC_VOL" = "$NGINX_STATIC_VOL" ] && [ -n "$BACKEND_STATIC_VOL" ]; then
        print_success "Backend and Nginx share the same static files volume: $BACKEND_STATIC_VOL"
    else
        print_error "Volume mismatch! Backend: $BACKEND_STATIC_VOL, Nginx: $NGINX_STATIC_VOL"
    fi
    echo ""
    
    # Check media files
    print_info "Checking media files..."
    MEDIA_COUNT=$(docker exec multivendor_backend ls -1 /app/media 2>/dev/null | wc -l || echo "0")
    if [ "$MEDIA_COUNT" -gt 0 ]; then
        print_success "Media files found in backend: $MEDIA_COUNT items"
        # Show directory structure
        print_info "Media directory structure:"
        docker exec multivendor_backend find /app/media -maxdepth 2 -type d 2>/dev/null | head -10 | while read dir; do
            echo "  - $dir"
        done
    else
        print_warning "No media files in backend (this might be normal for new deployments)"
    fi
    
    NGINX_MEDIA_COUNT=$(docker exec multivendor_nginx ls -1 /usr/share/nginx/html/media 2>/dev/null | wc -l || echo "0")
    if [ "$NGINX_MEDIA_COUNT" -gt 0 ]; then
        print_success "Media files found in nginx: $NGINX_MEDIA_COUNT items"
    else
        print_warning "No media files in nginx"
    fi
    
    # Verify media volume connection
    BACKEND_MEDIA_VOL=$(docker inspect multivendor_backend --format '{{range .Mounts}}{{if eq .Destination "/app/media"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")
    NGINX_MEDIA_VOL=$(docker inspect multivendor_nginx --format '{{range .Mounts}}{{if eq .Destination "/usr/share/nginx/html/media"}}{{.Name}}{{end}}{{end}}' 2>/dev/null || echo "")
    if [ "$BACKEND_MEDIA_VOL" = "$NGINX_MEDIA_VOL" ] && [ -n "$BACKEND_MEDIA_VOL" ]; then
        print_success "Backend and Nginx share the same media files volume: $BACKEND_MEDIA_VOL"
    else
        print_error "Volume mismatch! Backend: $BACKEND_MEDIA_VOL, Nginx: $NGINX_MEDIA_VOL"
    fi
    echo ""
    
    # Check container health
    print_info "Checking container health status..."
    docker ps --filter "name=multivendor" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
}

# ============================================================================
# STEP 9: RECOLLECT STATIC FILES (IF NEEDED)
# ============================================================================

recollect_static_files() {
    print_section "STEP 9: RECOLLECTING STATIC FILES"
    
    print_info "Running collectstatic in backend container..."
    if docker exec multivendor_backend python manage.py collectstatic --noinput --clear; then
        print_success "Static files collected successfully!"
        
        # Verify files were collected
        STATIC_COUNT=$(docker exec multivendor_backend ls -1 /app/static 2>/dev/null | wc -l || echo "0")
        print_info "Static files count after collection: $STATIC_COUNT"
        
        # Check if nginx can see them
        NGINX_STATIC_COUNT=$(docker exec multivendor_nginx ls -1 /usr/share/nginx/html/static 2>/dev/null | wc -l || echo "0")
        if [ "$NGINX_STATIC_COUNT" -gt 0 ]; then
            print_success "Nginx can see $NGINX_STATIC_COUNT static files"
        else
            print_warning "Nginx cannot see static files (volume might not be shared)"
        fi
    else
        print_error "Failed to collect static files!"
        print_info "This might be due to:"
        print_info "  - Database connection issues"
        print_info "  - Missing dependencies"
        print_info "  - Permission issues"
        print_info "Backend logs:"
        docker logs multivendor_backend --tail 20
    fi
    echo ""
}

# ============================================================================
# STEP 10: FINAL STATUS CHECK
# ============================================================================

final_status_check() {
    print_section "STEP 10: FINAL STATUS CHECK"
    
    print_info "Container Status:"
    docker ps --filter "name=multivendor" --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"
    echo ""
    
    print_info "Volume Mounts Summary:"
    echo "Backend mounts:"
    docker inspect multivendor_backend --format '{{range .Mounts}}{{.Type}} {{.Name}} -> {{.Destination}}
{{end}}' 2>/dev/null | grep -E "(static|media)" || true
    echo ""
    echo "Nginx mounts:"
    docker inspect multivendor_nginx --format '{{range .Mounts}}{{.Type}} {{.Name}} -> {{.Destination}}
{{end}}' 2>/dev/null | grep -E "(static|media)" || true
    echo ""
    
    print_info "Network Connectivity:"
    if docker exec multivendor_backend ping -c 1 db > /dev/null 2>&1; then
        print_success "Backend can reach database service (db)"
    else
        print_error "Backend cannot reach database service!"
    fi
    
    if docker exec multivendor_backend ping -c 1 redis > /dev/null 2>&1; then
        print_success "Backend can reach Redis"
    else
        print_error "Backend cannot reach Redis!"
    fi
    echo ""
    
    print_info "Database Statistics:"
    if docker exec multivendor_db pg_isready -U postgres > /dev/null 2>&1; then
        DB_SIZE=$(docker exec multivendor_db psql -U postgres -t -c "SELECT pg_size_pretty(pg_database_size(current_database()));" 2>/dev/null | xargs || echo "unknown")
        TABLE_COUNT=$(docker exec multivendor_db psql -U postgres -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs || echo "unknown")
        print_info "  Database size: $DB_SIZE"
        print_info "  Tables: $TABLE_COUNT"
    fi
    echo ""
    
    print_info "Recent Backend Logs (last 10 lines):"
    docker logs multivendor_backend --tail 10 2>&1 | tail -10
    echo ""
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    clear
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   CRISIS RECOVERY SCRIPT - PRODUCTION DEPLOYMENT            ║${NC}"
    echo -e "${GREEN}║   VPS: 91.107.172.234                                     ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Ask for confirmation
    read -p "Do you want to proceed with crisis recovery? (yes/no): " confirm
    confirm_lower=$(echo "$confirm" | tr '[:upper:]' '[:lower:]')
    if [ "$confirm_lower" != "yes" ] && [ "$confirm_lower" != "y" ]; then
        print_info "Recovery cancelled."
        exit 0
    fi
    
    # Run all steps
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
    print_success "All recovery steps completed!"
    print_info "Backup location: $BACKUP_DIR"
    print_info ""
    print_info "Next steps:"
    print_info "  1. Check application logs: docker logs multivendor_backend"
    print_info "  2. Test API endpoint: curl https://your-api-domain/api/"
    print_info "  3. Check static files: curl https://your-api-domain/static/admin/css/base.css"
    print_info "  4. Monitor containers: docker ps"
    print_info "  5. Check database: docker exec multivendor_db psql -U postgres -c '\\dt'"
    echo ""
}

# Run main function
main


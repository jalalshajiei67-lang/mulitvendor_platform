#!/bin/bash
# ============================================================================
# Production Recovery Script - Restore from Backup
# ============================================================================
# This script helps recover production by:
# 1. Finding and listing available backups
# 2. Restoring database from selected backup
# 3. Optionally rolling back to a previous Git commit
# 4. Restarting services and verifying
# ============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
DEPLOY_DIR="/home/deploy/docker-deploy"
COMPOSE_FILE="docker-compose.production.yml"
DB_NAME="${DB_NAME:-multivendor_db}"
DB_USER="${DB_USER:-postgres}"

# Backup locations to search
BACKUP_LOCATIONS=(
    "/root/crisis-backups-*"
    "/home/deploy/docker-deploy/database_backups"
    "/opt/multivendor_platform/backups"
    "/root/database_backups"
    "/root/backup-*"
    "."
)

print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Production Recovery Script                              ║${NC}"
    echo -e "${BLUE}║   VPS: 91.107.172.234                                    ║${NC}"
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

# Check prerequisites
check_prerequisites() {
    print_section "STEP 1: CHECKING PREREQUISITES"
    
    # Check if we're in the right directory
    if [ ! -d "$DEPLOY_DIR" ]; then
        print_error "Deployment directory not found: $DEPLOY_DIR"
        print_info "Current directory: $(pwd)"
        read -p "Continue from current directory? (y/n): " continue_here
        if [ "$continue_here" != "y" ] && [ "$continue_here" != "Y" ]; then
            exit 1
        fi
        DEPLOY_DIR="$(pwd)"
    fi
    
    cd "$DEPLOY_DIR" || exit 1
    print_success "Working directory: $DEPLOY_DIR"
    
    # Check docker-compose file
    if [ ! -f "$COMPOSE_FILE" ] && [ ! -f "docker-compose.yml" ]; then
        print_error "Docker compose file not found!"
        exit 1
    fi
    
    [ -f "docker-compose.yml" ] && COMPOSE_FILE="docker-compose.yml"
    print_success "Using compose file: $COMPOSE_FILE"
    
    # Check Docker
    command -v docker > /dev/null || { print_error "Docker not installed!"; exit 1; }
    print_success "Docker is installed"
    
    # Check if containers are running
    if ! docker ps --filter "name=multivendor_db" --format "{{.Names}}" | grep -q multivendor_db; then
        print_warning "Database container is not running. Starting it..."
        docker compose -f "$COMPOSE_FILE" up -d db || true
        print_info "Waiting for database to be ready..."
        sleep 10
    fi
    print_success "Database container is running"
}

# Find all available backups
find_backups() {
    print_section "STEP 2: FINDING AVAILABLE BACKUPS"
    
    BACKUP_FILES=()
    
    # Search in all backup locations
    for location_pattern in "${BACKUP_LOCATIONS[@]}"; do
        # Handle wildcards
        for location in $location_pattern; do
            if [ -d "$location" ]; then
                # Find SQL files in this directory
                while IFS= read -r -d '' file; do
                    BACKUP_FILES+=("$file")
                done < <(find "$location" -type f \( -name "*.sql" -o -name "*.sql.gz" -o -name "database.sql" \) -print0 2>/dev/null)
            elif [ -f "$location" ] && [[ "$location" == *.sql* ]]; then
                BACKUP_FILES+=("$location")
            fi
        done
    done
    
    # Also check crisis-backups directories specifically
    for crisis_dir in /root/crisis-backups-*; do
        if [ -d "$crisis_dir" ]; then
            if [ -f "$crisis_dir/database.sql" ]; then
                BACKUP_FILES+=("$crisis_dir/database.sql")
            fi
        fi
    done
    
    # Remove duplicates and sort by modification time (newest first)
    if [ ${#BACKUP_FILES[@]} -eq 0 ]; then
        print_error "No backup files found!"
        print_info "Searched in:"
        for loc in "${BACKUP_LOCATIONS[@]}"; do
            echo "  - $loc"
        done
        read -p "Enter backup file path manually: " manual_backup
        if [ -f "$manual_backup" ]; then
            BACKUP_FILES=("$manual_backup")
        else
            print_error "Backup file not found: $manual_backup"
            exit 1
        fi
    else
        # Remove duplicates
        BACKUP_FILES=($(printf '%s\n' "${BACKUP_FILES[@]}" | sort -u))
        # Sort by modification time (newest first)
        BACKUP_FILES=($(printf '%s\n' "${BACKUP_FILES[@]}" | xargs -I {} sh -c 'echo "$(stat -c %Y "{}") {}"' | sort -rn | cut -d' ' -f2-))
    fi
    
    print_success "Found ${#BACKUP_FILES[@]} backup file(s)"
    echo ""
    echo -e "${YELLOW}Available backups:${NC}"
    echo ""
    for i in "${!BACKUP_FILES[@]}"; do
        file="${BACKUP_FILES[$i]}"
        size=$(du -h "$file" 2>/dev/null | cut -f1)
        date=$(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        echo -e "  ${GREEN}[$((i+1))]${NC} $(basename "$file")"
        echo -e "      Path: $file"
        echo -e "      Size: $size | Date: $date"
        echo ""
    done
}

# Select backup
select_backup() {
    print_section "STEP 3: SELECTING BACKUP"
    
    if [ ${#BACKUP_FILES[@]} -eq 1 ]; then
        SELECTED_BACKUP="${BACKUP_FILES[0]}"
        print_info "Only one backup found, using: $SELECTED_BACKUP"
    else
        read -p "Enter backup number (1-${#BACKUP_FILES[@]}) or 'latest' for most recent: " selection
        
        if [ "$selection" == "latest" ]; then
            SELECTED_BACKUP="${BACKUP_FILES[0]}"
        elif [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le ${#BACKUP_FILES[@]} ]; then
            SELECTED_BACKUP="${BACKUP_FILES[$((selection-1))]}"
        else
            print_error "Invalid selection: $selection"
            exit 1
        fi
    fi
    
    if [ ! -f "$SELECTED_BACKUP" ]; then
        print_error "Backup file not found: $SELECTED_BACKUP"
        exit 1
    fi
    
    print_success "Selected backup: $SELECTED_BACKUP"
    BACKUP_SIZE=$(du -h "$SELECTED_BACKUP" | cut -f1)
    print_info "Backup size: $BACKUP_SIZE"
    
    echo ""
    echo -e "${RED}⚠️  WARNING: This will overwrite the current database!${NC}"
    read -p "Are you sure you want to continue? (type 'yes' to confirm): " CONFIRM
    
    if [ "$CONFIRM" != "yes" ]; then
        print_warning "Recovery cancelled"
        exit 0
    fi
}

# Create safety backup
create_safety_backup() {
    print_section "STEP 4: CREATING SAFETY BACKUP"
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SAFETY_BACKUP_DIR="/root/safety-backup-before-restore-${TIMESTAMP}"
    mkdir -p "$SAFETY_BACKUP_DIR"
    
    print_info "Backing up current database..."
    if docker exec multivendor_db psql -U postgres -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        CURRENT_BACKUP="$SAFETY_BACKUP_DIR/database_before_restore.sql"
        if docker exec multivendor_db pg_dump -U postgres "$DB_NAME" > "$CURRENT_BACKUP" 2>/dev/null; then
            print_success "Current database backed up to: $CURRENT_BACKUP"
            DB_SIZE=$(du -h "$CURRENT_BACKUP" | cut -f1)
            print_info "Backup size: $DB_SIZE"
        else
            print_warning "Could not backup current database (may be empty or corrupted)"
        fi
    else
        print_warning "Database '$DB_NAME' doesn't exist yet"
    fi
    
    # Backup current Git commit
    if [ -d ".git" ]; then
        CURRENT_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
        echo "$CURRENT_COMMIT" > "$SAFETY_BACKUP_DIR/current_commit.txt"
        git log --oneline -10 > "$SAFETY_BACKUP_DIR/git_log.txt" 2>/dev/null || true
        print_success "Git state backed up"
    fi
    
    print_success "Safety backup created: $SAFETY_BACKUP_DIR"
}

# Restore database
restore_database() {
    print_section "STEP 5: RESTORING DATABASE"
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    RESTORE_FILE="/tmp/restore_${TIMESTAMP}.sql"
    
    # Prepare backup file (decompress if needed)
    print_info "Preparing backup file..."
    if [[ "$SELECTED_BACKUP" == *.gz ]]; then
        print_info "Decompressing backup..."
        gunzip -c "$SELECTED_BACKUP" > "$RESTORE_FILE"
    else
        print_info "Copying backup file..."
        cp "$SELECTED_BACKUP" "$RESTORE_FILE"
    fi
    
    # Drop and recreate database
    print_info "Dropping existing database (if exists)..."
    docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS ${DB_NAME};" 2>/dev/null || true
    
    print_info "Creating new database..."
    docker exec multivendor_db psql -U postgres -c "CREATE DATABASE ${DB_NAME};" || {
        print_error "Failed to create database"
        rm -f "$RESTORE_FILE"
        exit 1
    }
    
    # Restore database
    print_info "Restoring database (this may take a while)..."
    if cat "$RESTORE_FILE" | docker exec -i multivendor_db psql -U postgres -d ${DB_NAME} > /tmp/restore_log.txt 2>&1; then
        print_success "Database restored successfully!"
        rm -f "$RESTORE_FILE"
    else
        print_error "Database restore failed!"
        print_info "Check /tmp/restore_log.txt for details"
        rm -f "$RESTORE_FILE"
        exit 1
    fi
}

# Optional: Rollback Git commit
rollback_git() {
    print_section "STEP 6: GIT ROLLBACK (OPTIONAL)"
    
    if [ ! -d ".git" ]; then
        print_warning "Not a Git repository, skipping Git rollback"
        return
    fi
    
    print_info "Current commit: $(git rev-parse HEAD 2>/dev/null || echo 'unknown')"
    echo ""
    read -p "Do you want to rollback to a previous Git commit? (y/n): " rollback_choice
    
    if [ "$rollback_choice" != "y" ] && [ "$rollback_choice" != "Y" ]; then
        print_info "Skipping Git rollback"
        return
    fi
    
    echo ""
    print_info "Recent commits:"
    git log --oneline -15
    
    echo ""
    read -p "Enter commit hash to rollback to (or 'skip' to continue): " commit_hash
    
    if [ "$commit_hash" == "skip" ] || [ -z "$commit_hash" ]; then
        print_info "Skipping Git rollback"
        return
    fi
    
    # Verify commit exists
    if ! git cat-file -e "$commit_hash^{commit}" 2>/dev/null; then
        print_error "Commit not found: $commit_hash"
        return
    fi
    
    print_warning "Rolling back to commit: $commit_hash"
    print_warning "This will reset your working directory!"
    read -p "Are you sure? (type 'yes' to confirm): " confirm_rollback
    
    if [ "$confirm_rollback" == "yes" ]; then
        git fetch --all || true
        git reset --hard "$commit_hash" || {
            print_error "Git rollback failed!"
            return
        }
        print_success "Rolled back to commit: $commit_hash"
        print_info "You may need to rebuild containers after rollback"
    else
        print_info "Git rollback cancelled"
    fi
}

# Restart services
restart_services() {
    print_section "STEP 7: RESTARTING SERVICES"
    
    print_info "Restarting backend service..."
    docker compose -f "$COMPOSE_FILE" restart backend || docker restart multivendor_backend || {
        print_warning "Could not restart backend, trying to start it..."
        docker compose -f "$COMPOSE_FILE" up -d backend || true
    }
    
    print_info "Waiting for backend to be ready..."
    sleep 10
    
    print_success "Services restarted"
}

# Verify recovery
verify_recovery() {
    print_section "STEP 8: VERIFYING RECOVERY"
    
    # Check database connection
    print_info "Checking database connection..."
    if docker exec multivendor_backend python manage.py check --database default > /dev/null 2>&1; then
        print_success "Backend can connect to database"
    else
        print_error "Backend cannot connect to database!"
        print_info "Check logs: docker logs multivendor_backend --tail 50"
    fi
    
    # Check if database has data
    print_info "Checking database tables..."
    TABLE_COUNT=$(docker exec multivendor_db psql -U postgres -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")
    if [ "$TABLE_COUNT" -gt 0 ]; then
        print_success "Database has $TABLE_COUNT table(s)"
    else
        print_warning "Database appears to be empty"
    fi
    
    # Check backend health
    print_info "Checking backend health..."
    HEALTH_STATUS=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' multivendor_backend 2>/dev/null || echo "unknown")
    if [ "$HEALTH_STATUS" == "healthy" ] || [ "$HEALTH_STATUS" == "running" ]; then
        print_success "Backend is $HEALTH_STATUS"
    else
        print_warning "Backend status: $HEALTH_STATUS"
    fi
    
    # Check container status
    echo ""
    print_info "Container status:"
    docker ps --filter "name=multivendor" --format "table {{.Names}}\t{{.Status}}"
}

# Main function
main() {
    clear
    print_header
    
    print_warning "This script will restore your production database from backup"
    print_warning "Make sure you have SSH access to the VPS and backups are available"
    echo ""
    read -p "Continue with recovery? (y/n): " start_recovery
    
    if [ "$start_recovery" != "y" ] && [ "$start_recovery" != "Y" ]; then
        print_info "Recovery cancelled"
        exit 0
    fi
    
    check_prerequisites
    find_backups
    select_backup
    create_safety_backup
    restore_database
    rollback_git
    restart_services
    verify_recovery
    
    print_section "RECOVERY COMPLETE"
    print_success "Database has been restored from backup"
    print_info "Safety backup location: /root/safety-backup-before-restore-*"
    echo ""
    print_info "Next steps:"
    echo "  1. Check backend logs: docker logs multivendor_backend --tail 50"
    echo "  2. Test API endpoints: curl https://api.indexo.ir/api/"
    echo "  3. Test frontend: https://indexo.ir"
    echo "  4. Run migrations if needed: docker exec multivendor_backend python manage.py migrate"
    echo "  5. Collect static files if needed: docker exec multivendor_backend python manage.py collectstatic --noinput"
    echo ""
}

# Run main function
main


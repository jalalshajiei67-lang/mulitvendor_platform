#!/bin/bash

# ============================================
# Old Vue Code Cleanup Script
# ============================================

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         🧹 Old Vue Code Cleanup Script                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -d "multivendor_platform/front_end" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

cd multivendor_platform/front_end

print_info "Current directory: $(pwd)"
echo ""

# Warning
print_warning "⚠️  WARNING: This will permanently delete old Vue code!"
print_warning "Make sure you have:"
echo "  1. Tested Nuxt app thoroughly"
echo "  2. Deployed Nuxt to production"
echo "  3. Verified everything works"
echo ""

read -p "Do you want to continue? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    print_info "Cleanup cancelled. No changes made."
    exit 0
fi

echo ""
print_info "Starting cleanup process..."
echo ""

# Step 1: Create Backup
print_info "Step 1: Creating backup..."

BACKUP_DIR="../../backups"
BACKUP_FILE="vue-app-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

mkdir -p "$BACKUP_DIR"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    src/ \
    dist/ \
    Dockerfile \
    Dockerfile.local \
    vite.config.js \
    eslint.config.js \
    jsconfig.json \
    index.html \
    package.json \
    package-lock.json \
    2>/dev/null || true

if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    print_success "Backup created: $BACKUP_FILE ($BACKUP_SIZE)"
    print_info "Location: $BACKUP_DIR/$BACKUP_FILE"
else
    print_error "Failed to create backup!"
    exit 1
fi

echo ""
read -p "Backup created. Continue with cleanup? (yes/no): " confirm2
if [ "$confirm2" != "yes" ]; then
    print_info "Cleanup cancelled. Backup preserved."
    exit 0
fi

echo ""

# Step 2: Remove Old Code
print_info "Step 2: Removing old Vue code..."
echo ""

# Remove src directory
if [ -d "src" ]; then
    print_warning "Removing src/ directory..."
    rm -rf src/
    print_success "src/ removed"
fi

# Remove dist directory
if [ -d "dist" ]; then
    print_warning "Removing dist/ directory..."
    rm -rf dist/
    print_success "dist/ removed"
fi

# Remove old Dockerfiles
if [ -f "Dockerfile" ]; then
    print_warning "Removing old Dockerfile..."
    rm -f Dockerfile
    print_success "Dockerfile removed"
fi

if [ -f "Dockerfile.local" ]; then
    print_warning "Removing Dockerfile.local..."
    rm -f Dockerfile.local
    print_success "Dockerfile.local removed"
fi

# Remove config files
if [ -f "vite.config.js" ]; then
    print_warning "Removing vite.config.js..."
    rm -f vite.config.js
    print_success "vite.config.js removed"
fi

if [ -f "eslint.config.js" ]; then
    print_warning "Removing eslint.config.js..."
    rm -f eslint.config.js
    print_success "eslint.config.js removed"
fi

if [ -f "jsconfig.json" ]; then
    print_warning "Removing jsconfig.json..."
    rm -f jsconfig.json
    print_success "jsconfig.json removed"
fi

if [ -f "index.html" ]; then
    print_warning "Removing index.html..."
    rm -f index.html
    print_success "index.html removed"
fi

if [ -f "package.json" ]; then
    print_warning "Removing old package.json..."
    rm -f package.json
    print_success "package.json removed"
fi

if [ -f "package-lock.json" ]; then
    print_warning "Removing old package-lock.json..."
    rm -f package-lock.json
    print_success "package-lock.json removed"
fi

echo ""
print_success "Old Vue code removed successfully!"
echo ""

# Step 3: Show what remains
print_info "Step 3: Remaining structure..."
echo ""
echo "front_end/"
ls -1 | sed 's/^/  ├── /'
echo ""

# Step 4: Verify Nuxt app
print_info "Step 4: Verifying Nuxt app..."
echo ""

if [ -d "nuxt" ]; then
    print_success "Nuxt directory exists"
    
    if [ -f "nuxt/package.json" ]; then
        print_success "Nuxt package.json found"
    else
        print_warning "Nuxt package.json not found"
    fi
    
    if [ -f "nuxt/nuxt.config.ts" ]; then
        print_success "Nuxt config found"
    else
        print_warning "Nuxt config not found"
    fi
else
    print_error "Nuxt directory not found!"
    print_error "Something went wrong. Restore from backup!"
    exit 1
fi

echo ""

# Step 5: Size comparison
print_info "Step 5: Calculating space saved..."
echo ""

if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -sh "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    print_info "Old code size (compressed): $BACKUP_SIZE"
fi

CURRENT_SIZE=$(du -sh . | cut -f1)
print_info "Current directory size: $CURRENT_SIZE"

echo ""

# Final summary
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   ✅ Cleanup Complete!                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

print_success "Old Vue code has been removed"
print_success "Backup saved to: $BACKUP_DIR/$BACKUP_FILE"
echo ""

print_info "Next steps:"
echo "  1. Test Nuxt app: cd nuxt && npm run dev"
echo "  2. Build Nuxt app: npm run build"
echo "  3. Test Docker: docker-compose build frontend"
echo "  4. Commit changes: git add . && git commit -m 'Clean up old Vue code'"
echo ""

print_warning "To restore from backup:"
echo "  tar -xzf $BACKUP_DIR/$BACKUP_FILE"
echo ""

print_success "Cleanup script completed successfully! 🎉"
















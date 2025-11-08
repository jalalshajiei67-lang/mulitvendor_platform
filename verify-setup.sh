#!/bin/bash

# Setup Verification Script
# Checks if all deployment files are in place before deploying

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $description"
        return 0
    else
        echo -e "${RED}✗${NC} $description (missing: $file)"
        ((ERRORS++))
        return 1
    fi
}

check_dir() {
    local dir=$1
    local description=$2
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $description"
        return 0
    else
        echo -e "${RED}✗${NC} $description (missing: $dir)"
        ((ERRORS++))
        return 1
    fi
}

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Deployment Setup Verification        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}Checking Docker Configuration...${NC}"
check_file "docker-compose.yml" "Docker Compose configuration"
check_file ".dockerignore" "Docker ignore file"
check_file "Dockerfile" "Backend Dockerfile"
check_file "requirements.txt" "Python requirements"

echo ""
echo -e "${YELLOW}Checking Environment Configuration...${NC}"
check_file ".env.production" "Production environment template"
if check_file ".env" "Environment configuration"; then
    # Check critical env vars
    if grep -q "SECRET_KEY=" .env && ! grep -q "your-super-secret-key" .env; then
        echo -e "  ${GREEN}✓${NC} SECRET_KEY is configured"
    else
        echo -e "  ${YELLOW}⚠${NC} SECRET_KEY needs to be set"
        ((ERRORS++))
    fi
    
    if grep -q "DB_PASSWORD=" .env && ! grep -q "changeme" .env; then
        echo -e "  ${GREEN}✓${NC} DB_PASSWORD is configured"
    else
        echo -e "  ${YELLOW}⚠${NC} DB_PASSWORD should be changed from default"
    fi
fi

echo ""
echo -e "${YELLOW}Checking Nginx Configuration...${NC}"
check_dir "nginx" "Nginx directory"
check_file "nginx/nginx.conf" "Nginx main config"
check_file "nginx/conf.d/default.conf" "Nginx default config"

echo ""
echo -e "${YELLOW}Checking Deployment Scripts...${NC}"
check_file "deploy.sh" "Linux/Mac deployment script"
check_file "deploy-windows.bat" "Windows deployment script"
check_file "server-deploy.sh" "Server setup script"
check_file "setup-ssl.sh" "SSL setup script"
check_file "manage-deployment.sh" "Management interface"

echo ""
echo -e "${YELLOW}Checking Utility Scripts...${NC}"
check_file "monitor.sh" "Monitoring script"
check_file "health-check.sh" "Health check script"
check_file "backup-database.sh" "Backup script"
check_file "restore-database.sh" "Restore script"
check_file "update-app.sh" "Update script"
check_file "test-connection.sh" "Connection test script"

echo ""
echo -e "${YELLOW}Checking Documentation...${NC}"
check_file "START_DEPLOYMENT_HERE.md" "Getting started guide"
check_file "QUICK_START.md" "Quick start guide"
check_file "DEPLOYMENT_GUIDE.md" "Comprehensive guide"
check_file "README_DEPLOYMENT.md" "Deployment overview"
check_file "DEPLOYMENT_SUMMARY.md" "Deployment summary"

echo ""
echo -e "${YELLOW}Checking Project Structure...${NC}"
check_dir "multivendor_platform" "Django project directory"
check_dir "multivendor_platform/multivendor_platform" "Django backend"
check_dir "multivendor_platform/front_end" "Vue.js frontend"
check_file "multivendor_platform/front_end/Dockerfile" "Frontend Dockerfile"

echo ""
echo "═══════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Ready to deploy.${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Ensure .env file is properly configured"
    echo "2. Run deployment:"
    echo "   Windows: deploy-windows.bat"
    echo "   Linux/Mac: ./deploy.sh"
    echo ""
    echo "3. Or use one-command deploy:"
    echo "   ./deploy-one-command.sh"
    exit 0
else
    echo -e "${RED}✗ Found $ERRORS issue(s). Please fix before deploying.${NC}"
    exit 1
fi




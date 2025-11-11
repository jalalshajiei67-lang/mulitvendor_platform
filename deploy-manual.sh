#!/bin/bash

# Manual Deployment Script for CapRover
# This script deploys backend and frontend to CapRover manually

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "════════════════════════════════════════════════════════════"
echo "  🚀 CapRover Manual Deployment Script"
echo "════════════════════════════════════════════════════════════"
echo ""

# Check if CapRover CLI is installed
if ! command -v caprover &> /dev/null; then
    echo -e "${RED}❌ CapRover CLI is not installed${NC}"
    echo "Install it with: npm install -g caprover"
    exit 1
fi

# Function to deploy backend
deploy_backend() {
    echo -e "${YELLOW}[1/2] Deploying Backend...${NC}"
    echo ""
    
    # Create tarball
    echo "Creating backend tarball..."
    cp captain-definition-backend captain-definition
    tar -czf backend-deploy.tar.gz \
        --exclude='multivendor_platform/front_end' \
        --exclude='**/venv' \
        --exclude='**/__pycache__' \
        --exclude='**/.pytest_cache' \
        --exclude='**/node_modules' \
        --exclude='*.pyc' \
        --exclude='*.pyo' \
        --exclude='*.sqlite3' \
        --exclude='.git' \
        captain-definition \
        Dockerfile.backend \
        multivendor_platform/
    
    echo -e "${GREEN}✓ Backend tarball created ($(du -h backend-deploy.tar.gz | cut -f1))${NC}"
    echo ""
    
    # Deploy
    echo "Deploying to CapRover..."
    caprover deploy --tarFile backend-deploy.tar.gz
    
    # Cleanup
    rm -f captain-definition backend-deploy.tar.gz
    
    echo ""
    echo -e "${GREEN}✅ Backend deployed successfully!${NC}"
    echo -e "   URL: https://multivendor-backend.indexo.ir"
    echo ""
}

# Function to deploy frontend
deploy_frontend() {
    echo -e "${YELLOW}[2/2] Deploying Frontend...${NC}"
    echo ""
    
    # Create tarball
    echo "Creating frontend tarball..."
    cp captain-definition-frontend captain-definition
    tar -czf frontend-deploy.tar.gz \
        --exclude='**/node_modules' \
        --exclude='**/dist' \
        --exclude='**/.output' \
        --exclude='**/.nuxt' \
        --exclude='**/__pycache__' \
        --exclude='.git' \
        captain-definition \
        multivendor_platform/front_end/nuxt/
    
    echo -e "${GREEN}✓ Frontend tarball created ($(du -h frontend-deploy.tar.gz | cut -f1))${NC}"
    echo ""
    
    # Deploy
    echo "Deploying to CapRover..."
    caprover deploy --tarFile frontend-deploy.tar.gz
    
    # Cleanup
    rm -f captain-definition frontend-deploy.tar.gz
    
    echo ""
    echo -e "${GREEN}✅ Frontend deployed successfully!${NC}"
    echo -e "   URL: https://indexo.ir"
    echo ""
}

# Main execution
case "${1:-both}" in
    backend)
        deploy_backend
        ;;
    frontend)
        deploy_frontend
        ;;
    both)
        deploy_backend
        deploy_frontend
        ;;
    *)
        echo "Usage: $0 [backend|frontend|both]"
        echo ""
        echo "Examples:"
        echo "  $0           # Deploy both backend and frontend"
        echo "  $0 backend   # Deploy only backend"
        echo "  $0 frontend  # Deploy only frontend"
        exit 1
        ;;
esac

echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Test your deployment:"
echo "  Frontend: https://indexo.ir"
echo "  Backend:  https://multivendor-backend.indexo.ir/api/"
echo "  Admin:    https://multivendor-backend.indexo.ir/admin/"
echo ""


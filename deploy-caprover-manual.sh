#!/bin/bash

# Manual CapRover Deployment Script
# Use this if the GitHub action fails

set -e

echo "🚀 Starting CapRover Manual Deployment..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration - Update these with your actual values
CAPROVER_SERVER="${CAPROVER_SERVER:-https://captain.indexo.ir}"
BACKEND_APP="${CAPROVER_APP_BACKEND:-backend}"
FRONTEND_APP="${CAPROVER_APP_FRONTEND:-frontend}"
BACKEND_TOKEN="${CAPROVER_APP_TOKEN_BACKEND}"
FRONTEND_TOKEN="${CAPROVER_APP_TOKEN_FRONTEND}"

# Check if tokens are set
if [ -z "$BACKEND_TOKEN" ]; then
    echo -e "${RED}Error: CAPROVER_APP_TOKEN_BACKEND environment variable not set${NC}"
    exit 1
fi

if [ -z "$FRONTEND_TOKEN" ]; then
    echo -e "${RED}Error: CAPROVER_APP_TOKEN_FRONTEND environment variable not set${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Installing CapRover CLI...${NC}"
npm install -g caprover

echo -e "${YELLOW}Step 2: Deploying Backend...${NC}"
# Create backend tarball
tar -czf deploy-backend.tar.gz \
    captain-definition \
    Dockerfile.backend \
    multivendor_platform/requirements.txt \
    multivendor_platform/multivendor_platform/

# Deploy backend
caprover deploy \
    -h "$CAPROVER_SERVER" \
    -p "$BACKEND_TOKEN" \
    -a "$BACKEND_APP" \
    -t deploy-backend.tar.gz

echo -e "${GREEN}✓ Backend deployed successfully!${NC}"

echo -e "${YELLOW}Step 3: Deploying Frontend...${NC}"
# Create frontend tarball from nuxt directory
cd multivendor_platform/front_end/nuxt
tar -czf deploy-frontend.tar.gz \
    captain-definition \
    Dockerfile \
    package*.json \
    nuxt.config.ts \
    tsconfig.json \
    app.vue \
    public/ \
    components/ \
    composables/ \
    layouts/ \
    middleware/ \
    pages/ \
    plugins/ \
    server/ \
    stores/ \
    assets/ \
    types/

# Deploy frontend
caprover deploy \
    -h "$CAPROVER_SERVER" \
    -p "$FRONTEND_TOKEN" \
    -a "$FRONTEND_APP" \
    -t deploy-frontend.tar.gz

cd ../../..

echo -e "${GREEN}✓ Frontend deployed successfully!${NC}"
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"

# Cleanup
rm -f deploy-backend.tar.gz multivendor_platform/front_end/nuxt/deploy-frontend.tar.gz

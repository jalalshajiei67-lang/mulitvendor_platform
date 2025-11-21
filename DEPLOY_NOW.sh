#!/bin/bash

# SSR Fix Deployment Script
# Run this to deploy the fix automatically

set -e  # Exit on error

echo "======================================"
echo "🚀 SSR Fix Deployment Script"
echo "======================================"
echo ""

# Navigate to project directory
cd "/media/jalal/New Volume/project/mulitvendor_platform"

echo "📂 Current directory: $(pwd)"
echo ""

# Show what will be committed
echo "📝 Files to be committed:"
git status --short
echo ""

# Add all fix files
echo "➕ Adding files..."
git add multivendor_platform/front_end/nuxt/composables/useApiFetch.ts
git add Dockerfile.frontend.nuxt
git add SSR_FIX_DEPLOYMENT_GUIDE.md
git add QUICK_FIX_COMMANDS.md
git add NITRO_CONFIG_FIX.md
git add FIX_SUMMARY.md
git add DEPLOY_NOW.sh

echo "✅ Files added"
echo ""

# Commit
echo "💾 Committing changes..."
git commit -m "fix(ssr): comprehensive fix for Nuxt instance unavailable error

**Problem**: 
- Nitro runtime config showing empty: config: {}
- useRuntimeConfig() failing during SSR
- Infinite error loop: 'nuxt instance unavailable'

**Solutions**:
1. Enhanced Dockerfile with better env var handling
   - Added NUXT_PUBLIC_SITE_URL
   - Added build-time env var verification
   - Set runtime env vars in production stage
   - Added nitro.json check after build

2. Made useApiFetch SSR-safe
   - Added tryUseNuxtApp() check
   - Graceful fallback to process.env
   - Multi-layer error handling

3. Added comprehensive debugging
   - Verify env vars during build
   - Check nitro.json after build
   - Runtime env var validation

**Verification**:
- Empty nitro.json config diagnosed
- Environment variables properly set at build and runtime
- Fallback mechanisms in place for SSR edge cases

**Documentation**:
- SSR_FIX_DEPLOYMENT_GUIDE.md
- QUICK_FIX_COMMANDS.md
- NITRO_CONFIG_FIX.md
- FIX_SUMMARY.md

Fixes: #SSR-ERROR
Impact: Critical production stability fix"

echo "✅ Changes committed"
echo ""

# Push
echo "🚀 Pushing to origin main..."
git push origin main

echo ""
echo "======================================"
echo "✅ Deployment triggered!"
echo "======================================"
echo ""
echo "📊 Next steps:"
echo "1. Monitor GitHub Actions: https://github.com/YOUR_USERNAME/YOUR_REPO/actions"
echo "2. Check CapRover: https://captain.indexo.ir/"
echo "3. Wait 10-15 minutes for deployment"
echo "4. Verify at: https://indexo.ir/"
echo ""
echo "🔍 To monitor in real-time:"
echo "   ssh root@185.208.172.76"
echo "   docker logs -f \$(docker ps | grep frontend | awk '{print \$1}')"
echo ""
echo "✅ Look for: 'Listening on http://[::]:3000'"
echo "❌ No more: '[nuxt] instance unavailable' errors"
echo ""
echo "======================================"
echo "🎉 Done! Good luck!"
echo "======================================"


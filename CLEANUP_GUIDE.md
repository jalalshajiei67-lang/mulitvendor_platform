# Cleanup Guide - Removing Old Vue Codebase

**⚠️ IMPORTANT:** Only perform cleanup after thorough testing of the Nuxt application!

---

## Prerequisites

Before starting cleanup, ensure:

1. ✅ All features work correctly in Nuxt
2. ✅ All pages load and function properly
3. ✅ Authentication flows work
4. ✅ Admin functionality works
5. ✅ Mobile responsiveness is correct
6. ✅ RTL layout is correct
7. ✅ Production build works (`npm run build`)
8. ✅ Docker build works

---

## Step-by-Step Cleanup Process

### Step 1: Backup (Recommended)

```bash
# Create a backup branch
git checkout -b backup-before-cleanup
git add .
git commit -m "Backup before cleanup"
git checkout main
```

### Step 2: Remove Old Vue Codebase

```bash
cd multivendor_platform/front_end

# Remove old Vue source directory
rm -rf src/

# Remove old configuration files
rm vite.config.js
rm index.html
rm jsconfig.json
rm eslint.config.js

# Remove old public assets (if not needed)
# Keep only what's needed for Nuxt
```

### Step 3: Clean Up Old Dependencies

Edit `multivendor_platform/front_end/package.json` and remove:

```json
{
  "dependencies": {
    // Remove these if not needed:
    "vue-router": "^4.x.x",  // Nuxt handles routing
    "vuex": "^4.x.x",        // Using Pinia instead
    "axios": "^1.x.x",       // Using Nuxt's $fetch
    // Keep Vuetify, Vue, and other shared dependencies
  }
}
```

Then run:
```bash
cd multivendor_platform/front_end
npm install
```

### Step 4: Update Root package.json (if exists)

If there's a root `package.json` in `multivendor_platform/front_end/`, update it to remove old scripts:

```json
{
  "scripts": {
    // Remove old Vue/Vite scripts:
    // "dev": "vite",
    // "build": "vite build",
    // "preview": "vite preview",
    
    // Keep or add Nuxt scripts if needed
  }
}
```

### Step 5: Update Docker Configuration

Ensure `docker-compose.local.yml` and other Docker files point to Nuxt:

```yaml
frontend:
  build:
    context: ./multivendor_platform/front_end/nuxt
    dockerfile: Dockerfile
```

### Step 6: Update CI/CD Pipelines

Update GitHub Actions or other CI/CD configurations:

```yaml
# Example GitHub Actions update
- name: Build Nuxt
  run: |
    cd multivendor_platform/front_end/nuxt
    npm install
    npm run build
```

### Step 7: Update Documentation

Update these files:

1. **README.md**
   - Update installation instructions
   - Update development setup
   - Update build commands
   - Update deployment instructions

2. **Development Guides**
   - Update any guides referencing old Vue setup
   - Update API documentation if needed

### Step 8: Remove Old Migration Documentation

After cleanup is complete, you can optionally remove:

```bash
# These are historical - keep for reference or remove:
# FORM_MIGRATION_COMPLETE.md
# MIGRATION_PROGRESS.md
# NUXT_MIGRATION_STATUS.md
# MIGRATION_FEEDBACK.md
# PHASE1_MIGRATION_COMPLETE.md
# PHASE2_MIGRATION_COMPLETE.md

# Keep these:
# MIGRATION_COMPLETE.md (final summary)
# CLEANUP_GUIDE.md (this file)
```

---

## Verification Checklist

After cleanup, verify:

- [ ] Nuxt dev server starts: `cd nuxt && npm run dev`
- [ ] Nuxt build works: `cd nuxt && npm run build`
- [ ] Docker build works: `docker-compose build frontend`
- [ ] All pages load correctly
- [ ] No references to old `src/` directory
- [ ] No references to `vite.config.js`
- [ ] No broken imports
- [ ] No console errors

---

## Rollback Plan

If something goes wrong:

```bash
# Restore from backup branch
git checkout backup-before-cleanup
git checkout -b rollback-restore
git checkout main
git reset --hard backup-before-cleanup
```

---

## Post-Cleanup Tasks

1. **Update .gitignore**
   ```gitignore
   # Remove old Vue-specific ignores if any
   # Keep Nuxt-specific ignores
   ```

2. **Update Environment Variables**
   - Ensure all env vars use `NUXT_PUBLIC_` prefix
   - Remove old `VITE_` prefixed vars

3. **Final Testing**
   - Run full test suite
   - Test all user flows
   - Test admin functionality
   - Test mobile devices

---

## Notes

- Keep migration documentation for reference
- The old codebase can be restored from git history if needed
- Consider keeping a backup branch for a few weeks
- Update team documentation and onboarding guides

---

**⚠️ Remember:** Only perform cleanup after thorough testing!


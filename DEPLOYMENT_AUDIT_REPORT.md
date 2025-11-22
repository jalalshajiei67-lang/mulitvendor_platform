# Deployment Configuration Audit Report

**Date:** 2025-01-27  
**Project:** Multivendor Platform  
**Auditor:** Automated Deployment Audit  
**Status:** ⚠️ Issues Found - Action Required

---

## Executive Summary

This comprehensive audit examined all deployment-related configurations including GitHub Actions workflows, CapRover setup, Dockerfiles, environment variables, and documentation. **15 critical issues** and **8 warnings** were identified that need attention before deployment.

### Severity Breakdown
- 🔴 **Critical Issues:** 8
- 🟡 **Warnings:** 7
- 🟢 **Good Practices:** Multiple

---

## 1. GitHub Actions Workflows

### ✅ Strengths
- Workflow triggers correctly configured (push to main, manual dispatch)
- Proper deployment order (backend → frontend)
- File existence checks before deployment
- Security scan for hardcoded secrets
- Proper use of GitHub Actions caching

### 🔴 Critical Issues

#### Issue 1.1: Secret Name Mismatch
**Severity:** 🔴 Critical  
**Location:** `.github/workflows/deploy-caprover.yml` vs Documentation

**Problem:**
- Workflow uses: `CAPROVER_BACKEND_APP_NAME` and `CAPROVER_FRONTEND_APP_NAME`
- Documentation (`ENV_VARIABLES.md`) mentions: `CAPROVER_APP_BACKEND` and `CAPROVER_APP_FRONTEND`
- `GITHUB_SECRETS_SETUP.md` mentions: `CAPROVER_APP_BACKEND` and `CAPROVER_APP_FRONTEND`

**Impact:** Deployment will fail if secrets are named according to documentation.

**Recommendation:**
- **Option A (Recommended):** Update documentation to match workflow (use `CAPROVER_BACKEND_APP_NAME` and `CAPROVER_FRONTEND_APP_NAME`)
- **Option B:** Update workflow to match documentation (use `CAPROVER_APP_BACKEND` and `CAPROVER_APP_FRONTEND`)

#### Issue 1.2: Missing Secret Usage
**Severity:** 🟡 Warning  
**Location:** `.github/workflows/deploy-caprover.yml`

**Problem:**
- Workflow uses `env.CAPROVER_SERVER` (hardcoded in workflow)
- Documentation mentions `CAPROVER_URL` secret
- No secret is used for server URL

**Impact:** Server URL is hardcoded, making it harder to change environments.

**Recommendation:** Use `${{ secrets.CAPROVER_URL }}` instead of hardcoded value, or document that it's intentionally hardcoded.

### 🟡 Warnings

#### Warning 1.1: Duplicate Test Workflow
**Location:** `.github/workflows/test.yml` and `.github/workflows/ci.yml`

Both workflows run similar tests. Consider consolidating or clearly documenting the difference.

---

## 2. Dockerfiles

### 🔴 Critical Issues

#### Issue 2.1: Port Mismatch in Root Dockerfile
**Severity:** 🔴 Critical  
**Location:** `Dockerfile` (root)

**Problem:**
- Dockerfile exposes port **8000** and uses Daphne on port 8000
- Healthcheck checks port **8000**
- But `Dockerfile.backend` uses port **80** with Gunicorn
- `captain-definition` points to root `Dockerfile`
- CapRover expects apps to run on port **80** (or configured port)

**Impact:** Backend may not be accessible through CapRover if using root Dockerfile.

**Recommendation:**
- **Option A (Recommended):** Update root `Dockerfile` to use port 80 and Gunicorn (like `Dockerfile.backend`)
- **Option B:** Update `captain-definition` to point to `Dockerfile.backend`
- **Option C:** Configure CapRover backend app to use port 8000

#### Issue 2.2: Inconsistent Dockerfile Usage
**Severity:** 🔴 Critical  
**Location:** Multiple Dockerfiles

**Problem:**
- Root `Dockerfile` uses Daphne on port 8000
- `Dockerfile.backend` uses Gunicorn on port 80 with entrypoint script
- `captain-definition` points to root `Dockerfile`
- GitHub Actions workflow includes root `Dockerfile` in tar

**Impact:** Unclear which Dockerfile is actually used in production.

**Recommendation:**
- Standardize on one Dockerfile for backend deployment
- If using `Dockerfile.backend`, update `captain-definition` to point to it
- Remove or clearly document the purpose of alternative Dockerfiles

#### Issue 2.3: Requirements.txt Path Inconsistency
**Severity:** 🟡 Warning  
**Location:** `Dockerfile` vs `Dockerfile.backend`

**Problem:**
- Root `Dockerfile` copies `requirements.txt` from root
- `Dockerfile.backend` copies `multivendor_platform/requirements.txt`
- GitHub Actions includes root `requirements.txt` in tar

**Impact:** May use wrong requirements file if paths don't match.

**Recommendation:** Ensure consistent requirements.txt location and update Dockerfiles accordingly.

#### Issue 2.4: Frontend Dockerfile Path Issues
**Severity:** 🟡 Warning  
**Location:** `Dockerfile.frontend.nuxt` vs `multivendor_platform/front_end/nuxt/Dockerfile`

**Problem:**
- `Dockerfile.frontend.nuxt` (root) expects build context from root with `multivendor_platform/front_end/nuxt` path
- `multivendor_platform/front_end/nuxt/Dockerfile` expects build context from nuxt directory
- `captain-definition` in nuxt dir points to `./Dockerfile` (local)
- GitHub Actions creates tar from nuxt directory

**Impact:** Build context may be incorrect depending on which Dockerfile is used.

**Recommendation:** 
- Use `multivendor_platform/front_end/nuxt/Dockerfile` (already referenced by captain-definition)
- Remove or document `Dockerfile.frontend.nuxt` if not used

### ✅ Strengths
- Multi-stage builds for frontend (good for optimization)
- Proper healthchecks configured
- Environment variables properly used
- Node.js memory limits set for large builds

---

## 3. Captain-Definition Files

### ✅ Strengths
- Both files use schema version 2 (correct)
- Proper JSON format

### 🟡 Warnings

#### Warning 3.1: Backend Dockerfile Reference
**Location:** `captain-definition` (root)

**Problem:**
- Points to `./Dockerfile` which uses port 8000
- Should probably point to `Dockerfile.backend` or root Dockerfile should be fixed

**Recommendation:** Verify which Dockerfile should be used and update accordingly.

---

## 4. Django Settings (settings_caprover.py)

### ✅ Strengths
- Comprehensive environment variable usage
- Proper security settings for production
- Good CORS configuration
- Proper Redis/Channels setup
- SSL proxy header configuration
- Logging configuration with fallback

### 🟡 Warnings

#### Warning 4.1: Default Database Host
**Location:** `settings_caprover.py` line 94

**Problem:**
- Default DB_HOST is `srv-captain--multivendor-db`
- But some documentation mentions `srv-captain--postgres-db`

**Impact:** May cause confusion if database app is named differently.

**Recommendation:** Document the expected database app name clearly.

---

## 5. Environment Variables

### 🔴 Critical Issues

#### Issue 5.1: Inconsistent Database Service Names
**Severity:** 🔴 Critical  
**Location:** Multiple files

**Problem:**
- `ENV_VARIABLES.md`: `srv-captain--multivendor-db`
- `caprover-env-backend.txt`: `srv-captain--postgres-db`
- `settings_caprover.py`: `srv-captain--multivendor-db` (default)
- `REQUIREMENTS_CI_CD_CAPROVER.md`: `srv-captain--postgres`

**Impact:** Database connection will fail if wrong service name is used.

**Recommendation:** 
- Standardize on one database service name
- Update all documentation and config files to match
- Document the actual database app name in CapRover

#### Issue 5.2: Frontend API URL Inconsistency
**Severity:** 🔴 Critical  
**Location:** Multiple files

**Problem:**
- `ENV_VARIABLES.md`: `NUXT_PUBLIC_API_BASE=https://api.indexo.ir/api`
- `caprover-env-frontend.txt`: `VITE_API_BASE_URL=https://multivendor-backend.indexo.ir` (wrong variable name for Nuxt)
- `Dockerfile.frontend.nuxt`: `NUXT_PUBLIC_API_BASE=https://multivendor-backend.indexo.ir/api`
- `settings_caprover.py`: Default CORS includes `https://multivendor-backend.indexo.ir`

**Impact:** Frontend may not connect to backend if URLs don't match.

**Recommendation:**
- Standardize on either `api.indexo.ir` or `multivendor-backend.indexo.ir`
- Update all references consistently
- Use `NUXT_PUBLIC_API_BASE` (not `VITE_API_BASE_URL`) for Nuxt 3

#### Issue 5.3: Old IP Address in Files
**Severity:** 🟡 Warning  
**Location:** `deploy.sh`, `env.template`

**Problem:**
- `deploy.sh` uses IP `158.255.74.123`
- `env.template` mentions IP `158.255.74.123`
- Current VPS IP is `185.208.172.76`

**Impact:** Old deployment scripts may fail or deploy to wrong server.

**Recommendation:** Update all IP addresses to current VPS IP or use domain names.

### ✅ Strengths
- Comprehensive environment variable documentation
- Good separation of dev/prod variables
- Security best practices followed

---

## 6. GitHub Secrets

### 🔴 Critical Issues

#### Issue 6.1: Secret Name Inconsistencies
**Severity:** 🔴 Critical  
**Location:** Workflow vs Documentation

**Problem:**
- Workflow expects: `CAPROVER_PASSWORD`, `CAPROVER_BACKEND_APP_NAME`, `CAPROVER_FRONTEND_APP_NAME`
- `ENV_VARIABLES.md` mentions: `CAPROVER_SERVER`, `CAPROVER_APP_BACKEND`, `CAPROVER_APP_FRONTEND`
- `GITHUB_SECRETS_SETUP.md` mentions: `CAPROVER_APP_BACKEND`, `CAPROVER_APP_FRONTEND`, `CAPROVER_APP_TOKEN_BACKEND`, `CAPROVER_APP_TOKEN_FRONTEND`
- Workflow doesn't use app tokens (uses password instead)

**Impact:** Users following documentation will set wrong secret names, causing deployment failures.

**Recommendation:**
- Update all documentation to match actual workflow usage
- Or update workflow to match documentation
- Document which authentication method is used (password vs app tokens)

---

## 7. Deployment Scripts

### 🟡 Warnings

#### Warning 7.1: Outdated VPS IP
**Location:** `deploy.sh` line 19

**Problem:**
- Script uses old IP `158.255.74.123`
- Current IP is `185.208.172.76`

**Recommendation:** Update IP address or use domain name.

#### Warning 7.2: Script Uses Docker Compose
**Location:** `deploy.sh`, `deploy-nuxt.sh`

**Problem:**
- Scripts deploy using Docker Compose
- But production uses CapRover (not Docker Compose)

**Impact:** Scripts may not work for CapRover deployment.

**Recommendation:** 
- Document that these are for local/docker-compose deployment
- Or create separate CapRover deployment scripts

---

## 8. Documentation Consistency

### 🔴 Critical Issues

#### Issue 8.1: Domain Name Inconsistencies
**Severity:** 🔴 Critical  
**Location:** Multiple documentation files

**Problem:**
- Backend domain mentioned as both `api.indexo.ir` and `multivendor-backend.indexo.ir`
- Frontend domain mentioned as `indexo.ir`, `www.indexo.ir`, and `multivendor-frontend.indexo.ir`
- Not clear which is the actual production domain

**Impact:** Configuration may use wrong domains, causing CORS/connection issues.

**Recommendation:**
- Document the actual production domains clearly
- Update all references to match
- Create a single source of truth for domain configuration

#### Issue 8.2: App Name Inconsistencies
**Severity:** 🟡 Warning  
**Location:** Multiple files

**Problem:**
- Most files use `multivendor-backend` and `multivendor-frontend`
- Some older files may use different names

**Recommendation:** Verify actual CapRover app names and update all references.

### ✅ Strengths
- Extensive documentation
- Multiple guides for different scenarios
- Good troubleshooting sections

---

## 9. File Path Consistency

### 🔴 Critical Issues

#### Issue 9.1: Requirements.txt Location
**Severity:** 🟡 Warning  
**Location:** Multiple locations

**Problem:**
- Root `requirements.txt` exists
- `multivendor_platform/requirements.txt` may exist
- Dockerfiles reference different locations

**Recommendation:** Verify which requirements.txt is correct and standardize.

#### Issue 9.2: Settings File Path
**Severity:** ✅ Verified  
**Location:** Dockerfiles

**Status:** ✅ Correct - All Dockerfiles use `multivendor_platform.settings_caprover`

---

## 10. Dependencies

### ✅ Strengths
- Python 3.11 consistently used
- Node.js 20 consistently used
- Requirements.txt properly maintained

### 🟡 Warnings

#### Warning 10.1: Missing Dependencies Check
**Location:** Requirements files

**Recommendation:** Verify all dependencies in requirements.txt are actually used and up to date.

---

## Summary of Critical Issues

### Must Fix Before Deployment:

1. **Secret Name Mismatch** - Workflow and documentation use different secret names
2. **Port Mismatch** - Root Dockerfile uses port 8000, should use 80 for CapRover
3. **Dockerfile Inconsistency** - Multiple Dockerfiles, unclear which is used
4. **Database Service Name** - Inconsistent across files (`multivendor-db` vs `postgres-db`)
5. **Frontend API URL** - Inconsistent (`api.indexo.ir` vs `multivendor-backend.indexo.ir`)
6. **Domain Name Confusion** - Multiple domains mentioned, unclear which are production
7. **Environment Variable Names** - Frontend uses wrong variable name (`VITE_API_BASE_URL` instead of `NUXT_PUBLIC_API_BASE`)

### Should Fix Soon:

8. **Old IP Addresses** - Update to current VPS IP
9. **Documentation Updates** - Align all docs with actual configuration
10. **Deployment Scripts** - Update or document purpose clearly

---

## Recommendations Priority

### Priority 1 (Critical - Fix Immediately):
1. Standardize GitHub secret names across workflow and documentation
2. Fix Dockerfile port configuration (use port 80)
3. Standardize database service name across all files
4. Standardize frontend API URL and variable name
5. Document actual production domains

### Priority 2 (Important - Fix Before Next Deployment):
6. Update old IP addresses
7. Consolidate or clearly document Dockerfile usage
8. Update deployment scripts or mark as deprecated

### Priority 3 (Nice to Have):
9. Consolidate test workflows
10. Review and update all documentation for consistency

---

## Action Items

### Immediate Actions:
- [ ] Decide on GitHub secret naming convention and update all files
- [ ] Fix root Dockerfile to use port 80 or update captain-definition
- [ ] Verify actual database app name in CapRover and update all references
- [ ] Verify actual production domains and update all references
- [ ] Update frontend environment variable name in caprover-env-frontend.txt

### Short-term Actions:
- [ ] Update all IP addresses to current VPS IP
- [ ] Create single source of truth document for deployment configuration
- [ ] Update or remove outdated deployment scripts
- [ ] Verify requirements.txt location and update Dockerfiles if needed

### Long-term Actions:
- [ ] Consolidate documentation
- [ ] Create deployment configuration validation script
- [ ] Set up automated deployment testing

---

## Files Requiring Updates

### Critical Updates:
1. `.github/workflows/deploy-caprover.yml` - Secret names or documentation
2. `Dockerfile` (root) - Port configuration
3. `ENV_VARIABLES.md` - Secret names, database service name, API URLs
4. `caprover-env-backend.txt` - Database service name
5. `caprover-env-frontend.txt` - Variable name and API URL
6. `GITHUB_SECRETS_SETUP.md` - Secret names

### Recommended Updates:
7. `deploy.sh` - IP address
8. `env.template` - IP address
9. `REQUIREMENTS_CI_CD_CAPROVER.md` - Database service name
10. All documentation files - Domain names

---

## Positive Findings

### ✅ Good Practices Found:
- Comprehensive environment variable documentation
- Security best practices in settings
- Proper use of healthchecks
- Multi-stage Docker builds for optimization
- Good separation of concerns (dev vs prod)
- Extensive documentation
- Proper use of GitHub Actions caching
- Security scanning in CI/CD

---

## Conclusion

The deployment configuration is **mostly well-structured** but has **critical inconsistencies** that will cause deployment failures. The main issues are:

1. **Naming inconsistencies** (secrets, services, domains)
2. **Port configuration mismatch**
3. **Multiple Dockerfiles** without clear documentation

**Recommendation:** Address Priority 1 issues before the next deployment. The configuration is fixable and the foundation is solid.

---

**Report Generated:** 2025-01-27  
**Next Review:** After Priority 1 fixes are implemented


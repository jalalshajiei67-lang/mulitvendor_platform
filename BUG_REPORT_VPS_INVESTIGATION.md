# Bug Report - VPS Production Investigation
**Date:** December 31, 2025  
**Server:** 46.249.101.84  
**Investigation Type:** Read-only (no changes made)

## Executive Summary

Two critical bugs were identified in the production environment:
1. **Categories API 404 Error** - Frontend SSR requests failing intermittently
2. **robots.txt Treated as Blog Post** - Routing conflict causing 404 errors

Both issues are non-fatal but impact user experience and generate error logs.

---

## Bug #1: Categories API Returns 404 During SSR

### Severity: **Medium**
### Status: **Intermittent**

### Description
The frontend application logs show 404 errors when fetching categories during server-side rendering (SSR):

```
Error fetching categories for filters: FetchError: [GET] "https://multivendor-backend.indexo.ir/api/categories/": 404 Not Found
```

### Investigation Findings

#### ✅ What Works:
- **Backend API is functional**: Direct curl requests return HTTP 200
- **Backend logs show successful requests**: Multiple 200 responses logged
- **Database has data**: 19 categories exist, all active
- **Network connectivity**: Frontend container can reach backend (tested with Node.js)
- **URL routing**: `/api/categories/` is properly registered in Django

#### ❌ What's Broken:
- **SSR requests fail**: Frontend SSR (server-side rendering) gets 404
- **Error occurs during page setup**: Happens in `setup()` function during initial page load
- **Timing issue suspected**: May occur during container startup or when backend is temporarily unavailable

### Root Cause Analysis

1. **Timing/Race Condition**: The error occurs during SSR setup, suggesting the frontend might be making requests before the backend is fully ready, or there's a race condition during container startup.

2. **SSL/TLS Certificate Issue**: 
   - Frontend has `NODE_TLS_REJECT_UNAUTHORIZED=0` (disables certificate verification)
   - This suggests there might be SSL certificate validation issues
   - However, manual Node.js test with `rejectUnauthorized: false` works

3. **Request Context**: The error happens specifically during SSR, not client-side, which suggests:
   - Different network path during SSR
   - Different error handling
   - Possible timeout or connection issue

### Evidence

```bash
# Backend logs show successful requests:
172.18.0.6:46696 - - [31/Dec/2025:20:20:57] "GET /api/categories/" 200 141849

# Direct API test works:
$ curl https://multivendor-backend.indexo.ir/api/categories/
# Returns: {"count": 19, "results": [...]}

# Frontend container can reach backend:
$ docker exec multivendor_frontend node -e "..."
# Status: 200
```

### Impact
- **User Experience**: Categories filter may not load on homepage
- **Error Logs**: Generates noise in logs
- **Functionality**: May cause incomplete page rendering during SSR

### Recommended Fixes

1. **Add Retry Logic**: Implement exponential backoff retry for SSR API calls
2. **Add Health Check**: Verify backend is ready before making SSR requests
3. **Error Handling**: Gracefully handle 404s and retry on client-side
4. **Timeout Configuration**: Increase timeout for SSR requests
5. **SSL Certificate**: Fix SSL certificate issue (remove `NODE_TLS_REJECT_UNAUTHORIZED=0`)

---

## Bug #2: robots.txt Treated as Blog Post Slug

### Severity: **Low** (but should be fixed)
### Status: **Consistent**

### Description
The frontend application attempts to fetch `/api/blog/posts/robots.txt/` as if "robots.txt" is a blog post slug, resulting in 404 errors:

```
Error fetching blog post: FetchError: [GET] "https://multivendor-backend.indexo.ir/api/blog/posts/robots.txt/": 404 Not Found
```

### Investigation Findings

#### ✅ What Works:
- **Backend correctly returns 404**: No blog post with slug "robots.txt" exists (as expected)
- **robots.txt endpoint exists**: Django serves `/robots.txt` correctly
- **Nuxt public folder**: `public/robots.txt` exists

#### ❌ What's Broken:
- **Nuxt routing conflict**: The catch-all route `pages/blog/[slug].vue` matches `/blog/robots.txt`
- **No slug validation**: Blog page doesn't validate slugs before fetching
- **Reserved paths not handled**: System files like robots.txt, sitemap.xml are treated as blog slugs

### Root Cause Analysis

1. **Nuxt File-Based Routing**: 
   - `pages/blog/[slug].vue` is a catch-all route that matches ANY path under `/blog/`
   - When a request comes for `/blog/robots.txt`, Nuxt treats "robots.txt" as the slug parameter
   - The blog page then tries to fetch it as a blog post

2. **Missing Validation**:
   - No validation to reject reserved/invalid slugs
   - No check for file extensions (.txt, .xml, etc.)
   - No early 404 for obviously invalid slugs

3. **Request Source**:
   - Could be from search engine crawlers
   - Could be from misconfigured links
   - Could be from internal navigation

### Evidence

```bash
# Backend correctly returns 404:
$ curl -I https://multivendor-backend.indexo.ir/api/blog/posts/robots.txt/
HTTP/2 404

# Frontend error log:
Error fetching blog post: FetchError: [GET] ".../api/blog/posts/robots.txt/": 404 Not Found
    at async fetchPage (file:///app/.output/server/chunks/build/_slug_-DmpVzigs.mjs:1:10225)
```

### Impact
- **Error Logs**: Generates unnecessary 404 errors in logs
- **Performance**: Wasted API requests for invalid slugs
- **SEO**: Potential confusion for search engines

### Recommended Fixes

1. **Add Slug Validation in Blog Page**:
   ```typescript
   // Reject reserved slugs and file extensions
   const reservedSlugs = ['robots.txt', 'sitemap.xml', 'favicon.ico', ...]
   const invalidExtensions = ['.txt', '.xml', '.ico', ...]
   
   if (!isValidSlug(slug.value)) {
     throw createError({ statusCode: 404, ... })
   }
   ```

2. **Create Explicit robots.txt Route** (optional):
   - Add `server/api/robots.txt.ts` to handle robots.txt explicitly
   - Or ensure Nuxt serves it from `public/robots.txt` before routing

3. **Add Middleware** (optional):
   - Create Nuxt middleware to intercept and handle reserved paths

---

## Additional Findings

### Security Warning
- **TLS Certificate Verification Disabled**: 
  ```
  NODE_TLS_REJECT_UNAUTHORIZED=0
  ```
  This is a security risk and should be fixed in production.

### Container Status
All containers are healthy and running:
- ✅ `multivendor_backend` - Up 7 hours (healthy)
- ✅ `multivendor_db` - Up 7 hours (healthy)
- ✅ `multivendor_frontend` - Up 7 hours (healthy)
- ✅ `multivendor_nginx` - Up 41 hours
- ✅ `traefik` - Up 41 hours
- ✅ `multivendor_redis` - Up 41 hours (healthy)

### Configuration
- **API Base URL**: `https://multivendor-backend.indexo.ir/api` ✅
- **Site URL**: `https://indexo.ir` ✅
- **CORS**: Properly configured ✅
- **ALLOWED_HOSTS**: Correctly set ✅

---

## Summary

### Critical Issues: **0**
### Medium Issues: **1** (Categories 404)
### Low Issues: **1** (robots.txt routing)
### Security Warnings: **1** (TLS verification disabled)

### Next Steps
1. Fix robots.txt routing issue (add slug validation)
2. Investigate and fix categories 404 during SSR (add retry logic)
3. Fix SSL certificate issue (remove insecure TLS setting)
4. Monitor logs after fixes to confirm resolution

---

## Technical Details

### Error Stack Traces

**Categories Error:**
```
Error fetching categories for filters: FetchError: [GET] "https://multivendor-backend.indexo.ir/api/categories/": 404 Not Found
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
    at async $fetch (file:///app/.output/server/chunks/nitro/nitro.mjs:1:45838)
    at async useApiFetch (file:///app/.output/server/chunks/build/server.mjs:1:36555)
    at async fetchCategories (file:///app/.output/server/chunks/build/index-D_9RiMSc.mjs:1:24462)
    at async Promise.all (index 0)
    at async setup (file:///app/.output/server/chunks/build/index-D_9RiMSc.mjs:1:25752)
```

**robots.txt Error:**
```
Error fetching blog post: FetchError: [GET] "https://multivendor-backend.indexo.ir/api/blog/posts/robots.txt/": 404 Not Found
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
    at async $fetch (file:///app/.output/server/chunks/nitro/nitro.mjs:1:45838)
    at async useApiFetch (file:///app/.output/server/chunks/build/server.mjs:1:36555)
    at async Proxy.fetchPost (file:///app/.output/server/chunks/build/blog-CUKJuic8.mjs:1:5038)
    at async fetchPage (file:///app/.output/server/chunks/build/_slug_-DmpVzigs.mjs:1:10225)
    at async setup (file:///app/.output/server/chunks/build/_slug_-DmpVzigs.mjs:1:10438)
```

### Files Involved
- `multivendor_platform/front_end/nuxt/pages/index.vue` - Categories fetch
- `multivendor_platform/front_end/nuxt/pages/blog/[slug].vue` - Blog post fetch
- `multivendor_platform/front_end/nuxt/composables/useApiFetch.ts` - API fetch utility

---

**Report Generated:** December 31, 2025  
**Investigator:** AI Assistant  
**No changes made to production system**


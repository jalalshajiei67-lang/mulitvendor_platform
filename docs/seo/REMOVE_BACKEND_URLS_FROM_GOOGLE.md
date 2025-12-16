# Remove Backend URLs from Google Search Index

## Problem
Google has indexed backend API domain URLs that should not be publicly accessible:
- `https://multivendor-backend.indexo.ir/products/8`
- `https://multivendor-backend.indexo.ir/subcategories/fabric-roll-slitting-machine`
- `https://multivendor-backend.indexo.ir/categories/insulation-construction-machinery`
- And other similar URLs

## Solution Implemented

### 1. Robots.txt Blocking ✅
- Backend domains now return `Disallow: /` in robots.txt
- This prevents future crawling

### 2. X-Robots-Tag Header ✅
- All responses from backend domains now include `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet`
- This tells search engines not to index these pages

### 3. 301 Redirects ✅
- Backend product/category URLs now redirect (301) to frontend
- This signals to Google that content has moved permanently

## Steps to Remove from Google Search Console

### Step 1: Access Google Search Console
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Select your property: `https://multivendor-backend.indexo.ir` (or add it if not verified)

### Step 2: Request URL Removal (Quick Method)

#### Option A: Remove Individual URLs
1. Go to **Removals** in the left sidebar
2. Click **New Request**
3. Enter each URL you want to remove:
   ```
   https://multivendor-backend.indexo.ir/products/8
   https://multivendor-backend.indexo.ir/products/12
   https://multivendor-backend.indexo.ir/products/26
   https://multivendor-backend.indexo.ir/products/16
   https://multivendor-backend.indexo.ir/products/13
   https://multivendor-backend.indexo.ir/subcategories/fabric-roll-slitting-machine
   https://multivendor-backend.indexo.ir/subcategories/fabric-bleaching-machine
   https://multivendor-backend.indexo.ir/subcategories/leather-embroidery-machine
   https://multivendor-backend.indexo.ir/subcategories/polyurethane-insulation-machine
   https://multivendor-backend.indexo.ir/categories/insulation-construction-machinery
   ```
4. Select **Temporarily hide from Google Search**
5. Click **Submit**

#### Option B: Remove All Backend URLs (Recommended)
1. Go to **Removals** → **New Request**
2. Enter URL pattern:
   ```
   https://multivendor-backend.indexo.ir/products/*
   https://multivendor-backend.indexo.ir/subcategories/*
   https://multivendor-backend.indexo.ir/categories/*
   https://multivendor-backend.indexo.ir/departments/*
   ```
3. Select **Temporarily hide from Google Search**
4. Click **Submit**

### Step 3: Verify robots.txt is Working
1. Go to **Settings** → **robots.txt Tester**
2. Test URL: `https://multivendor-backend.indexo.ir/robots.txt`
3. Verify it shows: `Disallow: /`

### Step 4: Monitor Removal Status
1. Go to **Removals** tab
2. Check status of your removal requests
3. Removals are temporary (90 days) - after that, Google will respect robots.txt

### Step 5: Submit Updated Sitemap (Optional)
1. Go to **Sitemaps**
2. Submit your frontend sitemap: `https://indexo.ir/sitemap.xml`
3. This helps Google discover the correct URLs

## Long-term Solution

### What We've Implemented:
1. ✅ **robots.txt** blocks all backend domains
2. ✅ **X-Robots-Tag header** prevents indexing
3. ✅ **301 redirects** move traffic to frontend
4. ✅ **Middleware** automatically adds noindex to all backend responses

### Expected Results:
- **Immediate**: New crawls will see robots.txt and noindex headers
- **Within 1-2 weeks**: Google will process removal requests
- **Within 1-3 months**: Backend URLs will be removed from search results
- **Ongoing**: Redirects will help Google update indexed URLs to frontend

## Testing

### Test robots.txt:
```bash
curl https://multivendor-backend.indexo.ir/robots.txt
```
Should return: `Disallow: /`

### Test X-Robots-Tag header:
```bash
curl -I https://multivendor-backend.indexo.ir/products/8
```
Should include: `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet`

### Test redirect:
```bash
curl -I https://multivendor-backend.indexo.ir/products/8
```
Should return: `301 Moved Permanently` with `Location: https://indexo.ir/products/8`

## Notes

- **Removal requests are temporary** (90 days)
- After 90 days, Google will rely on robots.txt and noindex headers
- **301 redirects are permanent** and help with SEO
- Backend domain should ideally not be publicly accessible (only via API)

## Additional Recommendations

1. **Block backend domain in nginx** (if possible):
   - Only allow `/api/`, `/admin/`, `/robots.txt`, `/sitemap.xml`
   - Block all other paths

2. **Use IP whitelisting** for admin panel:
   - Restrict `/admin/` to specific IPs

3. **Monitor Search Console** regularly:
   - Check for new backend URLs being indexed
   - Submit removal requests as needed


# WordPress Scraper Improvements

## Overview
Enhanced the universal scraper to better handle WordPress websites, especially those built with page builders (Elementor, Divi, Beaver Builder, etc.) and custom themes.

## Key Improvements

### 1. **WordPress Platform Detection**
- Now specifically detects WordPress sites (not just WooCommerce)
- Detects page builders: Elementor, Divi, Beaver Builder, Visual Composer, SiteOrigin
- Checks for WordPress indicators: `wp-content`, `/wp-includes/`, WordPress meta generator tag

### 2. **Enhanced Main Content Extraction**
The `_find_main_content()` method now:
- ✅ **Excludes header, footer, navigation, and sidebars** - Automatically removes these sections
- ✅ **Looks for common WordPress containers**:
  - `<article>`, `<main>`, `[role="main"]`
  - `.entry-content`, `.content-area`, `.site-main`
  - Page builder containers (`.elementor-element`, `.et_pb_section`, etc.)
- ✅ **Smart content detection** - Finds the largest meaningful content block
- ✅ **Filters navigation-like content** - Skips divs with too many links (menu indicators)

### 3. **Improved Title Extraction**
For WordPress pages, now checks:
1. Schema.org structured data
2. Open Graph meta tags
3. **Title tag** (checked early for WordPress pages)
4. H1 tags with WordPress-specific selectors:
   - `h1.entry-title`, `h1.page-title`
   - `article h1`, `.entry-header h1`
   - Page builder selectors: `[class*="elementor"] h1`
- **Cleans up title** - Removes site name, separators (|, -, –, —)

### 4. **Comprehensive Image Extraction**
For WordPress pages, now:
- ✅ Extracts **ALL images from main content area**
- ✅ Excludes images from header/footer/navigation
- ✅ Handles lazy-loading images (`data-src`, `data-lazy-src`, `data-large_image`)
- ✅ Filters out placeholders and tiny icons (< 50px)
- ✅ Supports up to 20 product images

### 5. **Better Price Extraction**
WordPress-specific price selectors including:
- `.price`, `span.price`, `.product-price`
- `[itemprop="price"]`
- Persian/Farsi selectors: `[class*="قیمت"]`, `[class*="مبلغ"]`

### 6. **Enhanced Description Extraction**
For WordPress pages:
- ✅ Uses WordPress-specific selectors:
  - `article .entry-content`, `.entry-content`, `.post-content`
  - Page builder selectors (Elementor, Divi)
- ✅ **Always tries to find main content** - Ensures we get the full page content
- ✅ **Excludes header/footer/nav content** - Only extracts main content area

## Testing

A new test script has been created:
```bash
python multivendor_platform/multivendor_platform/products/test_wordpress_scraper.py
```

This tests the specific URL: `https://danacodenegar.com/product/cij-dcnlt860/`

## What Gets Extracted

For WordPress pages (including page builders), the scraper now extracts:

1. **Title**: From title tag or H1 elements
2. **Main Content**: All content excluding header, footer, navbars
3. **Price**: From various price selectors
4. **All Product Images**: All images from main content area (excluding header/footer/nav icons)

## Usage

```python
from products.universal_scraper import UniversalProductScraper

# For WordPress sites
scraper = UniversalProductScraper(
    url="https://danacodenegar.com/product/cij-dcnlt860/",
    verify_ssl=False,  # Some sites have SSL issues
    use_proxy=False    # Bypass proxy for direct connections
)

data = scraper.scrape()

print(f"Product: {data['name']}")
print(f"Description: {data['description'][:200]}...")
print(f"Price: {data['price']}")
print(f"Images: {len(data['images'])} found")
```

## Files Modified

- ✅ `multivendor_platform/multivendor_platform/products/universal_scraper.py` - Enhanced scraper
- ✅ `multivendor_platform/multivendor_platform/products/test_wordpress_scraper.py` - New test script

## Next Steps

1. Test the scraper on the provided URL
2. Verify it extracts title, main content, price, and all images correctly
3. Test on other WordPress pages to ensure universal compatibility


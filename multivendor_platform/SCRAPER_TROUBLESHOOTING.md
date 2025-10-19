# 🔧 Scraper Troubleshooting Guide

## How to View Error Details

### Method 1: In the Scrape Jobs List (NOW IMPROVED!)
1. Go to: **Django Admin → Products → Product Scrape Jobs**
2. Look at the **Status** column
3. **Failed jobs now show the error message directly in the list!**
   - Red "FAILED" text
   - Error message displayed below the status
   - Hover over status to see full error message

### Method 2: Click on the Job
1. Click on the **Job ID** number
2. Scroll to the **"Results"** section
3. Read the **Error message** field
4. Check the **Scraped data** section to see what was extracted before failure

###Method 3: Using Debug Script
```bash
cd multivendor_platform
python debug_scraper.py
```
Select option 3 to see all failed jobs with details.

---

## Common Errors & Solutions

### 1. "HTTP Error 403: Forbidden"
**Problem**: Website is blocking the scraper  
**Solution**:
- The website has anti-bot protection
- Try accessing the URL in your browser first
- Some websites don't allow scraping
- Consider contacting the website owner for permission

### 2. "Connection Error: Could not connect"
**Problem**: Network or DNS issues  
**Solution**:
- Check your internet connection
- Try opening the URL in your browser
- Check if the website is down
- Try again later

### 3. "Timeout Error: Website took too long"
**Problem**: Website is slow or unresponsive  
**Solution**:
- Try again later when the website is faster
- Check if the website works in your browser
- The scraper waits 30 seconds before timing out

### 4. "Failed to fetch page: SSL Error"
**Problem**: SSL/HTTPS certificate issues  
**Solution**:
- The website may have an invalid SSL certificate
- Try the HTTP version instead of HTTPS (if available)
- Contact website administrator

### 5. Price is 0.00 or Missing Data
**Problem**: Page structure doesn't match expected selectors  
**Solution**:
- This is not an error - the scraper continues anyway
- **Products are created as drafts for manual review**
- Check the scraped data JSON to see what was found
- Manually add missing information in the product edit page
- Some product pages don't list prices (e.g., "contact for price")

### 6. "No module named 'bs4'" or "No module named 'requests'"
**Problem**: Missing Python packages  
**Solution**:
```bash
cd multivendor_platform
pip install beautifulsoup4 requests lxml
```

---

## Testing Specific URLs

### Before Bulk Scraping
Always test individual URLs first!

**Option 1: Use Test Script**
```bash
cd multivendor_platform
python test_specific_url.py
```

**Option 2: Use Debug Script**
```bash
python debug_scraper.py
# Select option 2: Test URL scraping
```

**Option 3: Manual Single URL Test**
1. Go to Bulk Scrape form
2. Enter just ONE URL
3. Click Start Scraping
4. Check the results immediately

---

## Special Cases

### Persian/Farsi Websites (like dmabna.com)
✅ **Now Supported!**
- Scraper handles Persian/Farsi encoding properly
- Characters display correctly
- No encoding issues

**Example**: https://dmabna.com/product/...
- Product names in Persian are supported
- Descriptions in Persian are supported
- Images and structure detection works

### Pages Without Prices
✅ **Handled Gracefully!**
- If no price is found, defaults to 0.00
- Product is still created
- You can manually add the price later
- Common for "Contact us for price" products

### Pages With Multiple Images
✅ **Up to 20 images!**
- First image becomes primary image
- All gallery images are downloaded
- Images are saved to your media folder
- Check the Product Images section in admin

---

## Debugging Workflow

### Step 1: Identify the Error
1. Go to Product Scrape Jobs
2. Find the failed job
3. Read the error message (now visible in list!)
4. Or click on the job to see full details

### Step 2: Test the URL
```bash
python test_specific_url.py
# Enter the failing URL
```

This will show you:
- ✓ What data was successfully extracted
- ❌ What failed and why
- Full error traceback for debugging

### Step 3: Common Fixes

**If it's a connection/network error:**
- Wait and retry later
- Check if website works in browser

**If data is missing:**
- Check the scraped JSON data
- Manually add missing information
- Products are drafts, so you can edit before publishing

**If it's a structure mismatch:**
- The website might not be WordPress/WooCommerce
- Contact us to add support for that platform
- Manually create the product instead

### Step 4: Retry or Manual Creation
- Use the "Retry failed jobs" action in admin
- Or manually create the product using scraped data as reference
- The source URL is always saved for your reference

---

## Best Practices

### ✅ Do's
- **Always test 1-2 URLs first** before bulk scraping
- **Check error messages** before retrying
- **Review all scraped products** before publishing
- **Start with known WordPress/WooCommerce sites**
- **Keep source URLs** for reference
- **Use the debug tools** provided

### ❌ Don'ts
- Don't scrape 100s of URLs without testing first
- Don't ignore error messages
- Don't publish scraped products without review
- Don't scrape sites without permission
- Don't expect 100% accuracy - always review!

---

## Understanding the Scraping Process

### What Happens When You Scrape:

1. **Job Created** (Status: Pending)
   - URL is saved
   - Queued for processing

2. **Processing Starts** (Status: Processing)
   - Page is downloaded
   - HTML is parsed
   - Data is extracted
   - Images are downloaded

3. **Product Created** (Status: Completed)
   - Product model is created
   - Set as inactive/draft
   - Images are saved
   - Link to product is shown

4. **Or Error Occurs** (Status: Failed)
   - Error message is saved
   - Partial data may be in scraped_data JSON
   - Can be retried
   - Can use data for manual creation

---

## Getting Help

### If You're Stuck:

1. **Check this guide** - most issues are covered here
2. **Use the debug script** - `python debug_scraper.py`
3. **View the error message** - check the job details
4. **Test individual URLs** - use test scripts
5. **Check scraped data JSON** - see what was actually extracted

### Information to Provide When Reporting Issues:
- The URL you're trying to scrape
- The complete error message
- The scraped data JSON (if available)
- Screenshots of the error
- Whether the URL works in your browser

---

## Quick Reference Commands

```bash
# Test a specific URL
python test_specific_url.py

# Interactive debugger
python debug_scraper.py

# Install/reinstall dependencies
pip install beautifulsoup4 requests lxml

# Run migrations (if needed)
python manage.py migrate

# Check for errors in code
python manage.py check
```

---

## Supported Websites

### ✅ Best Support
- WordPress with WooCommerce
- Standard WordPress product pages
- Persian/Farsi WordPress sites (like dmabna.com)

### ⚠️ Partial Support
- Custom WordPress themes (may need adjustments)
- Non-WordPress sites with similar structure

### ❌ Not Supported Yet
- Shopify (planned for future)
- Magento (planned for future)
- Custom e-commerce platforms
- Sites with heavy JavaScript rendering

---

## Update: Improvements Made

### Latest Changes:
✅ **Better error messages** - now shown directly in list view  
✅ **Persian/Farsi support** - proper encoding handling  
✅ **Graceful handling of missing prices** - no longer fails  
✅ **More detailed error reporting** - see exactly what went wrong  
✅ **Better HTTP error handling** - clearer messages for 403, 404, etc.  
✅ **Improved timeout handling** - 30 second limit with clear message  

### What's Been Fixed:
- Error messages now visible in admin list
- Persian/Farsi text displays correctly
- Missing prices don't cause failures
- Better connection error messages
- Improved encoding detection

---

**Remember**: The scraper creates products as **DRAFTS** for a reason - always review before publishing!


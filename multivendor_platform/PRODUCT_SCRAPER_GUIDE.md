# Product Scraper Guide

## Overview
The Product Scraper feature allows you to automatically extract product information from WordPress/WooCommerce websites and create products in your multivendor platform.

## Features
- ✅ **Bulk URL Processing**: Add multiple product URLs at once
- ✅ **Queue System**: Jobs are processed in the background
- ✅ **WordPress/WooCommerce Support**: Optimized for WordPress-based e-commerce sites
- ✅ **Automatic Data Extraction**: Scrapes product name, description, price, images, and categories
- ✅ **Image Download**: Automatically downloads and saves product images
- ✅ **Job Tracking**: Monitor scraping progress and view detailed results
- ✅ **Error Handling**: Failed jobs can be retried with one click
- ✅ **Draft Mode**: Scraped products are created as drafts for review before publishing

## How to Use

### 1. Access the Scraper

1. Log in to Django admin: http://127.0.0.1:8000/admin/
2. Navigate to **Products** section
3. Click on **Product Scrape Jobs**
4. Click the **"🔍 Bulk Scrape Products"** button at the top

### 2. Add Product URLs

1. In the bulk scraper form, paste product URLs (one per line)
   ```
   https://example.com/product/item-1
   https://example.com/product/item-2
   https://example.com/product/item-3
   ```

2. (Optional) Select a supplier/company for all products

3. Click **"🚀 Start Scraping"**

### 3. Monitor Progress

1. You'll be redirected to the **Product Scrape Jobs** list
2. Each job shows:
   - **Status**: Pending → Processing → Completed/Failed
   - **URL**: Link to the source product page
   - **Vendor**: User who created the job
   - **Created Product**: Link to the created product (when completed)
   - **Timestamps**: When the job was created and processed

### 4. Review Created Products

1. Click on the created product link in the scrape job list
2. Review the scraped data:
   - Product name (auto-generated slug)
   - Description (HTML formatted)
   - Price
   - Images (first image set as primary)
   - Categories (stored in scraped data)

3. **Important**: Products are created as **drafts** (inactive)
   - Manually assign categories/subcategories
   - Verify pricing and descriptions
   - Add stock quantity
   - Set product as active when ready to publish

## What Data is Scraped?

The scraper extracts the following information:

| Field | Description | Notes |
|-------|-------------|-------|
| **Name** | Product title/name | Required |
| **Description** | Full product description with HTML | Long description preferred, falls back to short |
| **Price** | Product price | Extracted from various selectors, defaults to 0.00 |
| **Images** | Main image + gallery images | Up to 20 images, first is set as primary |
| **Categories** | Product categories/tags | Stored in scraped data JSON for manual assignment |
| **Source URL** | Original product page URL | Saved in scraped data for reference |

## Supported Selectors

The scraper is optimized for WordPress/WooCommerce with support for:

### Product Title
- `h1.product_title`
- `h1.entry-title`
- `h1[itemprop="name"]`
- Generic `h1` tags

### Description
- `.woocommerce-product-details__short-description`
- `#tab-description`
- `.product-description`
- `div[itemprop="description"]`

### Price
- `p.price .woocommerce-Price-amount`
- `.price .amount`
- `span[itemprop="price"]`

### Images
- `.woocommerce-product-gallery__image img`
- `.product-images img`
- `img.wp-post-image`
- `img[itemprop="image"]`

### Categories
- `.posted_in a`
- `.product_meta a[rel="tag"]`
- `.product-categories a`

## Managing Scrape Jobs

### View Job Details
Click on any job ID to see:
- Complete scraped data in JSON format
- Error messages (if failed)
- Related product information
- Timestamps

### Retry Failed Jobs
1. Select failed jobs using checkboxes
2. Choose **"Retry failed jobs"** from the Actions dropdown
3. Click **"Go"**
4. Jobs will be re-queued for processing

### Process Pending Jobs
If jobs are stuck in pending status:
1. Select the jobs
2. Choose **"Process pending jobs"** from Actions
3. Click **"Go"**

## Tips & Best Practices

### ✅ Do's
- ✅ Test with 1-2 URLs first before bulk scraping
- ✅ Review scraped products before publishing
- ✅ Manually assign proper categories/subcategories
- ✅ Verify and adjust pricing
- ✅ Add stock quantities
- ✅ Enhance descriptions with your own content
- ✅ Add SEO meta data (title, description)

### ❌ Don'ts
- ❌ Don't scrape copyrighted content without permission
- ❌ Don't scrape too many URLs at once (start small)
- ❌ Don't publish scraped products without review
- ❌ Don't rely solely on scraped descriptions
- ❌ Don't forget to check image quality

## Troubleshooting

### Job Stuck in "Pending"
- Use the "Process pending jobs" action
- Check server logs for errors
- Verify the source website is accessible

### Job Failed
- Click on the job to view error message
- Common issues:
  - Invalid URL
  - Website blocking scraper (403/401 errors)
  - Page structure not matching selectors
  - Network timeout
- Use "Retry failed jobs" after fixing the issue

### Missing Data
If some data wasn't scraped:
- View the scraped data JSON in job details
- Manually add missing information to the product
- The source URL is saved for reference

### Images Not Downloading
- Check image URLs in scraped data
- Verify images are publicly accessible
- Some sites may block image downloads
- Manually upload images if needed

## Technical Details

### Background Processing
- Jobs are processed in background threads
- Multiple jobs can be processed simultaneously
- No impact on admin UI responsiveness

### Database Schema
The `ProductScrapeJob` model stores:
- `url`: Source product URL
- `vendor`: User who created the job
- `supplier`: Optional supplier assignment
- `status`: pending/processing/completed/failed
- `scraped_data`: JSON with all extracted data
- `created_product`: Link to created product
- `error_message`: Error details if failed
- `processed_at`: Processing timestamp

### Scraped Data JSON Structure
```json
{
  "name": "Product Name",
  "description": "<p>HTML description...</p>",
  "price": 29.99,
  "images": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ],
  "categories": ["Category 1", "Category 2"],
  "source_url": "https://example.com/product/item-1"
}
```

## Required Packages
The following Python packages are required (already installed):
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `lxml` - Fast HTML parser
- `Pillow` - Image processing

## Future Enhancements
Potential improvements:
- Support for more e-commerce platforms (Shopify, Magento)
- Advanced selector customization
- Automatic category mapping
- Scheduled scraping
- Celery integration for better queue management
- Duplicate detection
- Price tracking and updates

## Support
For issues or questions:
1. Check the error message in failed jobs
2. Review the scraped data JSON
3. Verify the source website structure
4. Test with a different product URL

---

**Note**: Always ensure you have permission to scrape content from websites. Respect robots.txt and terms of service.


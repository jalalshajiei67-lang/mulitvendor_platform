#!/usr/bin/env python
"""
Debug script for troubleshooting scraper issues
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from products.models import ProductScrapeJob
from products.scraper import WordPressScraper, create_product_from_scraped_data
from django.contrib.auth import get_user_model

User = get_user_model()

def show_recent_jobs():
    """Show the most recent scrape jobs"""
    print("=" * 80)
    print("RECENT SCRAPE JOBS")
    print("=" * 80)
    
    jobs = ProductScrapeJob.objects.all()[:10]
    
    if not jobs:
        print("\n❌ No scrape jobs found in database.")
        print("\nTo create a job, go to:")
        print("http://127.0.0.1:8000/admin/products/productscrapejob/bulk-scrape/")
        return
    
    for job in jobs:
        print(f"\nJob #{job.id}")
        print(f"URL: {job.url}")
        print(f"Status: {job.status}")
        print(f"Vendor: {job.vendor.username}")
        if job.status == 'failed':
            print(f"❌ Error: {job.error_message}")
        if job.created_product:
            print(f"✅ Created Product: {job.created_product.name} (ID: {job.created_product.id})")
        print("-" * 80)

def test_url_scraping():
    """Test scraping a specific URL"""
    print("\n" + "=" * 80)
    print("TEST URL SCRAPING")
    print("=" * 80)
    
    url = input("\nEnter a product URL to test: ").strip()
    
    if not url:
        print("No URL provided.")
        return
    
    try:
        print(f"\n📡 Fetching: {url}")
        scraper = WordPressScraper(url)
        
        print("   Downloading page...")
        scraper.fetch_page()
        print("   ✓ Page downloaded")
        
        print("\n🔍 Extracting data...")
        
        # Test each extraction method separately
        try:
            name = scraper.extract_product_name()
            print(f"   ✓ Name: {name}")
        except Exception as e:
            print(f"   ❌ Name extraction failed: {str(e)}")
            name = "Unknown"
        
        try:
            price = scraper.extract_price()
            print(f"   ✓ Price: ${price:.2f}")
        except Exception as e:
            print(f"   ❌ Price extraction failed: {str(e)}")
            price = 0.00
        
        try:
            description = scraper.extract_description()
            desc_preview = description[:100] + "..." if len(description) > 100 else description
            print(f"   ✓ Description: {desc_preview}")
        except Exception as e:
            print(f"   ❌ Description extraction failed: {str(e)}")
            description = ""
        
        try:
            images = scraper.extract_images()
            print(f"   ✓ Images: {len(images)} found")
            for i, img in enumerate(images[:3], 1):
                print(f"      {i}. {img[:60]}...")
        except Exception as e:
            print(f"   ❌ Image extraction failed: {str(e)}")
            images = []
        
        try:
            categories = scraper.extract_categories()
            print(f"   ✓ Categories: {', '.join(categories) if categories else 'None'}")
        except Exception as e:
            print(f"   ❌ Category extraction failed: {str(e)}")
            categories = []
        
        print("\n✅ Scraping test completed!")
        print("\nIf you see errors above, the website structure might not match our selectors.")
        print("You can still create the job - it will use default values for failed fields.")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print("\nPossible causes:")
        print("  • Invalid URL")
        print("  • Website is blocking the request (403/401 error)")
        print("  • Network/connection issues")
        print("  • Website doesn't exist or is down")
        import traceback
        print("\nFull error details:")
        traceback.print_exc()

def check_failed_jobs():
    """Check and display failed jobs with details"""
    print("\n" + "=" * 80)
    print("FAILED JOBS ANALYSIS")
    print("=" * 80)
    
    failed_jobs = ProductScrapeJob.objects.filter(status='failed')
    
    if not failed_jobs:
        print("\n✅ No failed jobs found!")
        return
    
    print(f"\nFound {failed_jobs.count()} failed job(s):\n")
    
    for job in failed_jobs:
        print(f"Job #{job.id}")
        print(f"URL: {job.url}")
        print(f"Created: {job.created_at}")
        print(f"Error: {job.error_message}")
        print(f"\nScraped Data:")
        if job.scraped_data:
            import json
            print(json.dumps(job.scraped_data, indent=2))
        else:
            print("  (No data scraped)")
        print("-" * 80)

def retry_failed_job():
    """Retry a specific failed job"""
    print("\n" + "=" * 80)
    print("RETRY FAILED JOB")
    print("=" * 80)
    
    failed_jobs = ProductScrapeJob.objects.filter(status='failed')
    
    if not failed_jobs:
        print("\n✅ No failed jobs to retry!")
        return
    
    print(f"\nFailed jobs:")
    for job in failed_jobs:
        print(f"  {job.id}. {job.url[:60]} - {job.error_message[:50]}")
    
    job_id = input("\nEnter job ID to retry (or press Enter to skip): ").strip()
    
    if not job_id:
        return
    
    try:
        job = ProductScrapeJob.objects.get(id=int(job_id))
        print(f"\nRetrying job #{job.id}: {job.url}")
        
        job.status = 'processing'
        job.error_message = None
        job.save()
        
        # Try scraping
        scraper = WordPressScraper(job.url)
        scraped_data = scraper.scrape()
        
        job.scraped_data = scraped_data
        job.save()
        
        # Try creating product
        product, error = create_product_from_scraped_data(
            scraped_data,
            vendor=job.vendor,
            supplier=job.supplier
        )
        
        if product:
            job.created_product = product
            job.status = 'completed'
            job.save()
            print(f"\n✅ Success! Product created: {product.name} (ID: {product.id})")
        else:
            job.status = 'failed'
            job.error_message = error
            job.save()
            print(f"\n❌ Failed to create product: {error}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Main menu"""
    while True:
        print("\n" + "=" * 80)
        print("SCRAPER DEBUGGER")
        print("=" * 80)
        print("\n1. Show recent scrape jobs")
        print("2. Test URL scraping (without creating job)")
        print("3. Check failed jobs")
        print("4. Retry a failed job")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            show_recent_jobs()
        elif choice == '2':
            test_url_scraping()
        elif choice == '3':
            check_failed_jobs()
        elif choice == '4':
            retry_failed_job()
        elif choice == '5':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option. Please select 1-5.")

if __name__ == '__main__':
    main()


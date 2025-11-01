"""
Test the Universal Scraper with WordPress pages (including page builders)
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from products.universal_scraper import UniversalProductScraper

# Test the specific WordPress URL provided by user
test_url = "https://danacodenegar.com/product/cij-dcnlt860/"

print("="*100)
print("WORDPRESS SCRAPER TEST")
print("="*100)
print(f"Testing URL: {test_url}\n")

try:
    # Try with SSL disabled and no proxy (common for some WordPress sites)
    scraper = UniversalProductScraper(test_url, verify_ssl=False, use_proxy=False)
    data = scraper.scrape()
    
    print(f"✅ SUCCESS!")
    print(f"\n{'='*100}")
    print("EXTRACTED DATA:")
    print(f"{'='*100}")
    print(f"Platform: {data.get('platform', 'unknown')}")
    print(f"\nProduct Name: {data['name']}")
    print(f"\nDescription Length: {len(data['description'])} characters")
    print(f"Price: {data['price']}")
    print(f"Images Found: {len(data['images'])}")
    print(f"Warnings: {data['scraping_metadata']['warnings_count']}")
    
    if data['description']:
        print(f"\n{'='*100}")
        print("DESCRIPTION PREVIEW (first 500 chars):")
        print(f"{'='*100}")
        print(data['description'][:500] + "..." if len(data['description']) > 500 else data['description'])
    
    if data['images']:
        print(f"\n{'='*100}")
        print("IMAGES FOUND:")
        print(f"{'='*100}")
        for i, img_url in enumerate(data['images'][:10], 1):  # Show first 10
            print(f"{i}. {img_url}")
        if len(data['images']) > 10:
            print(f"... and {len(data['images']) - 10} more images")
    
    if data['scraping_metadata']['warnings_count'] > 0:
        print(f"\n{'='*100}")
        print("WARNINGS:")
        print(f"{'='*100}")
        print(data['scraping_metadata']['summary'])
    
    print(f"\n{'='*100}")
    print("✅ Test completed successfully!")
    print(f"{'='*100}\n")
    
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    import traceback
    print("\nFull error traceback:")
    print(traceback.format_exc())


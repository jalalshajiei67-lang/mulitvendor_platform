"""
Test the Universal Scraper with the failed URLs
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from products.universal_scraper import UniversalProductScraper

# Test URLs that previously failed
test_urls = [
    "http://www.ebtekarehashemi.com/%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa/%d8%ae%d8%b1%d9%85%d9%86%da%a9%d9%88%d8%a8-%d8%a8%d9%88%d8%ac%d8%a7%d8%b1%db%8c/%d8%ae%d8%b1%d9%85%d9%86%da%a9%d9%88%d8%a8-%d8%a8%d9%88%d8%ac%d8%a7%d8%b1%db%8c-%d8%b7%d8%b1%d8%ad-%d8%b3%d9%88%d8%a7%d8%b1-%d8%a8%d8%af%d9%88%d9%86-%da%86%d8%b1%d8%ae.html",
    "https://fisheriestech.com/product/automatic-fish-sorting-machine/",
    "https://aracup.com/product/%d8%b1%d8%b3%d8%aa%d8%b1-%d9%82%d9%87%d9%88%d9%87-2-%da%a9%db%8c%d9%84%d9%88%db%8c%db%8c/",
    "https://sknmachinery.ir/index.php/complete-curd-production-line/",
    "https://www.amolboresh.com/products/%d8%af%d9%88%d8%b1%da%a9%d9%86/%d8%af%d9%88%d8%b1%da%a9%d9%86-%d9%85%d9%88%d9%84%d9%86/%d8%af%d9%88%d8%b1%da%a9%d9%86-ps102-2200-2/",
    "https://bestanano.com/product/nanobubble-device/",
    "https://www.polymeresabz.com/%d8%b4%d8%b1%db%8c%d8%af%d8%b1/",
    "https://taksamachine.com/product/%d8%a8%db%8c%d9%84%d8%b1-%d8%a8%d8%b3%d8%aa%d9%87-%d8%a8%d9%86%d8%af%db%8c-%d8%b9%d9%84%d9%88%d9%81%d9%87-%da%a9%d8%af-%d9%85%d8%ad%d8%b5%d9%88%d9%84-tk0001/",
    "https://turanmachine.com/product/%d8%af%d8%b3%d8%aa%da%af%d8%a7%d9%87-%d8%aa%d9%85%db%8c%d8%b2-%da%a9%d9%86-%d9%be%d8%a7%d9%88%d8%b1%d8%aa%da%a9/",
]

print("="*100)
print("UNIVERSAL SCRAPER TEST")
print("="*100)
print(f"Testing {len(test_urls)} previously failed URLs\n")

results = {
    'success': [],
    'failed': []
}

for i, url in enumerate(test_urls, 1):
    print(f"\n{'='*100}")
    print(f"TEST {i}/{len(test_urls)}")
    print(f"URL: {url}")
    print(f"{'='*100}")
    
    try:
        # Try with SSL disabled and no proxy (most common for Iranian sites)
        scraper = UniversalProductScraper(url, verify_ssl=False, use_proxy=False)
        data = scraper.scrape()
        
        # Show results
        print(f"✅ SUCCESS!")
        print(f"   Platform: {data.get('platform', 'unknown')}")
        print(f"   Product Name: {data['name'][:80]}...")
        print(f"   Description Length: {len(data['description'])} chars")
        print(f"   Price: {data['price']}")
        print(f"   Images Found: {len(data['images'])}")
        print(f"   Warnings: {data['scraping_metadata']['warnings_count']}")
        
        if data['images']:
            print(f"   First Image: {data['images'][0][:80]}...")
        
        results['success'].append({
            'url': url,
            'name': data['name'],
            'platform': data.get('platform'),
            'images': len(data['images'])
        })
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
        results['failed'].append({
            'url': url,
            'error': str(e)
        })

# Summary
print(f"\n\n{'='*100}")
print("SUMMARY")
print(f"{'='*100}")
print(f"✅ Successful: {len(results['success'])}/{len(test_urls)}")
print(f"❌ Failed: {len(results['failed'])}/{len(test_urls)}")
print(f"📊 Success Rate: {(len(results['success'])/len(test_urls)*100):.1f}%")

if results['success']:
    print(f"\n🎉 SUCCESSFUL SCRAPES:")
    for item in results['success']:
        print(f"   • {item['name'][:60]} ({item['platform']}) - {item['images']} images")

if results['failed']:
    print(f"\n💥 FAILED SCRAPES:")
    for item in results['failed']:
        print(f"   • {item['url'][:80]}")
        print(f"     Error: {item['error'][:100]}")

print(f"\n{'='*100}")
print("Test completed!")
print(f"{'='*100}\n")

# Save detailed results to file
output_file = os.path.join(os.path.dirname(__file__), 'scraper_test_results.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("UNIVERSAL SCRAPER TEST RESULTS\n")
    f.write("="*100 + "\n\n")
    f.write(f"Total URLs Tested: {len(test_urls)}\n")
    f.write(f"Successful: {len(results['success'])}\n")
    f.write(f"Failed: {len(results['failed'])}\n")
    f.write(f"Success Rate: {(len(results['success'])/len(test_urls)*100):.1f}%\n\n")
    
    f.write("SUCCESSFUL SCRAPES:\n")
    f.write("-"*100 + "\n")
    for item in results['success']:
        f.write(f"\nURL: {item['url']}\n")
        f.write(f"Name: {item['name']}\n")
        f.write(f"Platform: {item['platform']}\n")
        f.write(f"Images: {item['images']}\n")
    
    f.write("\n\nFAILED SCRAPES:\n")
    f.write("-"*100 + "\n")
    for item in results['failed']:
        f.write(f"\nURL: {item['url']}\n")
        f.write(f"Error: {item['error']}\n")

print(f"✅ Detailed results saved to: {output_file}\n")


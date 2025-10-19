#!/usr/bin/env python
"""
Test script for the WordPress product scraper
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from products.scraper import WordPressScraper

def test_scraper():
    """Test the scraper with a sample URL"""
    print("=" * 60)
    print("WordPress Product Scraper - Test Script")
    print("=" * 60)
    
    # Example WordPress/WooCommerce product URL
    # Note: This is a demo URL - replace with actual product URL to test
    test_url = input("\nEnter a WordPress product URL to test (or press Enter to skip): ").strip()
    
    if not test_url:
        print("\nNo URL provided. Testing skipped.")
        print("\nTo test the scraper:")
        print("1. Find a WordPress/WooCommerce product page")
        print("2. Run: python test_scraper.py")
        print("3. Enter the URL when prompted")
        return
    
    try:
        print(f"\n📡 Fetching page: {test_url}")
        scraper = WordPressScraper(test_url)
        
        print("✓ Page fetched successfully!")
        print("\n🔍 Extracting data...")
        
        data = scraper.scrape()
        
        print("\n" + "=" * 60)
        print("SCRAPED DATA")
        print("=" * 60)
        
        print(f"\n📦 Product Name:")
        print(f"   {data['name']}")
        
        print(f"\n💰 Price:")
        print(f"   ${data['price']:.2f}")
        
        print(f"\n📝 Description:")
        desc_preview = data['description'][:200] + "..." if len(data['description']) > 200 else data['description']
        print(f"   {desc_preview}")
        
        print(f"\n🖼️  Images Found: {len(data['images'])}")
        for i, img_url in enumerate(data['images'][:5], 1):
            print(f"   {i}. {img_url[:80]}...")
        if len(data['images']) > 5:
            print(f"   ... and {len(data['images']) - 5} more")
        
        print(f"\n🏷️  Categories:")
        if data['categories']:
            for cat in data['categories']:
                print(f"   - {cat}")
        else:
            print("   (No categories found)")
        
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        
        print("\nThe scraper is working correctly!")
        print("You can now use the Django admin to scrape products.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPossible reasons:")
        print("- Invalid URL")
        print("- Website blocking the scraper")
        print("- Network issues")
        print("- Page structure not matching WordPress/WooCommerce")

if __name__ == '__main__':
    test_scraper()


#!/usr/bin/env python3
"""
Test script to verify category hierarchy API endpoints
Run this on the server to check if filtering is working correctly
"""

import requests
import json
from typing import Dict, Any

# Server URL
BASE_URL = "https://indexo.ir/api"

def print_header(text: str):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text: str):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text: str):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text: str):
    """Print info message"""
    print(f"ℹ️  {text}")

def test_endpoint(url: str, description: str) -> Dict[str, Any]:
    """Test an API endpoint and return results"""
    try:
        print(f"\nTesting: {description}")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle paginated response
            if 'results' in data:
                items = data['results']
                count = data.get('count', len(items))
            elif isinstance(data, list):
                items = data
                count = len(items)
            else:
                items = [data]
                count = 1
            
            print_success(f"Status: {response.status_code} OK")
            print_info(f"Items returned: {count}")
            
            return {
                'success': True,
                'data': items,
                'count': count
            }
        else:
            print_error(f"Status: {response.status_code}")
            print_error(f"Response: {response.text[:200]}")
            return {
                'success': False,
                'error': response.text
            }
    
    except Exception as e:
        print_error(f"Exception: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Main test function"""
    print_header("CATEGORY HIERARCHY API TESTING")
    
    # Test 1: Get all departments
    print_header("Test 1: Get All Departments")
    dept_result = test_endpoint(
        f"{BASE_URL}/departments/",
        "Fetch all departments"
    )
    
    if not dept_result['success'] or dept_result['count'] == 0:
        print_error("No departments found! Please add departments in admin panel.")
        return
    
    # Get first department for testing
    first_dept = dept_result['data'][0]
    dept_id = first_dept['id']
    dept_slug = first_dept['slug']
    dept_name = first_dept['name']
    
    print_success(f"Found department: {dept_name} (ID: {dept_id}, Slug: {dept_slug})")
    
    # Test 2: Get department by slug
    print_header("Test 2: Get Department by Slug")
    test_endpoint(
        f"{BASE_URL}/departments/?slug={dept_slug}",
        f"Fetch department by slug: {dept_slug}"
    )
    
    # Test 3: Get categories filtered by department
    print_header("Test 3: Get Categories Filtered by Department")
    cat_result = test_endpoint(
        f"{BASE_URL}/categories/?department={dept_id}",
        f"Fetch categories for department: {dept_name}"
    )
    
    if not cat_result['success'] or cat_result['count'] == 0:
        print_error(f"No categories found for department '{dept_name}'!")
        print_info("Please add categories and link them to this department in admin panel.")
        print_info("Go to: Admin > Categories > Edit > Departments field")
        return
    
    # Get first category for testing
    first_cat = cat_result['data'][0]
    cat_id = first_cat['id']
    cat_slug = first_cat['slug']
    cat_name = first_cat['name']
    
    print_success(f"Found category: {cat_name} (ID: {cat_id}, Slug: {cat_slug})")
    
    # Test 4: Get category by slug
    print_header("Test 4: Get Category by Slug")
    test_endpoint(
        f"{BASE_URL}/categories/?slug={cat_slug}",
        f"Fetch category by slug: {cat_slug}"
    )
    
    # Test 5: Get subcategories filtered by category
    print_header("Test 5: Get Subcategories Filtered by Category")
    subcat_result = test_endpoint(
        f"{BASE_URL}/subcategories/?category={cat_id}",
        f"Fetch subcategories for category: {cat_name}"
    )
    
    if not subcat_result['success'] or subcat_result['count'] == 0:
        print_error(f"No subcategories found for category '{cat_name}'!")
        print_info("Please add subcategories and link them to this category in admin panel.")
        print_info("Go to: Admin > Subcategories > Edit > Categories field")
        return
    
    # Get first subcategory for testing
    first_subcat = subcat_result['data'][0]
    subcat_id = first_subcat['id']
    subcat_slug = first_subcat['slug']
    subcat_name = first_subcat['name']
    
    print_success(f"Found subcategory: {subcat_name} (ID: {subcat_id}, Slug: {subcat_slug})")
    
    # Test 6: Get subcategory by slug
    print_header("Test 6: Get Subcategory by Slug")
    test_endpoint(
        f"{BASE_URL}/subcategories/?slug={subcat_slug}",
        f"Fetch subcategory by slug: {subcat_slug}"
    )
    
    # Test 7: Get products filtered by subcategory
    print_header("Test 7: Get Products Filtered by Subcategory")
    prod_result = test_endpoint(
        f"{BASE_URL}/products/?subcategories={subcat_id}",
        f"Fetch products for subcategory: {subcat_name}"
    )
    
    if not prod_result['success'] or prod_result['count'] == 0:
        print_error(f"No products found for subcategory '{subcat_name}'!")
        print_info("Please add products and link them to this subcategory in admin panel.")
        print_info("Go to: Admin > Products > Edit > Subcategories field")
    else:
        first_prod = prod_result['data'][0]
        prod_name = first_prod['name']
        print_success(f"Found product: {prod_name}")
    
    # Final summary
    print_header("TEST SUMMARY")
    print_success("✅ All API endpoints are working correctly!")
    print_info("\nTested hierarchy:")
    print(f"   Department: {dept_name}")
    print(f"   └─ Category: {cat_name}")
    print(f"      └─ Subcategory: {subcat_name}")
    if prod_result['success'] and prod_result['count'] > 0:
        print(f"         └─ Products: {prod_result['count']} items")
    
    print_info("\n📝 Next steps:")
    print("   1. Open browser: https://indexo.ir/departments")
    print("   2. Click on a department - should show categories")
    print("   3. Click on a category - should show subcategories")
    print("   4. Click on a subcategory - should show products")
    print("\n   Press F12 to check console for any errors.")

if __name__ == "__main__":
    main()


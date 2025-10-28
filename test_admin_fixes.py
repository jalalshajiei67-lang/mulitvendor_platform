#!/usr/bin/env python
"""
Test script to verify Django admin fixes are working
Tests all the custom display methods that were fixed
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'multivendor_platform', 'multivendor_platform'))
django.setup()

from django.contrib.admin.sites import site
from products.models import Product, Department, Category, Subcategory
from products.admin import ProductAdmin, SubcategoryAdmin, CategoryAdmin

def test_product_admin_methods():
    """Test all ProductAdmin list_display methods"""
    print("\n" + "="*70)
    print("🧪 TESTING PRODUCT ADMIN METHODS")
    print("="*70)
    
    products = Product.objects.all()[:3]
    if not products:
        print("  ⚠️  No products in database to test")
        return False
    
    admin = ProductAdmin(Product, site)
    all_passed = True
    
    for product in products:
        print(f"\n📦 Testing Product: {product.name} (ID: {product.id})")
        
        # Test get_subcategories
        try:
            result = admin.get_subcategories(product)
            print(f"  ✅ get_subcategories(): {result}")
        except Exception as e:
            print(f"  ❌ get_subcategories() FAILED: {e}")
            all_passed = False
        
        # Test get_category_path
        try:
            result = admin.get_category_path(product)
            print(f"  ✅ get_category_path(): {result}")
        except Exception as e:
            print(f"  ❌ get_category_path() FAILED: {e}")
            all_passed = False
        
        # Test image_count
        try:
            result = admin.image_count(product)
            # Strip HTML for display
            import re
            clean_result = re.sub('<[^<]+?>', '', str(result))
            print(f"  ✅ image_count(): {clean_result}")
        except Exception as e:
            print(f"  ❌ image_count() FAILED: {e}")
            all_passed = False
        
        # Test comment_count
        try:
            result = admin.comment_count(product)
            clean_result = re.sub('<[^<]+?>', '', str(result))
            print(f"  ✅ comment_count(): {clean_result}")
        except Exception as e:
            print(f"  ❌ comment_count() FAILED: {e}")
            all_passed = False
    
    return all_passed

def test_subcategory_admin_methods():
    """Test all SubcategoryAdmin list_display methods"""
    print("\n" + "="*70)
    print("🧪 TESTING SUBCATEGORY ADMIN METHODS")
    print("="*70)
    
    subcategories = Subcategory.objects.all()[:2]
    if not subcategories:
        print("  ⚠️  No subcategories in database to test")
        return False
    
    admin = SubcategoryAdmin(Subcategory, site)
    all_passed = True
    
    for subcat in subcategories:
        print(f"\n📂 Testing Subcategory: {subcat.name} (ID: {subcat.id})")
        
        # Test get_departments
        try:
            result = admin.get_departments(subcat)
            print(f"  ✅ get_departments(): {result}")
        except Exception as e:
            print(f"  ❌ get_departments() FAILED: {e}")
            all_passed = False
        
        # Test get_categories
        try:
            result = admin.get_categories(subcat)
            print(f"  ✅ get_categories(): {result}")
        except Exception as e:
            print(f"  ❌ get_categories() FAILED: {e}")
            all_passed = False
    
    return all_passed

def test_category_admin_methods():
    """Test all CategoryAdmin list_display methods"""
    print("\n" + "="*70)
    print("🧪 TESTING CATEGORY ADMIN METHODS")
    print("="*70)
    
    categories = Category.objects.all()[:2]
    if not categories:
        print("  ⚠️  No categories in database to test")
        return False
    
    admin = CategoryAdmin(Category, site)
    all_passed = True
    
    for cat in categories:
        print(f"\n📁 Testing Category: {cat.name} (ID: {cat.id})")
        
        # Test get_departments
        try:
            result = admin.get_departments(cat)
            print(f"  ✅ get_departments(): {result}")
        except Exception as e:
            print(f"  ❌ get_departments() FAILED: {e}")
            all_passed = False
    
    return all_passed

def test_edge_cases():
    """Test edge cases with missing data"""
    print("\n" + "="*70)
    print("🧪 TESTING EDGE CASES (Missing Data Handling)")
    print("="*70)
    
    # Test product with no images
    print("\n📦 Testing products with no images...")
    products_no_images = Product.objects.filter(images__isnull=True).distinct()[:1]
    if products_no_images:
        admin = ProductAdmin(Product, site)
        for product in products_no_images:
            try:
                result = admin.image_count(product)
                import re
                clean_result = re.sub('<[^<]+?>', '', str(result))
                print(f"  ✅ Product '{product.name}' with no images: {clean_result}")
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
                return False
    else:
        print("  ℹ️  All products have images (no edge case to test)")
    
    # Test product with no subcategories
    print("\n📦 Testing products with no subcategories...")
    products_no_subcat = Product.objects.filter(subcategories__isnull=True).distinct()[:1]
    if products_no_subcat:
        admin = ProductAdmin(Product, site)
        for product in products_no_subcat:
            try:
                result = admin.get_subcategories(product)
                print(f"  ✅ Product '{product.name}' with no subcategories: {result}")
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
                return False
    else:
        print("  ℹ️  All products have subcategories (no edge case to test)")
    
    return True

def test_admin_registration():
    """Verify all models are registered"""
    print("\n" + "="*70)
    print("🧪 TESTING ADMIN REGISTRATION")
    print("="*70)
    
    expected_models = [
        'products.Department',
        'products.Category',
        'products.Subcategory',
        'products.Product',
        'products.ProductImage',
        'products.ProductComment',
        'products.ProductScrapeJob',
        'products.ScrapeJobBatch',
    ]
    
    registered_models = [model._meta.label for model in site._registry.keys()]
    
    all_registered = True
    for model_label in expected_models:
        if model_label in registered_models:
            print(f"  ✅ {model_label} is registered")
        else:
            print(f"  ❌ {model_label} is NOT registered")
            all_registered = False
    
    return all_registered

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🔬 DJANGO ADMIN FIXES - AUTOMATED TEST SUITE")
    print("="*70)
    print("\nThis script tests all the fixes applied to admin.py")
    print("It verifies that error handling works correctly.\n")
    
    results = {
        'Admin Registration': test_admin_registration(),
        'Product Admin Methods': test_product_admin_methods(),
        'Subcategory Admin Methods': test_subcategory_admin_methods(),
        'Category Admin Methods': test_category_admin_methods(),
        'Edge Cases': test_edge_cases(),
    }
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    print(f"\n  Total: {passed}/{total} test groups passed")
    
    if passed == total:
        print("\n  🎉 ALL TESTS PASSED! Admin fixes are working correctly.")
        return 0
    else:
        print(f"\n  ⚠️  {total - passed} test group(s) failed. Check output above.")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


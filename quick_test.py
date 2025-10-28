import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'multivendor_platform', 'multivendor_platform'))
django.setup()

from django.contrib.admin.sites import site
from products.models import Product
from products.admin import ProductAdmin

print("\n=== QUICK ADMIN TEST ===\n")

# Test with first product
product = Product.objects.first()
if not product:
    print("❌ No products in database")
    sys.exit(1)

print(f"Testing with: {product.name}\n")

admin = ProductAdmin(Product, site)

# Test each method
tests = [
    ('get_subcategories', lambda: admin.get_subcategories(product)),
    ('get_category_path', lambda: admin.get_category_path(product)),
    ('image_count', lambda: admin.image_count(product)),
    ('comment_count', lambda: admin.comment_count(product)),
]

passed = 0
for name, func in tests:
    try:
        result = func()
        print(f"✅ {name}(): OK")
        passed += 1
    except Exception as e:
        print(f"❌ {name}(): FAILED - {e}")

print(f"\n{passed}/{len(tests)} tests passed")
print("✅ All tests passed!" if passed == len(tests) else "⚠️  Some tests failed")


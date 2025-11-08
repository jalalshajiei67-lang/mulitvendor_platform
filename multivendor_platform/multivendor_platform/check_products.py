import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from products.models import Product

# Get all products
products = Product.objects.all()

print(f"\n{'='*80}")
print(f"TOTAL PRODUCTS IN DATABASE: {products.count()}")
print(f"{'='*80}\n")

for product in products:
    print(f"ID: {product.id}")
    print(f"Name: {product.name}")
    print(f"Slug: {product.slug}")
    print(f"is_active: {product.is_active}")
    print(f"primary_category: {product.primary_category}")
    print(f"subcategories: {', '.join([str(sc) for sc in product.subcategories.all()])}")
    print(f"vendor: {product.vendor}")
    print(f"supplier: {product.supplier}")
    print("-" * 80)

# Check how many are active
active_count = Product.objects.filter(is_active=True).count()
inactive_count = Product.objects.filter(is_active=False).count()

print(f"\n{'='*80}")
print(f"ACTIVE PRODUCTS: {active_count}")
print(f"INACTIVE PRODUCTS: {inactive_count}")
print(f"{'='*80}\n")


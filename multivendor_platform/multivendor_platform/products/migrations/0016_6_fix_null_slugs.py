# Generated manually to fix null slug values
# This migration ensures all categories have slugs before making them NOT NULL

from django.db import migrations
from django.utils.text import slugify


def generate_slugs_for_null_entries(apps, schema_editor):
    """Generate slugs for any entries that have null slugs"""
    
    Department = apps.get_model('products', 'Department')
    Category = apps.get_model('products', 'Category')
    Subcategory = apps.get_model('products', 'Subcategory')
    Product = apps.get_model('products', 'Product')
    
    # Fix Departments
    departments_updated = 0
    for dept in Department.objects.filter(slug__isnull=True) | Department.objects.filter(slug=''):
        base_slug = slugify(dept.name) if dept.name else f'department-{dept.id}'
        slug = base_slug
        counter = 1
        while Department.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        dept.slug = slug
        dept.save(update_fields=['slug'])
        departments_updated += 1
    
    # Fix Categories
    categories_updated = 0
    for cat in Category.objects.filter(slug__isnull=True) | Category.objects.filter(slug=''):
        base_slug = slugify(cat.name) if cat.name else f'category-{cat.id}'
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        cat.slug = slug
        cat.save(update_fields=['slug'])
        categories_updated += 1
    
    # Fix Subcategories
    subcategories_updated = 0
    for subcat in Subcategory.objects.filter(slug__isnull=True) | Subcategory.objects.filter(slug=''):
        base_slug = slugify(subcat.name) if subcat.name else f'subcategory-{subcat.id}'
        slug = base_slug
        counter = 1
        while Subcategory.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        subcat.slug = slug
        subcat.save(update_fields=['slug'])
        subcategories_updated += 1
    
    # Fix Products
    products_updated = 0
    for product in Product.objects.filter(slug__isnull=True) | Product.objects.filter(slug=''):
        base_slug = slugify(product.name) if product.name else f'product-{product.id}'
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        product.slug = slug
        product.save(update_fields=['slug'])
        products_updated += 1
    
    print(f"Fixed {departments_updated} Departments")
    print(f"Fixed {categories_updated} Categories")
    print(f"Fixed {subcategories_updated} Subcategories")
    print(f"Fixed {products_updated} Products")


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_5_populate_timestamps'),
    ]

    operations = [
        migrations.RunPython(generate_slugs_for_null_entries, migrations.RunPython.noop),
    ]



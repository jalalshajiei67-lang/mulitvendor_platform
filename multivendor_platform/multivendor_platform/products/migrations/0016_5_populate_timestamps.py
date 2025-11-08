# Generated manually on 2025-10-26
# This migration populates NULL timestamps and empty slugs before migration 0017

from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify


def populate_timestamps_and_slugs(apps, schema_editor):
    """
    Populate NULL created_at/updated_at fields and empty slugs
    This is required before migration 0017 which changes these fields to auto_now/auto_now_add
    """
    Department = apps.get_model('products', 'Department')
    Category = apps.get_model('products', 'Category')
    Subcategory = apps.get_model('products', 'Subcategory')
    Product = apps.get_model('products', 'Product')
    
    now = timezone.now()
    
    # Populate NULL timestamps for Department
    dept_created = Department.objects.filter(created_at__isnull=True).update(created_at=now)
    dept_updated = Department.objects.filter(updated_at__isnull=True).update(updated_at=now)
    print(f"Updated {dept_created} Department created_at and {dept_updated} updated_at fields")
    
    # Populate NULL timestamps for Category
    cat_created = Category.objects.filter(created_at__isnull=True).update(created_at=now)
    cat_updated = Category.objects.filter(updated_at__isnull=True).update(updated_at=now)
    print(f"Updated {cat_created} Category created_at and {cat_updated} updated_at fields")
    
    # Populate NULL timestamps for Subcategory
    subcat_created = Subcategory.objects.filter(created_at__isnull=True).update(created_at=now)
    subcat_updated = Subcategory.objects.filter(updated_at__isnull=True).update(updated_at=now)
    print(f"Updated {subcat_created} Subcategory created_at and {subcat_updated} updated_at fields")
    
    # Generate slugs for Department records with empty/null slugs
    dept_slug_count = 0
    for dept in Department.objects.filter(slug__in=['', None]):
        base_slug = slugify(dept.name)
        slug = base_slug
        counter = 1
        # Ensure uniqueness
        while Department.objects.filter(slug=slug).exclude(pk=dept.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        dept.slug = slug
        dept.save()
        dept_slug_count += 1
    print(f"Generated {dept_slug_count} Department slugs")
    
    # Generate slugs for Category records with empty/null slugs
    cat_slug_count = 0
    for cat in Category.objects.filter(slug__in=['', None]):
        base_slug = slugify(cat.name)
        slug = base_slug
        counter = 1
        # Ensure uniqueness
        while Category.objects.filter(slug=slug).exclude(pk=cat.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        cat.slug = slug
        cat.save()
        cat_slug_count += 1
    print(f"Generated {cat_slug_count} Category slugs")
    
    # Generate slugs for Subcategory records with empty/null slugs
    subcat_slug_count = 0
    for subcat in Subcategory.objects.filter(slug__in=['', None]):
        base_slug = slugify(subcat.name)
        slug = base_slug
        counter = 1
        # Ensure uniqueness
        while Subcategory.objects.filter(slug=slug).exclude(pk=subcat.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        subcat.slug = slug
        subcat.save()
        subcat_slug_count += 1
    print(f"Generated {subcat_slug_count} Subcategory slugs")
    
    # Generate slugs for Product records with empty/null slugs
    prod_slug_count = 0
    for prod in Product.objects.filter(slug__in=['', None]):
        base_slug = slugify(prod.name)
        slug = base_slug
        counter = 1
        # Ensure uniqueness
        while Product.objects.filter(slug=slug).exclude(pk=prod.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        prod.slug = slug
        prod.save()
        prod_slug_count += 1
    print(f"Generated {prod_slug_count} Product slugs")


def reverse_populate_timestamps_and_slugs(apps, schema_editor):
    """
    Reverse migration - no action needed
    We don't want to delete the timestamps/slugs we just created
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_add_seo_fields_to_all_categories'),
    ]

    operations = [
        migrations.RunPython(
            populate_timestamps_and_slugs, 
            reverse_populate_timestamps_and_slugs
        ),
    ]


# products/management/commands/fix_missing_images.py
"""Django management command to find and optionally clear missing images."""

import re
from django.core.management.base import BaseCommand
from products.models import Category, Subcategory, Department, Product
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Fix categories/subcategories/departments with missing image files and broken image references in product descriptions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without actually fixing it',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear image field for records with missing files',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        clear_missing = options['clear']
        
        self.stdout.write(self.style.SUCCESS('Checking for missing image files...\n'))
        
        # Check Categories
        self.stdout.write(self.style.WARNING('=== Categories ==='))
        categories_fixed = self.check_and_fix_model(Category, dry_run, clear_missing)
        
        # Check Subcategories
        self.stdout.write(self.style.WARNING('\n=== Subcategories ==='))
        subcategories_fixed = self.check_and_fix_model(Subcategory, dry_run, clear_missing)
        
        # Check Departments
        self.stdout.write(self.style.WARNING('\n=== Departments ==='))
        departments_fixed = self.check_and_fix_model(Department, dry_run, clear_missing)
        
        # Check Product descriptions for broken image references
        self.stdout.write(self.style.WARNING('\n=== Product Descriptions ==='))
        products_fixed = self.check_and_fix_product_descriptions(dry_run, clear_missing)
        
        # Summary
        total_fixed = categories_fixed + subcategories_fixed + departments_fixed + products_fixed
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f'\n✅ Dry run complete. Found {total_fixed} records with missing images.'
            ))
            self.stdout.write(self.style.WARNING(
                'Run with --clear to actually fix these records.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'\n✅ Fixed {total_fixed} records with missing images.'
            ))

    def check_and_fix_model(self, model_class, dry_run, clear_missing):
        """Check and fix missing images for a model"""
        fixed_count = 0
        model_name = model_class.__name__
        
        # Get all records with images
        records_with_images = model_class.objects.exclude(image__isnull=True).exclude(image='')
        
        for record in records_with_images:
            image_field = getattr(record, 'image', None)
            if image_field:
                if not image_field.storage.exists(image_field.name):
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ❌ {model_name} "{record.name}" (ID: {record.id}) - '
                            f'Missing: {image_field.name}'
                        )
                    )
                    if clear_missing and not dry_run:
                        record.image = None
                        record.save(update_fields=['image'])
                        self.stdout.write(self.style.SUCCESS('    ✅ Cleared image field'))
                    fixed_count += 1
                elif not dry_run and not clear_missing:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✅ {model_name} "{record.name}" - Image exists'
                        )
                    )
        
        if fixed_count == 0:
            self.stdout.write(self.style.SUCCESS(f'  ✅ All {model_name} images exist'))
        
        return fixed_count
    
    def check_and_fix_product_descriptions(self, dry_run, clear_missing):
        """Check and fix broken image references in product descriptions"""
        fixed_count = 0
        
        # Pattern to find img tags with src attributes
        img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
        
        products = Product.objects.exclude(description__isnull=True).exclude(description='')
        
        for product in products:
            if not product.description:
                continue
                
            # Find all image references in description
            matches = img_pattern.findall(product.description)
            broken_images = []
            
            for img_src in matches:
                # Check if it's a broken reference (like imgi_ files or static/ paths that don't exist)
                if 'imgi_' in img_src or '/static/imgi_' in img_src:
                    # Check if file exists
                    file_exists = False
                    
                    # Try different paths
                    if img_src.startswith('/'):
                        # Absolute path
                        if img_src.startswith('/static/'):
                            static_path = os.path.join(settings.STATIC_ROOT, img_src.replace('/static/', ''))
                            file_exists = os.path.exists(static_path)
                        elif img_src.startswith('/media/'):
                            media_path = os.path.join(settings.MEDIA_ROOT, img_src.replace('/media/', ''))
                            file_exists = os.path.exists(media_path)
                    else:
                        # Relative path - try static and media
                        static_path = os.path.join(settings.STATIC_ROOT, img_src)
                        media_path = os.path.join(settings.MEDIA_ROOT, img_src)
                        file_exists = os.path.exists(static_path) or os.path.exists(media_path)
                    
                    if not file_exists:
                        broken_images.append(img_src)
            
            if broken_images:
                self.stdout.write(
                    self.style.ERROR(
                        f'  ❌ Product "{product.name}" (ID: {product.id}) - '
                        f'Found {len(broken_images)} broken image reference(s)'
                    )
                )
                for img_src in broken_images[:3]:  # Show first 3
                    self.stdout.write(f'      - {img_src}')
                if len(broken_images) > 3:
                    self.stdout.write(f'      ... and {len(broken_images) - 3} more')
                
                if clear_missing and not dry_run:
                    # Remove broken img tags from description
                    updated_description = product.description
                    for img_src in broken_images:
                        # Remove img tag with this src
                        pattern = re.compile(
                            r'<img[^>]*src=["\']' + re.escape(img_src) + r'["\'][^>]*>',
                            re.IGNORECASE
                        )
                        updated_description = pattern.sub('', updated_description)
                    
                    product.description = updated_description
                    product.save(update_fields=['description'])
                    self.stdout.write(self.style.SUCCESS('    ✅ Removed broken image references'))
                
                fixed_count += 1
        
        if fixed_count == 0:
            self.stdout.write(self.style.SUCCESS('  ✅ No broken image references found in product descriptions'))
        
        return fixed_count


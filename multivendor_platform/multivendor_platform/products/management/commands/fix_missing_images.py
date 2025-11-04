# products/management/commands/fix_missing_images.py
"""Django management command to find and optionally clear missing images."""

from django.core.management.base import BaseCommand
from products.models import Category, Subcategory, Department


class Command(BaseCommand):
    help = 'Fix categories/subcategories/departments with missing image files'

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
        
        # Summary
        total_fixed = categories_fixed + subcategories_fixed + departments_fixed
        
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


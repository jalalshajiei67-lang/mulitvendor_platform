"""
Auto-link subcategories to categories based on name matching
This helps organize scraped subcategories into the existing category structure
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from products.models import Subcategory, Category, Department
from difflib import SequenceMatcher
import re


class Command(BaseCommand):
    help = 'Automatically link subcategories to matching categories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--threshold',
            type=float,
            default=0.6,
            help='Similarity threshold (0.0-1.0). Default: 0.6'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be linked without making changes'
        )
        parser.add_argument(
            '--exact-only',
            action='store_true',
            help='Only link exact matches (case-insensitive)'
        )

    def handle(self, *args, **options):
        threshold = options['threshold']
        dry_run = options['dry_run']
        exact_only = options['exact_only']

        self.stdout.write(self.style.WARNING('\n' + '='*70))
        self.stdout.write(self.style.WARNING('🔗 AUTO-LINK SUBCATEGORIES TO CATEGORIES'))
        self.stdout.write(self.style.WARNING('='*70 + '\n'))

        if dry_run:
            self.stdout.write(self.style.NOTICE('🔍 DRY RUN MODE - No changes will be made\n'))

        # Get all categories and subcategories
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()

        self.stdout.write(f'📊 Found {categories.count()} categories and {subcategories.count()} subcategories\n')

        # Statistics
        exact_matches = 0
        fuzzy_matches = 0
        no_matches = 0
        already_linked = 0
        skipped = 0

        for subcat in subcategories:
            # Check if already linked
            current_links = subcat.categories.count()
            if current_links > 0:
                already_linked += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {subcat.name} - Already linked to {current_links} categories')
                )
                continue

            # Clean name for better matching
            subcat_clean = self.clean_name(subcat.name)

            # Try exact match first
            exact_match = None
            for cat in categories:
                cat_clean = self.clean_name(cat.name)
                if cat_clean == subcat_clean:
                    exact_match = cat
                    break

            if exact_match:
                exact_matches += 1
                if not dry_run:
                    subcat.categories.add(exact_match)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ EXACT: {subcat.name} ➜ {exact_match.name}')
                )
                continue

            # Skip fuzzy matching if exact-only mode
            if exact_only:
                no_matches += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ NO MATCH: {subcat.name}')
                )
                continue

            # Try fuzzy matching
            best_match = None
            best_score = 0

            for cat in categories:
                score = self.similarity(subcat_clean, self.clean_name(cat.name))
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = cat

            if best_match:
                fuzzy_matches += 1
                if not dry_run:
                    subcat.categories.add(best_match)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ FUZZY ({best_score:.2f}): {subcat.name} ➜ {best_match.name}'
                    )
                )
            else:
                no_matches += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ NO MATCH: {subcat.name}')
                )

        # Summary
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.WARNING('📈 SUMMARY'))
        self.stdout.write('='*70 + '\n')
        
        self.stdout.write(f'✅ Exact matches: {exact_matches}')
        self.stdout.write(f'🔍 Fuzzy matches: {fuzzy_matches}')
        self.stdout.write(f'✓  Already linked: {already_linked}')
        self.stdout.write(f'⚠️  No matches: {no_matches}')
        self.stdout.write(f'📊 Total processed: {subcategories.count()}')

        if dry_run:
            self.stdout.write(
                self.style.NOTICE('\n💡 This was a dry run. Run without --dry-run to apply changes.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\n✨ Successfully linked {exact_matches + fuzzy_matches} subcategories!')
            )

        # Show unlinked subcategories
        if no_matches > 0:
            self.stdout.write('\n' + '-'*70)
            self.stdout.write(self.style.WARNING('📋 UNLINKED SUBCATEGORIES (need manual assignment):'))
            self.stdout.write('-'*70 + '\n')
            
            unlinked = Subcategory.objects.filter(categories__isnull=True)
            for subcat in unlinked:
                self.stdout.write(f'  • {subcat.name}')

            self.stdout.write(
                self.style.NOTICE(
                    f'\n💡 Assign these manually in Django admin:\n'
                    f'   http://127.0.0.1:8000/admin/products/subcategory/\n'
                )
            )

    def clean_name(self, name):
        """Clean name for better matching"""
        # Remove special characters and extra whitespace
        cleaned = re.sub(r'[^\w\s]', '', name.lower())
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def similarity(self, a, b):
        """Calculate similarity ratio between two strings"""
        return SequenceMatcher(None, a, b).ratio()


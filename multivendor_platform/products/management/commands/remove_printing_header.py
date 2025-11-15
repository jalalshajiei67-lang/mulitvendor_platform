from django.core.management.base import BaseCommand
from django.db import models
from products.models import Category
import re


class Command(BaseCommand):
    help = 'Remove unwanted HTML content from printing machines category header'

    def handle(self, *args, **options):
        def remove_printing_header_content(description):
            if not description:
                return description

            # Pattern to match the HTML-encoded content
            pattern1 = r'<p[^>]*>&lt;h2&gt;ماشین آلات چاپ: از ایده تا اجرا&lt;/h2&gt;\s*&lt;p&gt;انتخاب ماشین چاپ مناسب یکی از مهمترینو رضایت مشتری خواهد بود\.&lt;/p&gt;</p>'

            # Pattern to match the regular HTML content
            pattern2 = r'<p[^>]*>ماشین آلات چاپ: از ایده تا اجرا</p>\s*<p[^>]*>انتخاب ماشین چاپ مناسب یکی از مهمترین[^<]*رضایت مشتری خواهد بود\.</p>'

            # Remove both patterns
            cleaned = re.sub(pattern1, '', description, flags=re.DOTALL)
            cleaned = re.sub(pattern2, '', cleaned, flags=re.DOTALL)

            return cleaned.strip()

        # Find categories with printing-related content
        categories = Category.objects.filter(
            models.Q(description__icontains='ماشین آلات چاپ') |
            models.Q(description__icontains='printing')
        )

        updated_count = 0
        for cat in categories:
            original = cat.description
            cleaned = remove_printing_header_content(original)

            if cleaned != original:
                cat.description = cleaned
                cat.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Updated category: {cat.name}')
                )

        if updated_count == 0:
            # If no categories found, check all categories for the specific pattern
            all_categories = Category.objects.all()
            for cat in all_categories:
                if cat.description:
                    original = cat.description
                    cleaned = remove_printing_header_content(original)

                    if cleaned != original:
                        cat.description = cleaned
                        cat.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Updated category: {cat.name}')
                        )

        self.stdout.write(
            self.style.SUCCESS(f'Total categories updated: {updated_count}')
        )

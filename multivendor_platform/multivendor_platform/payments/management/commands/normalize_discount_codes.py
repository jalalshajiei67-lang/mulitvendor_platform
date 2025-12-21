"""
Management command to normalize all discount codes to uppercase
Usage: python manage.py normalize_discount_codes
"""
from django.core.management.base import BaseCommand
from payments.models import DiscountCampaign


class Command(BaseCommand):
    help = 'Normalize all discount codes to uppercase'

    def handle(self, *args, **options):
        campaigns = DiscountCampaign.objects.all()
        normalized_count = 0
        
        for campaign in campaigns:
            old_code = campaign.code
            new_code = campaign.code.strip().upper()
            
            if old_code != new_code:
                campaign.code = new_code
                campaign.save(update_fields=['code'])
                normalized_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Normalized: "{old_code}" -> "{new_code}"'
                    )
                )
        
        if normalized_count == 0:
            self.stdout.write(
                self.style.SUCCESS('All discount codes are already normalized.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully normalized {normalized_count} discount code(s).'
                )
            )


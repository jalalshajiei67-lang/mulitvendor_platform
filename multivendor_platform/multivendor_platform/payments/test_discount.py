"""
Test script to verify discount codes are working
Run: python manage.py shell < payments/test_discount.py
"""
from payments.models import DiscountCampaign
from django.utils import timezone

print("=" * 60)
print("Testing Discount Campaigns")
print("=" * 60)

campaigns = DiscountCampaign.objects.all()
print(f"\nTotal campaigns: {campaigns.count()}\n")

for campaign in campaigns:
    print(f"Code: '{campaign.code}'")
    print(f"  Name: {campaign.name}")
    print(f"  Active: {campaign.is_active}")
    print(f"  Valid From: {campaign.valid_from}")
    print(f"  Valid Until: {campaign.valid_until}")
    print(f"  Now: {timezone.now()}")
    print(f"  In Range: {campaign.valid_from <= timezone.now() <= campaign.valid_until}")
    print(f"  Used: {campaign.used_count}/{campaign.max_uses if campaign.max_uses else 'unlimited'}")
    print(f"  Discount: {campaign.discount_value} ({campaign.get_discount_type_display()})")
    print(f"  Billing Period: {campaign.get_billing_period_display()}")
    print()

# Test lookup
test_codes = ['TEST', 'test', 'WELLCOME', 'wellcome']
print("\n" + "=" * 60)
print("Testing Code Lookup")
print("=" * 60)

for test_code in test_codes:
    found = DiscountCampaign.objects.filter(code__iexact=test_code).first()
    if found:
        print(f"✓ '{test_code}' -> Found: '{found.code}'")
    else:
        print(f"✗ '{test_code}' -> Not found")


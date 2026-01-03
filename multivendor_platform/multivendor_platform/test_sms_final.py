#!/usr/bin/env python
"""
SMS Newsletter Test Script

This script tests the SMS newsletter functionality using the Kavenegar API.
You can modify the test data below to test with different suppliers.

Usage:
    # Set environment variables
    export KAVENEGAR_API_KEY="your-api-key"
    export KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME="SupplyerNotif"
    
    # Run the test
    python test_sms_final.py

For local testing without sending real SMS:
    export SMS_NEWSLETTER_LOCAL_MODE=true
    python test_sms_final.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from sms_newsletter.models import Seller
from sms_newsletter.services import send_sms_via_kavenegar


def test_final():
    """Final test with actual supplier data"""
    
    print("\n" + "="*70)
    print("📱 SMS Newsletter - Final Test")
    print("="*70)
    
    # Your actual test data
    test_name = "رجبعلی طیبی نژاد"
    test_mobile = "09124242066"
    test_filter = "خط تولید نوار بهداشتی صنعتی"
    
    print(f"\n📝 Supplier Information:")
    print(f"   Name: {test_name}")
    print(f"   Mobile: {test_mobile}")
    print(f"   Filter Applied: {test_filter}")
    
    # Token processing explanation
    print(f"\n🔧 Token Processing:")
    print(f"   Original name length: {len(test_name)} chars")
    print(f"   Original filter length: {len(test_filter)} chars")
    
    # Simulate token processing (same as service)
    name_clean = test_name.replace(' ', '')
    filter_clean = test_filter.replace(' ', '')
    name_display = name_clean[:3]
    filter_display = filter_clean[:3]
    
    print(f"   After removing spaces:")
    print(f"     Name: '{name_clean}' ({len(name_clean)} chars)")
    print(f"     Filter: '{filter_clean}' ({len(filter_clean)} chars)")
    print(f"   Final tokens (3 chars max):")
    print(f"     Token 1: '{name_display}'")
    print(f"     Token 2: '{filter_display}'")
    
    # Expected message
    print(f"\n📨 Expected SMS Content:")
    print(f"   سلام، {name_display} عزیز برای {filter_display} مشتری جدیدی منتظر شماست.")
    print(f"   ایندکسو")
    print(f"   indexo.ir/s/notif")
    
    # Get or create seller
    seller, created = Seller.objects.get_or_create(
        mobile_number=test_mobile,
        defaults={'name': test_name}
    )
    if not created and seller.name != test_name:
        seller.name = test_name
        seller.save()
    
    # Send SMS
    print(f"\n📤 Sending SMS to {test_mobile}...")
    result = send_sms_via_kavenegar(seller, test_filter)
    
    # Display result
    print(f"\n📊 Result:")
    if result.get('success'):
        print(f"   ✅ SMS sent successfully!")
        print(f"   Message: {result.get('message')}")
        if not result.get('local_mode'):
            print(f"   📱 Check your phone ({test_mobile}) for the SMS!")
    else:
        print(f"   ❌ Failed to send SMS")
        print(f"   Error: {result.get('message')}")
        if result.get('error'):
            print(f"   Details: {result.get('error')}")
    
    print("\n" + "="*70 + "\n")
    
    return result


if __name__ == '__main__':
    try:
        result = test_final()
        sys.exit(0 if result.get('success') else 1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


#!/usr/bin/env python
"""
Test script for Kavenegar OTP API
Run this to test your Kavenegar configuration locally
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

import requests
from django.conf import settings
from users.services.otp_senders import KavenegarOTPSender

def test_kavenegar_config():
    """Test Kavenegar configuration"""
    print("=" * 60)
    print("Testing Kavenegar Configuration")
    print("=" * 60)
    
    api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
    template_name = getattr(settings, 'KAVENEGAR_OTP_TEMPLATE_NAME', None)
    otp_sender_class = getattr(settings, 'OTP_SENDER_CLASS', None)
    
    print(f"\n1. API Key: {'✅ Set' if api_key else '❌ NOT SET'}")
    if api_key:
        print(f"   Value: {api_key[:10]}...{api_key[-10:]}")
    else:
        print("   Set KAVENEGAR_API_KEY environment variable")
    
    print(f"\n2. Template Name: {'✅ Set' if template_name else '❌ NOT SET'}")
    if template_name:
        print(f"   Value: {template_name}")
    else:
        print("   Set KAVENEGAR_OTP_TEMPLATE_NAME environment variable")
    
    print(f"\n3. OTP Sender Class: {otp_sender_class}")
    if 'KavenegarOTPSender' in otp_sender_class:
        print("   ✅ Using KavenegarOTPSender")
    else:
        print("   ⚠️  Not using KavenegarOTPSender")
        print("   Set OTP_SENDER_CLASS=users.services.otp_senders.KavenegarOTPSender")
    
    return api_key and template_name

def test_api_directly(api_key: str, template_name: str, phone: str, code: str = "123456"):
    """Test Kavenegar API directly"""
    print("\n" + "=" * 60)
    print("Testing Kavenegar API Directly")
    print("=" * 60)
    
    # Prepare API URL
    base_url = f'https://api.kavenegar.com/v1/{api_key}/verify/lookup.json'
    
    # Prepare parameters
    params = {
        'receptor': phone,
        'template': template_name,
        'token': code
    }
    
    print(f"\n📞 Phone: {phone}")
    print(f"📝 Template: {template_name}")
    print(f"🔑 Code: {code}")
    print(f"\n🌐 URL: {base_url}")
    print(f"📦 Params: {params}")
    
    try:
        print("\n⏳ Sending request to Kavenegar API...")
        response = requests.get(base_url, params=params, timeout=10)
        
        print(f"\n📊 Response Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        result = response.json()
        print(f"\n📋 Response Body:")
        print(f"   {result}")
        
        # Check response
        if result.get('return', {}).get('status') == 200:
            print("\n✅ SUCCESS! SMS sent successfully")
            entries = result.get('entries', [])
            if entries:
                print(f"   Message ID: {entries[0].get('messageid', 'N/A')}")
            return True
        else:
            error_message = result.get('return', {}).get('message', 'Unknown error')
            status = result.get('return', {}).get('status', 'N/A')
            print(f"\n❌ ERROR!")
            print(f"   Status: {status}")
            print(f"   Message: {error_message}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n❌ TIMEOUT: Request took too long")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ CONNECTION ERROR: {str(e)}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"\n❌ REQUEST ERROR: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_otp_sender_class(phone: str, code: str = "123456"):
    """Test using OTP Sender class"""
    print("\n" + "=" * 60)
    print("Testing OTP Sender Class")
    print("=" * 60)
    
    try:
        sender = KavenegarOTPSender()
        print(f"\n📞 Phone: {phone}")
        print(f"🔑 Code: {code}")
        print(f"📝 Purpose: login")
        
        print("\n⏳ Calling send_otp()...")
        result = sender.send_otp(code, phone, 'login')
        
        print(f"\n📋 Result:")
        print(f"   Success: {result.get('success')}")
        print(f"   Message: {result.get('message')}")
        print(f"   Delivery Method: {result.get('delivery_method')}")
        if 'error' in result:
            print(f"   Error: {result.get('error')}")
        
        if result.get('success'):
            print("\n✅ SUCCESS! OTP sender worked correctly")
            return True
        else:
            print("\n❌ FAILED! Check the error message above")
            return False
            
    except Exception as e:
        print(f"\n❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("\n" + "🔍 " * 30)
    print("Kavenegar OTP API Test Script")
    print("🔍 " * 30)
    
    # Test configuration
    config_ok = test_kavenegar_config()
    
    if not config_ok:
        print("\n" + "=" * 60)
        print("❌ Configuration incomplete!")
        print("=" * 60)
        print("\nTo fix, set these environment variables:")
        print("  export KAVENEGAR_API_KEY='your-api-key'")
        print("  export KAVENEGAR_OTP_TEMPLATE_NAME='OTPInedexo'")
        print("  export OTP_SENDER_CLASS='users.services.otp_senders.KavenegarOTPSender'")
        print("\nThen restart Django server.")
        sys.exit(1)
    
    # Get phone number from command line or use default
    if len(sys.argv) > 1:
        phone = sys.argv[1]
    else:
        phone = input("\nEnter phone number to test (e.g., 09123456789): ").strip()
        if not phone:
            print("❌ Phone number is required")
            sys.exit(1)
    
    # Test API directly
    api_key = getattr(settings, 'KAVENEGAR_API_KEY')
    template_name = getattr(settings, 'KAVENEGAR_OTP_TEMPLATE_NAME')
    
    print(f"\n⚠️  This will send a REAL SMS to {phone}!")
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Test cancelled")
        sys.exit(0)
    
    # Test with test code
    test_code = "123456"
    print(f"\n🔑 Using test code: {test_code}")
    
    # Test 1: Direct API call
    api_success = test_api_directly(api_key, template_name, phone, test_code)
    
    # Test 2: OTP Sender class
    sender_success = test_otp_sender_class(phone, test_code)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Direct API Test: {'✅ PASSED' if api_success else '❌ FAILED'}")
    print(f"Sender Class Test: {'✅ PASSED' if sender_success else '❌ FAILED'}")
    
    if api_success and sender_success:
        print("\n✅ All tests passed! Kavenegar integration is working.")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()





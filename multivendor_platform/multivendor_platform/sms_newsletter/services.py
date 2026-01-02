import requests
import logging
import re
from django.conf import settings
from typing import List, Dict, Optional
from .models import Seller
from products.models import Subcategory

logger = logging.getLogger(__name__)


def _normalize_phone(phone: str) -> str:
    """
    Normalize phone number format for Kavenegar API.
    Converts various formats to Iranian format (09XXXXXXXXX).
    
    Args:
        phone: Phone number in any format
        
    Returns:
        Normalized phone number
    """
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-()]', '', phone.strip())
    
    # Normalize to Iranian format (09XXXXXXXXX)
    if cleaned.startswith('+98'):
        cleaned = '0' + cleaned[3:]
    elif cleaned.startswith('0098'):
        cleaned = '0' + cleaned[4:]
    elif cleaned.startswith('98'):
        cleaned = '0' + cleaned[2:]
    elif not cleaned.startswith('0'):
        cleaned = '0' + cleaned
    
    return cleaned


def send_sms_via_kavenegar(
    seller: Seller,
    filter_name: str
) -> Dict[str, any]:
    """
    Send SMS to seller via Kavenegar API using lookup template.
    Template: SupplyerNotif
    - %token = seller name
    - %token2 = filter name (applied filter from admin, max 45 chars)
    
    In local/development mode (when KAVENEGAR_API_KEY is not set),
    the SMS content will be logged to console instead of being sent.
    
    Args:
        seller: Seller instance
        filter_name: Name of the applied filter (from admin filter selection)
        
    Returns:
        Dict with 'success' (bool) and 'message' (str) keys
    """
    api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
    template_name = getattr(settings, 'KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME', 'SupplyerNotif')
    use_local_mode = getattr(settings, 'SMS_NEWSLETTER_LOCAL_MODE', False)
    
    # Normalize phone number
    phone = _normalize_phone(seller.mobile_number)
    
    # Prepare filter name - limit to 45 characters
    # Truncate if too long and add ellipsis
    if len(filter_name) > 45:
        filter_name_display = filter_name[:42] + "..."
    else:
        filter_name_display = filter_name
    
    # Local mode: Log to console instead of sending real SMS
    if not api_key or use_local_mode:
        logger.info(f"[LOCAL SMS] Supplier Notification SMS (not sent)")
        print(f"\n{'='*70}")
        print(f"📱 SUPPLIER NOTIFICATION SMS (LOCAL MODE - NOT SENT)")
        print(f"{'='*70}")
        print(f"To: {phone}")
        print(f"Seller: {seller.name}")
        print(f"Filter Name: {filter_name_display}")
        print(f"\nMessage Template: SupplyerNotif")
        print(f"Token 1 (Name): {seller.name}")
        print(f"Token 2 (Filter): {filter_name_display}")
        print(f"\nFull Message:")
        print(f"سلام، {seller.name} عزیز برای {filter_name_display} مشتری جدیدی منتظر شماست.")
        print(f"ایندکسو")
        print(f"indexo.ir/s/notif")
        print(f"{'='*70}\n")
        
        return {
            'success': True,
            'message': 'پیامک با موفقیت ارسال شد (حالت تست - در محیط واقعی ارسال می‌شود)',
            'local_mode': True
        }
    
    # Prepare API URL
    base_url = f'https://api.kavenegar.com/v1/{api_key}/verify/lookup.json'
    
    # Prepare parameters
    # Template: SupplyerNotif
    # %token = seller name
    # %token2 = filter name (max 45 chars)
    params = {
        'receptor': phone,
        'template': template_name,
        'token': seller.name,
        'token2': filter_name_display
    }
    
    try:
        # Make API request
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        # Check Kavenegar response structure
        # Kavenegar returns: {"return": {"status": 200, "message": "..."}, "entries": [...]}
        if result.get('return', {}).get('status') == 200:
            logger.info(f"Supplier notification SMS sent successfully via Kavenegar to {phone} (seller: {seller.name})")
            return {
                'success': True,
                'message': 'پیامک با موفقیت ارسال شد'
            }
        else:
            error_message = result.get('return', {}).get('message', 'Unknown error')
            logger.error(f'Kavenegar API error: {error_message} | Response: {result} | Seller: {seller.name} | Phone: {phone}')
            return {
                'success': False,
                'message': 'خطا در ارسال پیامک. لطفاً بعداً تلاش کنید.',
                'error': error_message
            }
                
    except requests.exceptions.Timeout:
        logger.error(f'Kavenegar API timeout when sending supplier notification SMS to {phone} (seller: {seller.name})')
        return {
            'success': False,
            'message': 'زمان ارسال پیامک به پایان رسید. لطفاً دوباره تلاش کنید.'
        }
    except requests.exceptions.RequestException as e:
        logger.error(f'Kavenegar API network error when sending supplier notification SMS: {str(e)} | Seller: {seller.name} | Phone: {phone}')
        return {
            'success': False,
            'message': 'خطا در اتصال به سرویس پیامک. لطفاً بعداً تلاش کنید.'
        }
    except Exception as e:
        logger.error(f'Unexpected error sending supplier notification SMS via Kavenegar: {str(e)} | Seller: {seller.name} | Phone: {phone}')
        return {
            'success': False,
            'message': 'خطای غیرمنتظره در ارسال پیامک. لطفاً با پشتیبانی تماس بگیرید.'
        }


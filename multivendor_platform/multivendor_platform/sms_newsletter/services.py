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
    
    Due to Kavenegar HTTP 431 limitations, tokens are limited to ~6-7 chars total.
    Strategy: Use first name + first word of filter for maximum clarity.
    
    Template: SupplyerNotif
    - %token = first name (e.g., "رجبعلی" from "رجبعلی طیب پور")
    - %token2 = first word of filter (e.g., "خط" from "خط تولید نوار...")
    
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
    
    # Debug logging
    logger.debug(f"SMS Newsletter - API Key present: {bool(api_key)}, Template: {template_name}, Local Mode: {use_local_mode}")
    
    # Normalize phone number
    phone = _normalize_phone(seller.mobile_number)
    
    # Kavenegar token rules (from provider):
    # %token, %token2, %token3 - No spaces allowed
    # %token10 - Accepts up to 4 spaces (5 words)
    # %token20 - Accepts up to 8 spaces (9 words)
    
    # New template structure:
    # %token = "سلام" (static greeting, always same)
    # %token10 = Full name with spaces (up to 4 spaces)
    # %token20 = Full filter with spaces (up to 8 spaces)
    
    greeting = "سلام"
    
    # Name: Full name with spaces (truncate if > 4 spaces for %token10)
    seller_name_display = seller.name.strip()
    name_spaces = seller_name_display.count(' ')
    
    if name_spaces > 4:
        # Truncate to first 5 words (4 spaces) for %token10 limit
        words = seller_name_display.split()
        seller_name_display = ' '.join(words[:5])
        logger.info(f'Name truncated to 5 words (4 spaces): "{seller_name_display}"')
    
    # Filter: Full filter with spaces (truncate if > 8 spaces for %token20)
    filter_name_display = filter_name.strip()
    filter_spaces = filter_name_display.count(' ')
    
    if filter_spaces > 8:
        # Truncate to first 9 words (8 spaces) for %token20 limit
        words = filter_name_display.split()
        filter_name_display = ' '.join(words[:9])
        logger.info(f'Filter truncated to 9 words (8 spaces): "{filter_name_display}"')
    
    logger.info(
        f'Token extraction: '
        f'Greeting="{greeting}", '
        f'Name="{seller.name}" -> "{seller_name_display}" ({len(seller_name_display)} chars, {seller_name_display.count(" ")} spaces), '
        f'Filter="{filter_name}" -> "{filter_name_display}" ({len(filter_name_display)} chars, {filter_name_display.count(" ")} spaces)'
    )
    
    # Local mode: Log to console instead of sending real SMS
    if not api_key or use_local_mode:
        if not api_key:
            logger.warning("KAVENEGAR_API_KEY is not set - using local mode. Set KAVENEGAR_API_KEY in environment variables to send real SMS.")
        if use_local_mode:
            logger.info("SMS_NEWSLETTER_LOCAL_MODE is enabled - using local mode")
        logger.info(f"[LOCAL SMS] Supplier Notification SMS (not sent)")
        print(f"\n{'='*70}")
        print(f"📱 SUPPLIER NOTIFICATION SMS (LOCAL MODE - NOT SENT)")
        print(f"{'='*70}")
        print(f"To: {phone}")
        print(f"Full Name: {seller.name}")
        print(f"Full Filter: {filter_name}")
        print(f"\nTokens Used:")
        print(f"  %token (Greeting): {greeting}")
        print(f"  %token10 (Name): {seller_name_display}")
        print(f"  %token20 (Filter): {filter_name_display}")
        print(f"\nMessage Template: {template_name}")
        print(f"Expected SMS:")
        print(f"{greeting}، {seller_name_display} عزیز برای {filter_name_display} مشتری جدیدی منتظر شماست.")
        print(f"ایندکسو")
        print(f"indexo.ir/s/notif")
        print(f"{'='*70}\n")
        
        return {
            'success': True,
            'message': 'پیامک با موفقیت ارسال شد (حالت تست - در محیط واقعی ارسال می‌شود)',
            'local_mode': True
        }
    
    # Prepare API URL - using template lookup
    base_url = f'https://api.kavenegar.com/v1/{api_key}/verify/lookup.json'
    
    # Prepare parameters for new template structure
    # Template: %token، %token10 عزیز برای %token20 مشتری جدیدی منتظر شماست.
    params = {
        'receptor': phone,
        'template': template_name,
        'token': greeting,  # "سلام" - static greeting
        'token10': seller_name_display,  # Full name with spaces (up to 4 spaces)
        'token20': filter_name_display  # Full filter with spaces (up to 8 spaces)
    }
    
    try:
        # Log the request for debugging (without exposing full API key)
        logger.info(f"Sending SMS via Kavenegar - Template: {template_name}, Receptor: {phone}, Token: '{greeting}', Token10: '{seller_name_display}' ({len(seller_name_display)} chars, {seller_name_display.count(' ')} spaces), Token20: '{filter_name_display}' ({len(filter_name_display)} chars, {filter_name_display.count(' ')} spaces)")
        
        # Use GET method (Kavenegar verify/lookup.json requires GET, not POST)
        try:
            response = requests.get(
                base_url, 
                params=params,
                timeout=30
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as req_error:
            # Catch any request errors
            logger.error(f'Kavenegar API request error when sending SMS: {str(req_error)} | Seller: {seller.name} | Phone: {phone}')
            return {
                'success': False,
                'message': 'خطا در ارسال پیامک. لطفاً بعداً تلاش کنید.',
                'error': str(req_error)
            }
        
        result = response.json()
        
        # Check Kavenegar response structure
        # Kavenegar returns: {"return": {"status": 200, "message": "..."}, "entries": [...]}
        status_code = result.get('return', {}).get('status')
        if status_code == 200:
            logger.info(f"Supplier notification SMS sent successfully via Kavenegar to {phone} (seller: {seller.name}, filter: {filter_name})")
            return {
                'success': True,
                'message': 'پیامک با موفقیت ارسال شد'
            }
        else:
            error_message = result.get('return', {}).get('message', 'Unknown error')
            logger.error(
                f'Kavenegar API error {status_code}: {error_message} | '
                f'Response: {result} | Seller: {seller.name} | Phone: {phone}'
            )
            return {
                'success': False,
                'message': 'خطا در ارسال پیامک. لطفاً بعداً تلاش کنید.',
                'error': error_message,
                'error_code': status_code
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


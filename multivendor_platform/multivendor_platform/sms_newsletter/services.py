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
    
    # Debug logging
    logger.debug(f"SMS Newsletter - API Key present: {bool(api_key)}, Template: {template_name}, Local Mode: {use_local_mode}")
    
    # Normalize phone number
    phone = _normalize_phone(seller.mobile_number)
    
    # Use seller name - truncate if too long to avoid HTTP 431 errors
    # HTTP 431 = Request Header Fields Too Large
    # API key in URL is already 88 chars, making total URL ~136 chars
    # Need very short tokens to keep total request header size under limit
    # Persian characters in URL encoding can be 9 bytes each (%D8%A7)
    # Reduce to 20 chars to be safe (even shorter than before)
    MAX_TOKEN_LENGTH = 20
    seller_name_display = seller.name[:MAX_TOKEN_LENGTH] if len(seller.name) > MAX_TOKEN_LENGTH else seller.name
    
    # Use filter name - truncate if too long to avoid HTTP 431 errors
    # Even with POST, the URL length itself can cause header size issues
    filter_name_display = filter_name[:MAX_TOKEN_LENGTH] if len(filter_name) > MAX_TOKEN_LENGTH else filter_name
    
    if len(seller.name) > MAX_TOKEN_LENGTH or len(filter_name) > MAX_TOKEN_LENGTH:
        logger.warning(
            f'Token values truncated to avoid HTTP 431: '
            f'Seller name: {len(seller.name)} -> {len(seller_name_display)}, '
            f'Filter name: {len(filter_name)} -> {len(filter_name_display)}'
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
        print(f"Seller: {seller.name}")
        print(f"Filter Name: {filter_name_display}")
        print(f"\nMessage Template: SupplyerNotif")
        print(f"Token 1 (Name): {seller_name_display}")
        print(f"Token 2 (Filter): {filter_name_display}")
        print(f"\nFull Message:")
        print(f"سلام، {seller_name_display} عزیز برای {filter_name_display} مشتری جدیدی منتظر شماست.")
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
    # %token = seller name (max 20 chars to avoid HTTP 431 - Request Header Fields Too Large)
    # %token2 = filter name (max 20 chars to avoid HTTP 431 - Request Header Fields Too Large)
    # Note: Try GET first (like OTP sender), fall back to POST if needed
    params = {
        'receptor': phone,
        'template': template_name,
        'token': seller_name_display,
        'token2': filter_name_display
    }
    
    try:
        # Log the request for debugging (without exposing full API key)
        logger.info(f"Sending SMS via Kavenegar - Template: {template_name}, Receptor: {phone}, Token1 length: {len(seller_name_display)}, Token2 length: {len(filter_name_display)}")
        
        # Try GET method first (like OTP sender) to reduce header size
        # GET puts params in URL query string, which might be smaller than POST headers
        # If GET fails with 431, the URL itself is too long (API key + params)
        # Use minimal approach to avoid HTTP 431 (Request Header Fields Too Large)
        try:
            # Try GET first (works for OTP, might work here too with short tokens)
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as get_error:
            # If GET fails with 431, try POST (but likely will also fail)
            # If GET fails with other error, try POST as fallback
            if hasattr(get_error, 'response') and get_error.response.status_code == 431:
                # GET also got 431, URL is too long even with GET
                # Try POST as last resort, but it will likely also fail
                logger.warning("GET request returned 431, trying POST method (may also fail)")
                try:
                    response = requests.post(
                        base_url, 
                        data=params, 
                        timeout=10,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'}
                    )
                    response.raise_for_status()
                except requests.exceptions.HTTPError as post_error:
                    # POST also failed, re-raise to be handled below
                    raise post_error
            else:
                # GET failed with non-431 error, try POST
                logger.debug("GET request failed with non-431 error, trying POST method")
                try:
                    response = requests.post(
                        base_url, 
                        data=params, 
                        timeout=10,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'}
                    )
                    response.raise_for_status()
                except requests.exceptions.HTTPError as post_error:
                    # POST also failed, re-raise to be handled below
                    raise post_error
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Handle HTTP 431 (Request Header Fields Too Large)
            # This can happen if parameters are too long or API key in URL makes total request too large
            if e.response.status_code == 431:
                logger.error(
                    f'HTTP 431: Request header too large. '
                    f'Token1 length: {len(seller_name_display)}, Token2 length: {len(filter_name_display)}, '
                    f'Total URL length: ~{len(base_url)} chars'
                )
                return {
                    'success': False,
                    'message': 'خطا: داده‌های ارسالی بیش از حد مجاز است. لطفاً طول نام فروشنده یا فیلتر را کاهش دهید.',
                    'error': 'Request header too large (HTTP 431)',
                    'error_code': 431,
                    'help': f'Token1: {len(seller_name_display)} chars, Token2: {len(filter_name_display)} chars'
                }
            # Re-raise other HTTP errors to be handled by outer exception handler
            raise
        
        result = response.json()
        
        # Check Kavenegar response structure
        # Kavenegar returns: {"return": {"status": 200, "message": "..."}, "entries": [...]}
        status_code = result.get('return', {}).get('status')
        if status_code == 200:
            logger.info(f"Supplier notification SMS sent successfully via Kavenegar to {phone} (seller: {seller.name})")
            return {
                'success': True,
                'message': 'پیامک با موفقیت ارسال شد'
            }
        else:
            error_message = result.get('return', {}).get('message', 'Unknown error')
            
            # Special handling for error 431 (template structure mismatch)
            if status_code == 431:
                logger.error(
                    f'Kavenegar API error 431 (Template structure mismatch): {error_message} | '
                    f'Template: {template_name} | Seller: {seller.name} | Phone: {phone} | '
                    f'Token1: {seller_name_display[:50]}... | Token2: {filter_name_display[:50]}...'
                )
                return {
                    'success': False,
                    'message': 'خطا در ساختار قالب پیامک. لطفاً تنظیمات قالب "SupplyerNotif" را در پنل کاوه‌نگار بررسی کنید.',
                    'error': error_message,
                    'error_code': 431,
                    'help': 'لطفاً در پنل کاوه‌نگار بررسی کنید که قالب "SupplyerNotif" با دو توکن (token و token2) تعریف شده باشد.'
                }
            else:
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


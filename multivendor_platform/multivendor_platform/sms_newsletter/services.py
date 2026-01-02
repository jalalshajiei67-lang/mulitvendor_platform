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
    working_fields: Optional[List[Subcategory]] = None
) -> Dict[str, any]:
    """
    Send SMS to seller via Kavenegar API using lookup template.
    Template: SupplyerNotif
    - %token = seller name
    - %token2 = working fields
    
    Args:
        seller: Seller instance
        working_fields: Optional list of Subcategory instances to include in SMS
        
    Returns:
        Dict with 'success' (bool) and 'message' (str) keys
    """
    api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
    template_name = getattr(settings, 'KAVENEGAR_SUPPLIER_NOTIF_TEMPLATE_NAME', 'SupplyerNotif')
    
    if not api_key:
        logger.error('KAVENEGAR_API_KEY not configured in settings')
        return {
            'success': False,
            'message': 'سرویس پیامک پیکربندی نشده است. لطفاً با پشتیبانی تماس بگیرید.'
        }
    
    # Normalize phone number
    phone = _normalize_phone(seller.mobile_number)
    
    # Prepare working fields display
    if working_fields:
        working_fields_names = ", ".join([wf.name for wf in working_fields])
    else:
        # Use seller's working fields if not provided
        seller_working_fields = seller.working_fields.all()
        if seller_working_fields.exists():
            working_fields_names = ", ".join([wf.name for wf in seller_working_fields])
        else:
            working_fields_names = '-'
    
    # Prepare API URL
    base_url = f'https://api.kavenegar.com/v1/{api_key}/verify/lookup.json'
    
    # Prepare parameters
    # Template: SupplyerNotif
    # %token = seller name
    # %token2 = working fields
    params = {
        'receptor': phone,
        'template': template_name,
        'token': seller.name,
        'token2': working_fields_names
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


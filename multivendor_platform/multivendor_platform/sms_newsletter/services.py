import requests
from django.conf import settings
from typing import List, Dict, Optional
from .models import Seller
from products.models import Subcategory


def send_sms_via_kavenegar(
    seller: Seller,
    working_fields: Optional[List[Subcategory]] = None
) -> Dict[str, any]:
    """
    Send SMS to seller via Kavenegar API using lookup template.
    
    Args:
        seller: Seller instance
        working_fields: Optional list of Subcategory instances to include in SMS
        
    Returns:
        Dict with 'success' (bool) and 'message' (str) keys
    """
    api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
    template_name = getattr(settings, 'KAVENEGAR_TEMPLATE_NAME', None)
    
    if not api_key:
        return {
            'success': False,
            'message': 'KAVENEGAR_API_KEY not configured in settings'
        }
    
    if not template_name:
        return {
            'success': False,
            'message': 'KAVENEGAR_TEMPLATE_NAME not configured in settings'
        }
    
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
    params = {
        'receptor': seller.mobile_number,
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
            return {
                'success': True,
                'message': 'SMS sent successfully',
                'kavenegar_response': result
            }
        else:
            error_message = result.get('return', {}).get('message', 'Unknown error')
            return {
                'success': False,
                'message': f'Kavenegar API error: {error_message}',
                'kavenegar_response': result
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'message': f'Network error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Unexpected error: {str(e)}'
        }


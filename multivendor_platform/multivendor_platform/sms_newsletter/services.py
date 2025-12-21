"""
SMS sending service using Kavenegar API
"""
import os
import logging
from typing import List, Dict
from django.conf import settings

try:
    from kavenegar import KavenegarAPI, APIException, HTTPException
    KAVENEGAR_AVAILABLE = True
except ImportError:
    KAVENEGAR_AVAILABLE = False
    KavenegarAPI = None
    APIException = Exception
    HTTPException = Exception

logger = logging.getLogger(__name__)


class KavenegarSMSService:
    """
    Service for sending SMS via Kavenegar API using pattern-based messaging.
    """
    
    def __init__(self):
        if not KAVENEGAR_AVAILABLE:
            raise ImportError('kavenegar package is not installed. Install it with: pip install kavenegar')
        
        self.api_key = os.environ.get('KAVENEGAR_API_KEY')
        self.sender = os.environ.get('KAVENEGAR_SENDER', '10004346')
        self.pattern_id = os.environ.get('KAVENEGAR_PATTERN_ID')
        
        if not self.api_key:
            raise ValueError('KAVENEGAR_API_KEY environment variable is not set')
        
        if not self.pattern_id:
            raise ValueError('KAVENEGAR_PATTERN_ID environment variable is not set')
        
        try:
            self.api = KavenegarAPI(self.api_key)
        except Exception as e:
            logger.error(f'Failed to initialize Kavenegar API: {e}')
            raise
    
    def normalize_phone_number(self, phone: str) -> str:
        """
        Normalize Iranian phone number to format accepted by Kavenegar.
        Converts to format: 09123456789 or 02112345678
        """
        # Remove spaces, dashes, and plus signs
        cleaned = phone.replace(' ', '').replace('-', '').replace('+', '')
        
        # If starts with 98, replace with 0
        if cleaned.startswith('98'):
            cleaned = '0' + cleaned[2:]
        
        # If doesn't start with 0, add it
        if not cleaned.startswith('0'):
            cleaned = '0' + cleaned
        
        return cleaned
    
    def send_sms(
        self,
        receptor: str,
        name: str,
        company_name: str,
        category_name: str
    ) -> Dict:
        """
        Send SMS using Kavenegar pattern API.
        
        Args:
            receptor: Phone number to send SMS to
            name: Supplier name
            company_name: Company name
            category_name: Category/subcategory name
        
        Returns:
            Dict with success status and message
        """
        try:
            normalized_phone = self.normalize_phone_number(receptor)
            
            # Prepare pattern variables
            # Kavenegar pattern variables use token, token2, token3, etc.
            params = {
                'receptor': normalized_phone,
                'template': self.pattern_id,
                'token': name,
                'token2': company_name,
                'token3': category_name,
            }
            
            response = self.api.verify_lookup(params)
            
            logger.info(
                f'SMS sent successfully to {normalized_phone} '
                f'(name: {name}, company: {company_name}, category: {category_name})'
            )
            
            return {
                'success': True,
                'message': f'SMS sent to {normalized_phone}',
                'response': response
            }
            
        except APIException as e:
            error_msg = f'Kavenegar API error: {e}'
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'error': str(e)
            }
        
        except HTTPException as e:
            error_msg = f'Kavenegar HTTP error: {e}'
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'error': str(e)
            }
        
        except Exception as e:
            error_msg = f'Unexpected error sending SMS: {e}'
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'error': str(e)
            }
    
    def send_bulk_sms(
        self,
        suppliers: List[Dict]
    ) -> Dict:
        """
        Send bulk SMS to multiple suppliers.
        
        Args:
            suppliers: List of dicts with keys: receptor, name, company_name, category_name
        
        Returns:
            Dict with total_sent, total_failed, and details
        """
        results = {
            'total_sent': 0,
            'total_failed': 0,
            'details': []
        }
        
        for supplier in suppliers:
            result = self.send_sms(
                receptor=supplier['receptor'],
                name=supplier['name'],
                company_name=supplier['company_name'],
                category_name=supplier['category_name']
            )
            
            if result['success']:
                results['total_sent'] += 1
            else:
                results['total_failed'] += 1
            
            results['details'].append({
                'receptor': supplier['receptor'],
                'success': result['success'],
                'message': result['message']
            })
        
        return results


"""
OTP Delivery Abstraction Layer
This module provides an abstract base class for OTP senders and implementations
for different delivery channels (Local, SMS, Email, etc.)
"""
from abc import ABC, abstractmethod
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class OTPSender(ABC):
    """Abstract base class for OTP delivery services"""
    
    @abstractmethod
    def send_otp(self, code: str, recipient: str, purpose: str) -> dict:
        """
        Send OTP to recipient
        
        Args:
            code: The OTP code to send
            recipient: Phone number or email address
            purpose: Purpose of the OTP (login, password_reset, etc.)
        
        Returns:
            dict: Response with success status and optional metadata
        """
        pass


class LocalOTPSender(OTPSender):
    """
    Local OTP Sender for development
    Returns OTP in response and logs to console
    No external dependencies - zero cost for development
    """
    
    def send_otp(self, code: str, recipient: str, purpose: str) -> dict:
        """
        Send OTP locally (for development)
        
        Args:
            code: The OTP code
            recipient: Phone number
            purpose: Purpose of the OTP
        
        Returns:
            dict: Response with success status and the OTP code
        """
        logger.info(f"[LOCAL OTP] Code: {code} | Recipient: {recipient} | Purpose: {purpose}")
        print(f"\n{'='*60}")
        print(f"OTP CODE: {code}")
        print(f"Recipient: {recipient}")
        print(f"Purpose: {purpose}")
        print(f"{'='*60}\n")
        
        return {
            'success': True,
            'code': code,  # Return code for development
            'message': 'OTP generated successfully (local mode)',
            'delivery_method': 'local'
        }


class KavenegarOTPSender(OTPSender):
    """
    Kavenegar SMS OTP Sender for production
    Sends OTP codes via Kavenegar API using Lookup template
    """
    
    def send_otp(self, code: str, recipient: str, purpose: str) -> dict:
        """
        Send OTP via Kavenegar SMS API
        
        Args:
            code: The OTP code to send
            recipient: Phone number (must be in Iranian format: 09XXXXXXXXX)
            purpose: Purpose of the OTP (login, password_reset, etc.)
        
        Returns:
            dict: Response with success status and message
        """
        api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
        template_name = getattr(settings, 'KAVENEGAR_OTP_TEMPLATE_NAME', None)
        
        if not api_key:
            logger.error('KAVENEGAR_API_KEY not configured in settings')
            return {
                'success': False,
                'message': 'SMS service is not configured. Please contact support.',
                'delivery_method': 'kavenegar'
            }
        
        if not template_name:
            logger.error('KAVENEGAR_OTP_TEMPLATE_NAME not configured in settings')
            return {
                'success': False,
                'message': 'SMS template is not configured. Please contact support.',
                'delivery_method': 'kavenegar'
            }
        
        # Normalize phone number (remove spaces, dashes, etc.)
        phone = self._normalize_phone(recipient)
        
        # Prepare API URL
        base_url = f'https://api.kavenegar.com/v1/{api_key}/verify/lookup.json'
        
        # Prepare parameters
        # Template uses 1 token: the OTP code
        params = {
            'receptor': phone,
            'template': template_name,
            'token': code
        }
        
        try:
            # Make API request
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            # Check Kavenegar response structure
            # Kavenegar returns: {"return": {"status": 200, "message": "..."}, "entries": [...]}
            if result.get('return', {}).get('status') == 200:
                logger.info(f"OTP sent successfully via Kavenegar to {phone} (purpose: {purpose})")
                return {
                    'success': True,
                    'message': 'کد تأیید با موفقیت ارسال شد',
                    'delivery_method': 'kavenegar'
                }
            else:
                error_message = result.get('return', {}).get('message', 'Unknown error')
                logger.error(f'Kavenegar API error: {error_message} | Response: {result}')
                return {
                    'success': False,
                    'message': 'خطا در ارسال پیامک. لطفاً بعداً تلاش کنید.',
                    'delivery_method': 'kavenegar',
                    'error': error_message
                }
                
        except requests.exceptions.Timeout:
            logger.error(f'Kavenegar API timeout when sending OTP to {phone}')
            return {
                'success': False,
                'message': 'زمان ارسال پیامک به پایان رسید. لطفاً دوباره تلاش کنید.',
                'delivery_method': 'kavenegar'
            }
        except requests.exceptions.RequestException as e:
            logger.error(f'Kavenegar API network error: {str(e)}')
            return {
                'success': False,
                'message': 'خطا در اتصال به سرویس پیامک. لطفاً بعداً تلاش کنید.',
                'delivery_method': 'kavenegar'
            }
        except Exception as e:
            logger.error(f'Unexpected error sending OTP via Kavenegar: {str(e)}')
            return {
                'success': False,
                'message': 'خطای غیرمنتظره در ارسال پیامک. لطفاً با پشتیبانی تماس بگیرید.',
                'delivery_method': 'kavenegar'
            }
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number format for Kavenegar API"""
        import re
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


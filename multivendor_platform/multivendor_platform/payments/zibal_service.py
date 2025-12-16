"""
Zibal Payment Gateway Service
Integration with Zibal API for payment processing
"""
import requests
import logging
from django.conf import settings
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class ZibalServiceException(Exception):
    """Custom exception for Zibal service errors"""
    pass


class ZibalService:
    """Service class for Zibal payment gateway integration"""
    
    # Zibal Result Codes
    RESULT_CODES = {
        100: 'با موفقیت تایید شد',
        102: 'merchant یافت نشد',
        103: 'merchant غیرفعال',
        104: 'merchant نامعتبر',
        105: 'amount بایستی بزرگتر از 1,000 ریال باشد',
        106: 'callbackUrl نامعتبر می‌باشد',
        113: 'amount مبلغ تراکنش از سقف میزان تراکنش بیشتر است',
        201: 'قبلا تایید شده',
        202: 'سفارش پرداخت نشده یا ناموفق بوده است',
        203: 'trackId نامعتبر می‌باشد',
    }
    
    # Zibal Status Codes
    STATUS_CODES = {
        -1: 'در انتظار پردخت',
        -2: 'خطای داخلی',
        1: 'پرداخت شده - تاییدشده',
        2: 'پرداخت شده - تاییدنشده',
        3: 'لغوشده توسط کاربر',
        4: 'شماره کارت نامعتبر می‌باشد',
        5: 'موجودی حساب کافی نمی‌باشد',
        6: 'رمز واردشده اشتباه می‌باشد',
        7: 'تعداد درخواست‌ها بیش از حد مجاز می‌باشد',
        8: 'تعداد پرداخت اینترنتی روزانه بیش از حد مجاز می‌باشد',
        9: 'مبلغ پرداخت اینترنتی روزانه بیش از حد مجاز می‌باشد',
        10: 'صادرکننده‌ی کارت نامعتبر می‌باشد',
        11: 'خطای سوییچ',
        12: 'کارت قابل دسترسی نمی‌باشد',
    }
    
    def __init__(self):
        self.merchant = settings.ZIBAL_MERCHANT
        self.api_base = settings.ZIBAL_API_BASE
        self.site_url = settings.SITE_URL
    
    def request_payment(
        self,
        amount: int,
        callback_url: str,
        description: str = '',
        order_id: str = '',
        mobile: str = ''
    ) -> Tuple[bool, Dict]:
        """
        Step 1: Request payment from Zibal
        
        Args:
            amount: Amount in Rials (not Toman)
            callback_url: Callback URL for payment result
            description: Payment description
            order_id: Internal order ID
            mobile: User mobile number (optional)
        
        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        url = f"{self.api_base}/v1/request"
        
        payload = {
            "merchant": self.merchant,
            "amount": int(amount),
            "callbackUrl": callback_url,
        }
        
        if description:
            payload["description"] = description
        if order_id:
            payload["orderId"] = order_id
        if mobile:
            payload["mobile"] = mobile
        
        try:
            logger.info(f"Zibal request payment - amount: {amount}, order: {order_id}")
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            result_code = data.get('result')
            
            if result_code == 100:
                track_id = data.get('trackId')
                logger.info(f"Zibal payment requested successfully - trackId: {track_id}")
                return True, data
            else:
                error_msg = self.RESULT_CODES.get(result_code, f'Unknown error code: {result_code}')
                logger.error(f"Zibal request failed - code: {result_code}, msg: {error_msg}")
                return False, {"error": error_msg, "result": result_code}
        
        except requests.RequestException as e:
            logger.error(f"Zibal request exception: {str(e)}")
            return False, {"error": f"خطا در ارتباط با درگاه پرداخت: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error in Zibal request: {str(e)}")
            return False, {"error": f"خطای غیرمنتظره: {str(e)}"}
    
    def get_payment_url(self, track_id: str) -> str:
        """
        Step 2: Get payment gateway URL
        
        Args:
            track_id: Track ID received from request_payment
        
        Returns:
            Payment gateway URL
        """
        return f"{self.api_base}/start/{track_id}"
    
    def verify_payment(self, track_id: str) -> Tuple[bool, Dict]:
        """
        Step 3: Verify payment after callback
        
        Args:
            track_id: Track ID from callback
        
        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        url = f"{self.api_base}/v1/verify"
        
        payload = {
            "merchant": self.merchant,
            "trackId": int(track_id),
        }
        
        try:
            logger.info(f"Zibal verify payment - trackId: {track_id}")
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            result_code = data.get('result')
            
            if result_code == 100:
                logger.info(f"Zibal payment verified successfully - trackId: {track_id}")
                return True, data
            else:
                error_msg = self.RESULT_CODES.get(result_code, f'Unknown error code: {result_code}')
                logger.error(f"Zibal verify failed - code: {result_code}, msg: {error_msg}")
                return False, {"error": error_msg, "result": result_code, "raw_data": data}
        
        except requests.RequestException as e:
            logger.error(f"Zibal verify exception: {str(e)}")
            return False, {"error": f"خطا در تایید پرداخت: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error in Zibal verify: {str(e)}")
            return False, {"error": f"خطای غیرمنتظره: {str(e)}"}
    
    def inquiry_payment(self, track_id: str) -> Tuple[bool, Dict]:
        """
        Step 4: Inquiry payment status (optional)
        
        Args:
            track_id: Track ID to inquiry
        
        Returns:
            Tuple of (success: bool, response_data: dict)
        """
        url = f"{self.api_base}/v1/inquiry"
        
        payload = {
            "merchant": self.merchant,
            "trackId": int(track_id),
        }
        
        try:
            logger.info(f"Zibal inquiry payment - trackId: {track_id}")
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            result_code = data.get('result')
            
            if result_code == 100:
                logger.info(f"Zibal inquiry successful - trackId: {track_id}")
                return True, data
            else:
                error_msg = self.RESULT_CODES.get(result_code, f'Unknown error code: {result_code}')
                logger.warning(f"Zibal inquiry failed - code: {result_code}, msg: {error_msg}")
                return False, {"error": error_msg, "result": result_code}
        
        except requests.RequestException as e:
            logger.error(f"Zibal inquiry exception: {str(e)}")
            return False, {"error": f"خطا در استعلام پرداخت: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error in Zibal inquiry: {str(e)}")
            return False, {"error": f"خطای غیرمنتظره: {str(e)}"}
    
    def get_result_message(self, result_code: int) -> str:
        """Get Persian message for result code"""
        return self.RESULT_CODES.get(result_code, f'کد نامعتبر: {result_code}')
    
    def get_status_message(self, status_code: int) -> str:
        """Get Persian message for status code"""
        return self.STATUS_CODES.get(status_code, f'وضعیت نامعتبر: {status_code}')
    
    def is_successful_payment(self, status: int) -> bool:
        """Check if payment status is successful"""
        return status in [1, 2]  # 1: Paid-Verified, 2: Paid-Unverified


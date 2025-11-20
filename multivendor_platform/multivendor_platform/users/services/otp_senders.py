"""
OTP Delivery Abstraction Layer
This module provides an abstract base class for OTP senders and implementations
for different delivery channels (Local, SMS, Email, etc.)
"""
from abc import ABC, abstractmethod
import logging

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


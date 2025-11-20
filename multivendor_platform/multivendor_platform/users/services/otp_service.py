"""
OTP Service - Core business logic for OTP generation, validation, and management
"""
import secrets
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q, F
from ..models import OTP
from .otp_senders import OTPSender, LocalOTPSender
import logging

logger = logging.getLogger(__name__)


class OTPService:
    """Service class for OTP operations"""
    
    def __init__(self):
        """Initialize OTP service with configuration"""
        self.expiration_minutes = getattr(settings, 'OTP_EXPIRATION_MINUTES', 5)
        self.rate_limit_requests = getattr(settings, 'OTP_RATE_LIMIT_REQUESTS', 3)
        self.rate_limit_window_minutes = getattr(settings, 'OTP_RATE_LIMIT_WINDOW_MINUTES', 15)
        
        # Get sender class from settings
        sender_class_path = getattr(settings, 'OTP_SENDER_CLASS', 'users.services.otp_senders.LocalOTPSender')
        sender_class = self._get_sender_class(sender_class_path)
        self.sender = sender_class()
    
    def _get_sender_class(self, class_path: str):
        """Dynamically load sender class from settings"""
        try:
            module_path, class_name = class_path.rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            logger.warning(f"Failed to load OTP sender class {class_path}, using LocalOTPSender: {e}")
            return LocalOTPSender
    
    def _generate_code(self) -> str:
        """Generate a secure 6-digit numeric code"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number format"""
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
    
    def _get_phone_from_user_or_phone(self, user_or_phone):
        """Extract phone number from user object or phone string"""
        if isinstance(user_or_phone, User):
            # Try to get phone from user profile
            try:
                phone = user_or_phone.profile.phone
                if not phone:
                    phone = user_or_phone.username  # Fallback to username if phone not set
            except:
                phone = user_or_phone.username
            return self._normalize_phone(phone)
        else:
            return self._normalize_phone(str(user_or_phone))
    
    def is_rate_limited(self, user_or_phone, purpose: str) -> bool:
        """
        Check if user/phone is rate limited
        
        Args:
            user_or_phone: User object or phone number string
            purpose: Purpose of the OTP request
        
        Returns:
            bool: True if rate limited, False otherwise
        """
        phone = self._get_phone_from_user_or_phone(user_or_phone)
        
        # Calculate time window
        window_start = timezone.now() - timedelta(minutes=self.rate_limit_window_minutes)
        
        # Count recent OTP requests
        query = Q(phone=phone, purpose=purpose, created_at__gte=window_start)
        if isinstance(user_or_phone, User):
            query |= Q(user=user_or_phone, purpose=purpose, created_at__gte=window_start)
        
        recent_count = OTP.objects.filter(query).count()
        
        return recent_count >= self.rate_limit_requests
    
    def invalidate_old_otps(self, user_or_phone, purpose: str):
        """
        Invalidate old unused OTPs for the same user/phone and purpose
        
        Args:
            user_or_phone: User object or phone number string
            purpose: Purpose of the OTP
        """
        phone = self._get_phone_from_user_or_phone(user_or_phone)
        
        query = Q(phone=phone, purpose=purpose, is_used=False)
        if isinstance(user_or_phone, User):
            query |= Q(user=user_or_phone, purpose=purpose, is_used=False)
        
        OTP.objects.filter(query).update(is_used=True)
    
    def generate_otp(self, user_or_phone, purpose: str) -> dict:
        """
        Generate and send OTP
        
        Args:
            user_or_phone: User object or phone number string
            purpose: Purpose of the OTP (login, password_reset, etc.)
        
        Returns:
            dict: Response with success status and optional OTP code (for local mode)
        
        Raises:
            ValueError: If rate limited or invalid purpose
        """
        # Validate purpose
        valid_purposes = [choice[0] for choice in OTP.PURPOSE_CHOICES]
        if purpose not in valid_purposes:
            raise ValueError("خطایی در سیستم رخ داده است. لطفاً صفحه را رفرش کنید و دوباره تلاش کنید.")
        
        # Check rate limiting
        if self.is_rate_limited(user_or_phone, purpose):
            raise ValueError(
                f"شما در {self.rate_limit_window_minutes} دقیقه گذشته {self.rate_limit_requests} بار کد درخواست کرده‌اید. "
                f"لطفاً {self.rate_limit_window_minutes} دقیقه صبر کنید و سپس دوباره تلاش کنید. "
                "این محدودیت برای امنیت حساب شما اعمال شده است."
            )
        
        # Invalidate old OTPs
        self.invalidate_old_otps(user_or_phone, purpose)
        
        # Generate code
        code = self._generate_code()
        phone = self._get_phone_from_user_or_phone(user_or_phone)
        
        # Calculate expiration
        expires_at = timezone.now() + timedelta(minutes=self.expiration_minutes)
        
        # Create OTP record
        otp_obj = OTP.objects.create(
            user=user_or_phone if isinstance(user_or_phone, User) else None,
            phone=phone,
            code=code,
            purpose=purpose,
            expires_at=expires_at,
            attempts=0
        )
        
        # Send OTP via configured sender
        send_result = self.sender.send_otp(code, phone, purpose)
        
        logger.info(f"OTP generated for {phone} (purpose: {purpose})")
        
        return {
            'success': True,
            'otp_id': otp_obj.id,
            **send_result  # Include sender response (may contain code for local mode)
        }
    
    def verify_otp(self, code: str, user_or_phone, purpose: str, mark_as_used: bool = True) -> dict:
        """
        Verify OTP code
        
        Args:
            code: The OTP code to verify
            user_or_phone: User object or phone number string
            purpose: Purpose of the OTP
        
        Returns:
            dict: Response with success status and user (if login purpose)
        
        Raises:
            ValueError: If OTP is invalid, expired, or already used
        """
        phone = self._get_phone_from_user_or_phone(user_or_phone)
        
        # Find active OTP
        query = Q(phone=phone, purpose=purpose, is_used=False, code=code)
        if isinstance(user_or_phone, User):
            query |= Q(user=user_or_phone, purpose=purpose, is_used=False, code=code)
        
        try:
            otp_obj = OTP.objects.filter(query).order_by('-created_at').first()
        except OTP.DoesNotExist:
            otp_obj = None
        
        if not otp_obj:
            # Increment attempts for any matching OTP (for security tracking)
            OTP.objects.filter(
                Q(phone=phone, purpose=purpose) | 
                (Q(user=user_or_phone) if isinstance(user_or_phone, User) else Q())
            ).update(attempts=F('attempts') + 1)
            raise ValueError(
                "کد وارد شده صحیح نیست. لطفاً دقت کنید و کد 6 رقمی را به درستی وارد کنید. "
                "اگر کد را دریافت نکرده‌اید، می‌توانید دکمه 'ارسال مجدد کد' را بزنید."
            )
        
        # Check expiration
        if otp_obj.is_expired():
            otp_obj.is_used = True
            otp_obj.save()
            raise ValueError(
                f"متأسفانه کد تأیید شما منقضی شده است. کدهای تأیید فقط {self.expiration_minutes} دقیقه اعتبار دارند. "
                "لطفاً دکمه 'ارسال مجدد کد' را بزنید تا کد جدیدی برای شما ارسال شود."
            )
        
        # Check max attempts (brute force protection)
        max_attempts = 5
        if otp_obj.attempts >= max_attempts:
            otp_obj.is_used = True
            otp_obj.save()
            raise ValueError(
                "شما بیش از حد مجاز برای وارد کردن کد تلاش کرده‌اید. "
                "برای امنیت حساب شما، این کد دیگر قابل استفاده نیست. "
                "لطفاً دکمه 'ارسال مجدد کد' را بزنید تا کد جدیدی دریافت کنید."
            )
        
        # Mark as used (unless it's password_reset and we want to verify again later)
        if mark_as_used:
            otp_obj.is_used = True
        otp_obj.attempts += 1
        otp_obj.save()
        
        logger.info(f"OTP verified successfully for {phone} (purpose: {purpose}, marked_as_used: {mark_as_used})")
        
        result = {
            'success': True,
            'message': 'OTP verified successfully',
            'otp_id': otp_obj.id  # Return OTP ID for password reset flow
        }
        
        # If login purpose, return user
        if purpose == 'login' and otp_obj.user:
            result['user'] = otp_obj.user
        
        return result
    
    def cleanup_expired_otps(self):
        """Clean up expired OTPs (can be called by a periodic task)"""
        expired_count = OTP.objects.filter(
            expires_at__lt=timezone.now(),
            is_used=False
        ).update(is_used=True)
        
        logger.info(f"Cleaned up {expired_count} expired OTPs")
        return expired_count


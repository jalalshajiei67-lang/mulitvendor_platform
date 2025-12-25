import re
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Subcategory


def validate_iranian_mobile(value):
    """
    Validate Iranian mobile number format.
    Accepts: 09XXXXXXXXX, +98XXXXXXXXXX, 0098XXXXXXXXXX, 98XXXXXXXXXX, 9XXXXXXXXX
    """
    if not value:
        return
    
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-()]', '', str(value).strip())
    
    # Normalize to Iranian format (09XXXXXXXXX) for validation
    if cleaned.startswith('+98'):
        cleaned = '0' + cleaned[3:]
    elif cleaned.startswith('0098'):
        cleaned = '0' + cleaned[4:]
    elif cleaned.startswith('98'):
        cleaned = '0' + cleaned[2:]
    elif not cleaned.startswith('0') and cleaned.startswith('9'):
        cleaned = '0' + cleaned
    
    # Check if it's a valid Iranian mobile number (09XXXXXXXXX - 11 digits)
    if not re.match(r'^09\d{9}$', cleaned):
        raise ValidationError(
            _('شماره موبایل معتبر نیست. لطفاً شماره را به صورت صحیح وارد کنید (مثال: 09123456789)'),
            code='invalid_mobile'
        )


class Seller(models.Model):
    """
    Model for sellers in SMS newsletter system.
    This is independent from user sellers (vendors/suppliers).
    """
    name = models.CharField(
        max_length=200,
        verbose_name='نام فروشنده',
        help_text='نام فروشنده (الزامی)'
    )
    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='نام شرکت',
        help_text='نام شرکت (اختیاری)'
    )
    mobile_number = models.CharField(
        max_length=20,
        verbose_name='شماره موبایل',
        help_text='شماره موبایل برای ارسال پیامک (الزامی)',
        validators=[validate_iranian_mobile]
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='تلفن',
        help_text='شماره تلفن اضافی (اختیاری)'
    )
    working_fields = models.ManyToManyField(
        Subcategory,
        related_name='sellers',
        blank=True,
        verbose_name='حوزه‌های کاری',
        help_text='زیردسته‌بندی‌های مرتبط با این فروشنده'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'فروشنده'
        verbose_name_plural = 'فروشندگان'

    def __str__(self):
        return self.name

    def clean(self):
        """Normalize mobile number before saving"""
        super().clean()
        if self.mobile_number:
            # Remove spaces, dashes, parentheses
            cleaned = re.sub(r'[\s\-()]', '', str(self.mobile_number).strip())
            
            # Normalize to Iranian format (09XXXXXXXXX)
            if cleaned.startswith('+98'):
                cleaned = '0' + cleaned[3:]
            elif cleaned.startswith('0098'):
                cleaned = '0' + cleaned[4:]
            elif cleaned.startswith('98'):
                cleaned = '0' + cleaned[2:]
            elif not cleaned.startswith('0') and cleaned.startswith('9'):
                cleaned = '0' + cleaned
            
            # Validate format
            validate_iranian_mobile(cleaned)
            
            # Set normalized value
            self.mobile_number = cleaned

    def save(self, *args, **kwargs):
        """Override save to ensure mobile number is normalized"""
        self.full_clean()  # This will call clean() and validate
        super().save(*args, **kwargs)

    def get_working_fields_display(self):
        """Return comma-separated working fields names"""
        return ", ".join([wf.name for wf in self.working_fields.all()]) or '-'


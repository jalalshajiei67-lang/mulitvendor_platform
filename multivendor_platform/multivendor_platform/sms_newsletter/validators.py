"""
Validators for SMS Newsletter app
"""
import re
from django.core.exceptions import ValidationError


def validate_iranian_phone(value):
    """
    Validate Iranian phone number formats:
    - Mobile: 09123456789, 989123456789, +989123456789
    - Landline: 02112345678, 982112345678, +982112345678
    """
    if not value:
        return
    
    # Remove spaces and dashes
    cleaned = re.sub(r'[\s\-]', '', str(value))
    
    # Patterns for valid Iranian phone numbers
    mobile_patterns = [
        r'^09\d{9}$',  # 09123456789
        r'^989\d{9}$',  # 989123456789
        r'^\+989\d{9}$',  # +989123456789
    ]
    
    landline_patterns = [
        r'^0\d{10}$',  # 02112345678 (10 digits after 0)
        r'^98\d{10}$',  # 982112345678
        r'^\+98\d{10}$',  # +982112345678
    ]
    
    # Check mobile patterns
    for pattern in mobile_patterns:
        if re.match(pattern, cleaned):
            return
    
    # Check landline patterns
    for pattern in landline_patterns:
        if re.match(pattern, cleaned):
            return
    
    # If no pattern matches, raise validation error
    raise ValidationError(
        'شماره تلفن معتبر نیست. فرمت‌های مجاز: 09123456789، 02112345678، +989123456789'
    )





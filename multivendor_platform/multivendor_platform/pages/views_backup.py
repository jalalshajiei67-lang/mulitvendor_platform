from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import ShortLink, ShortLinkClick


def get_client_ip(request):
    """Get client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_device_type(request):
    """Detect device type from user agent"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
        return 'mobile'
    elif 'tablet' in user_agent or 'ipad' in user_agent:
        return 'tablet'
    elif 'mozilla' in user_agent or 'chrome' in user_agent or 'safari' in user_agent:
        return 'desktop'
    return 'unknown'


def short_link_redirect(request, short_code):
    """Handle short link redirect and track click"""
    short_link = get_object_or_404(ShortLink, short_code=short_code, is_active=True)
    
    # Track click
    ShortLinkClick.objects.create(
        short_link=short_link,
        ip_address=get_client_ip(request),
        device_type=get_device_type(request)
    )
    
    return redirect(short_link.target_url)

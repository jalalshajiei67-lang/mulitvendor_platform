from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import AboutPage, ContactPage, ShortLink, ShortLinkClick
from .serializers import AboutPageSerializer, ContactPageSerializer


class AboutPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='current')
    def current(self, request):
        """
        Get the current About Us page.
        Returns the single AboutPage instance (only one should exist).
        """
        try:
            about_page = AboutPage.objects.first()
            if not about_page:
                return Response(
                    {'detail': 'صفحه درباره ما هنوز ایجاد نشده است'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(about_page)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'detail': 'خطا در دریافت صفحه درباره ما'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContactPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactPage.objects.all()
    serializer_class = ContactPageSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='current')
    def current(self, request):
        """
        Get the current Contact Us page.
        Returns the single ContactPage instance (only one should exist).
        """
        try:
            contact_page = ContactPage.objects.first()
            if not contact_page:
                return Response(
                    {'detail': 'صفحه تماس با ما هنوز ایجاد نشده است'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(contact_page)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'detail': 'خطا در دریافت صفحه تماس با ما'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
    from django.conf import settings
    
    short_link = get_object_or_404(ShortLink, short_code=short_code, is_active=True)
    
    # Track click
    ShortLinkClick.objects.create(
        short_link=short_link,
        ip_address=get_client_ip(request),
        device_type=get_device_type(request)
    )
    
    # Build the target URL
    target_url = short_link.target_url
    
    # If the target URL is relative (starts with /), convert to absolute URL
    # pointing to the frontend domain
    if target_url.startswith('/'):
        # Get the main domain from SITE_URL setting
        site_url = getattr(settings, 'SITE_URL', 'https://indexo.ir')
        target_url = f"{site_url.rstrip('/')}{target_url}"
    
    return redirect(target_url)

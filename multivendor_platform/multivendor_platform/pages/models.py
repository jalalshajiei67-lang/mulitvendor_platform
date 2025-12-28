from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class AboutPage(models.Model):
    """
    About Us page with multilingual content and SEO fields.
    Only one instance should exist.
    """
    # Persian Content
    title_fa = models.CharField(
        max_length=200,
        verbose_name='عنوان (فارسی)',
        help_text='عنوان صفحه درباره ما به فارسی'
    )
    content_fa = HTMLField(
        verbose_name='محتوا (فارسی)',
        help_text='محتوای کامل صفحه درباره ما به فارسی'
    )
    
    # English Content
    title_en = models.CharField(
        max_length=200,
        verbose_name='Title (English)',
        help_text='About Us page title in English',
        blank=True,
        null=True
    )
    content_en = HTMLField(
        verbose_name='Content (English)',
        help_text='Full About Us page content in English',
        blank=True,
        null=True
    )
    
    # SEO Fields - Persian
    meta_title_fa = models.CharField(
        max_length=200,
        verbose_name='عنوان متا (فارسی)',
        help_text='عنوان SEO برای موتورهای جستجو (حداکثر 60 کاراکتر)',
        blank=True,
        null=True
    )
    meta_description_fa = models.TextField(
        max_length=300,
        verbose_name='توضیحات متا (فارسی)',
        help_text='توضیحات SEO برای موتورهای جستجو (حداکثر 160 کاراکتر)',
        blank=True,
        null=True
    )
    meta_keywords_fa = models.CharField(
        max_length=300,
        verbose_name='کلمات کلیدی متا (فارسی)',
        help_text='کلمات کلیدی را با کاما جدا کنید',
        blank=True,
        null=True
    )
    
    # SEO Fields - English
    meta_title_en = models.CharField(
        max_length=200,
        verbose_name='Meta Title (English)',
        help_text='SEO meta title for search engines (max 60 characters)',
        blank=True,
        null=True
    )
    meta_description_en = models.TextField(
        max_length=300,
        verbose_name='Meta Description (English)',
        help_text='SEO meta description for search engines (max 160 characters)',
        blank=True,
        null=True
    )
    meta_keywords_en = models.CharField(
        max_length=300,
        verbose_name='Meta Keywords (English)',
        help_text='Comma-separated keywords',
        blank=True,
        null=True
    )
    
    # Timestamps
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین بروزرسانی'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    class Meta:
        verbose_name = 'صفحه درباره ما'
        verbose_name_plural = 'صفحه درباره ما'
        db_table = 'pages_about'

    def __str__(self):
        return f"درباره ما - {self.title_fa}"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists - update existing instead of creating new"""
        if not self.pk and AboutPage.objects.exists():
            # If trying to create a new instance when one exists, update the existing one
            # Use the most recently updated instance (in case of duplicates from old bug)
            existing = AboutPage.objects.order_by('-updated_at').first()
            # Update all fields from self to existing instance
            for field in self._meta.fields:
                if field.name not in ['id', 'pk', 'created_at']:
                    setattr(existing, field.name, getattr(self, field.name, None))
            # Save the existing instance with force_update to avoid insert
            # Remove force_insert from kwargs to avoid conflict
            kwargs.pop('force_insert', None)
            return super(AboutPage, existing).save(force_update=True, *args, **kwargs)
        return super().save(*args, **kwargs)


class ContactPage(models.Model):
    """
    Contact Us page with multilingual content and SEO fields.
    Only one instance should exist.
    """
    # Persian Content
    title_fa = models.CharField(
        max_length=200,
        verbose_name='عنوان (فارسی)',
        help_text='عنوان صفحه تماس با ما به فارسی'
    )
    content_fa = HTMLField(
        verbose_name='محتوا (فارسی)',
        help_text='محتوای کامل صفحه تماس با ما به فارسی'
    )
    
    # Contact Information - Persian
    address_fa = models.TextField(
        verbose_name='آدرس (فارسی)',
        help_text='آدرس کامل دفتر یا مکان',
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='تلفن',
        help_text='شماره تلفن تماس',
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='ایمیل',
        help_text='آدرس ایمیل تماس',
        blank=True,
        null=True
    )
    working_hours_fa = models.CharField(
        max_length=200,
        verbose_name='ساعات کاری (فارسی)',
        help_text='ساعات کاری دفتر به فارسی',
        blank=True,
        null=True
    )
    
    # English Content
    title_en = models.CharField(
        max_length=200,
        verbose_name='Title (English)',
        help_text='Contact Us page title in English',
        blank=True,
        null=True
    )
    content_en = HTMLField(
        verbose_name='Content (English)',
        help_text='Full Contact Us page content in English',
        blank=True,
        null=True
    )
    
    # Contact Information - English
    address_en = models.TextField(
        verbose_name='Address (English)',
        help_text='Full office or location address',
        blank=True,
        null=True
    )
    working_hours_en = models.CharField(
        max_length=200,
        verbose_name='Working Hours (English)',
        help_text='Office working hours in English',
        blank=True,
        null=True
    )
    
    # SEO Fields - Persian
    meta_title_fa = models.CharField(
        max_length=200,
        verbose_name='عنوان متا (فارسی)',
        help_text='عنوان SEO برای موتورهای جستجو (حداکثر 60 کاراکتر)',
        blank=True,
        null=True
    )
    meta_description_fa = models.TextField(
        max_length=300,
        verbose_name='توضیحات متا (فارسی)',
        help_text='توضیحات SEO برای موتورهای جستجو (حداکثر 160 کاراکتر)',
        blank=True,
        null=True
    )
    meta_keywords_fa = models.CharField(
        max_length=300,
        verbose_name='کلمات کلیدی متا (فارسی)',
        help_text='کلمات کلیدی را با کاما جدا کنید',
        blank=True,
        null=True
    )
    
    # SEO Fields - English
    meta_title_en = models.CharField(
        max_length=200,
        verbose_name='Meta Title (English)',
        help_text='SEO meta title for search engines (max 60 characters)',
        blank=True,
        null=True
    )
    meta_description_en = models.TextField(
        max_length=300,
        verbose_name='Meta Description (English)',
        help_text='SEO meta description for search engines (max 160 characters)',
        blank=True,
        null=True
    )
    meta_keywords_en = models.CharField(
        max_length=300,
        verbose_name='Meta Keywords (English)',
        help_text='Comma-separated keywords',
        blank=True,
        null=True
    )
    
    # Timestamps
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین بروزرسانی'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    class Meta:
        verbose_name = 'صفحه تماس با ما'
        verbose_name_plural = 'صفحه تماس با ما'
        db_table = 'pages_contact'

    def __str__(self):
        return f"تماس با ما - {self.title_fa}"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists - update existing instead of creating new"""
        if not self.pk and ContactPage.objects.exists():
            # If trying to create a new instance when one exists, update the existing one
            # Use the most recently updated instance (in case of duplicates from old bug)
            existing = ContactPage.objects.order_by('-updated_at').first()
            # Update all fields from self to existing instance
            for field in self._meta.fields:
                if field.name not in ['id', 'pk', 'created_at']:
                    setattr(existing, field.name, getattr(self, field.name, None))
            # Save the existing instance with force_update to avoid insert
            # Remove force_insert from kwargs to avoid conflict
            kwargs.pop('force_insert', None)
            return super(ContactPage, existing).save(force_update=True, *args, **kwargs)
        return super().save(*args, **kwargs)


class Redirect(models.Model):
    """
    Manual redirect management for URL redirects.
    Allows admins to create custom redirects from old URLs to new URLs.
    """
    REDIRECT_TYPE_CHOICES = [
        ('301', '301 Permanent Redirect'),
        ('302', '302 Temporary Redirect'),
    ]
    
    # Source URL (the old URL that should redirect)
    from_path = models.CharField(
        max_length=500,
        verbose_name='از مسیر',
        help_text='مسیر قدیمی که باید به مسیر جدید هدایت شود (مثال: /old-page)',
        db_index=True,
        unique=True
    )
    
    # Destination URL (the new URL)
    to_path = models.CharField(
        max_length=500,
        verbose_name='به مسیر',
        help_text='مسیر جدید که باید به آن هدایت شود (مثال: /new-page یا https://example.com/page)',
    )
    
    # Redirect type
    redirect_type = models.CharField(
        max_length=3,
        choices=REDIRECT_TYPE_CHOICES,
        default='301',
        verbose_name='نوع هدایت',
        help_text='301 برای هدایت دائمی (بهتر برای SEO)، 302 برای هدایت موقت'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
        help_text='اگر غیرفعال باشد، این هدایت اعمال نخواهد شد'
    )
    
    # Notes for admin
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='یادداشت',
        help_text='یادداشت‌های اضافی درباره این هدایت'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین بروزرسانی'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='redirects_created',
        verbose_name='ایجاد شده توسط'
    )
    
    class Meta:
        verbose_name = 'URL Redirect'
        verbose_name_plural = 'URL Redirects'
        db_table = 'pages_redirect'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['from_path', 'is_active']),
        ]
    
    def __str__(self):
        status = '✓' if self.is_active else '✗'
        return f"{status} {self.from_path} → {self.to_path}"
    
    def clean(self):
        """Validate the redirect paths"""
        from django.core.exceptions import ValidationError
        
        # Ensure from_path starts with /
        if not self.from_path.startswith('/'):
            raise ValidationError({'from_path': 'مسیر باید با / شروع شود'})
        
        # Ensure to_path is either relative (starts with /) or absolute URL
        if not (self.to_path.startswith('/') or self.to_path.startswith('http://') or self.to_path.startswith('https://')):
            raise ValidationError({'to_path': 'مسیر باید با / یا http:// یا https:// شروع شود'})
    
    def save(self, *args, **kwargs):
        """Clean and save the redirect"""
        self.full_clean()
        super().save(*args, **kwargs)


class ShortLink(models.Model):
    """Marketing campaign short links with tracking"""
    short_code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='کد کوتاه',
        help_text='کد کوتاه برای لینک (مثال: summer-sale)'
    )
    target_url = models.CharField(
        max_length=500,
        verbose_name='آدرس هدف',
        help_text='آدرس صفحه داخلی (مثال: /products/special-offer)'
    )
    campaign_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='نام کمپین',
        help_text='نام کمپین برای شناسایی راحتتر'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال',
        help_text='اگر غیرفعال باشد، لینک کار نمیکند'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shortlinks_created',
        verbose_name='ایجاد شده توسط'
    )
    
    class Meta:
        verbose_name = 'لینک کوتاه'
        verbose_name_plural = 'لینکهای کوتاه'
        db_table = 'pages_shortlink'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['short_code', 'is_active'], name='pages_short_code_active_idx'),
        ]
    
    def __str__(self):
        status = '✓' if self.is_active else '✗'
        return f"{status} /s/{self.short_code} → {self.target_url}"
    
    def get_click_count(self):
        return self.clicks.count()
    
    def get_unique_visitors(self):
        return self.clicks.values('ip_address').distinct().count()


class ShortLinkClick(models.Model):
    """Track clicks on short links"""
    DEVICE_CHOICES = [
        ('mobile', 'موبایل'),
        ('tablet', 'تبلت'),
        ('desktop', 'دسکتاپ'),
        ('unknown', 'نامشخص'),
    ]
    
    short_link = models.ForeignKey(
        ShortLink,
        on_delete=models.CASCADE,
        related_name='clicks',
        verbose_name='لینک کوتاه'
    )
    ip_address = models.GenericIPAddressField(verbose_name='آیپی')
    device_type = models.CharField(
        max_length=20,
        choices=DEVICE_CHOICES,
        default='unknown',
        verbose_name='نوع دستگاه'
    )
    clicked_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='زمان کلیک')
    
    class Meta:
        verbose_name = 'کلیک لینک'
        verbose_name_plural = 'کلیکهای لینک'
        db_table = 'pages_shortlinkclick'
        ordering = ['-clicked_at']
        indexes = [
            models.Index(fields=['short_link', 'clicked_at'], name='pages_short_link_time_idx'),
            models.Index(fields=['ip_address', 'short_link'], name='pages_short_ip_link_idx'),
        ]
    
    def __str__(self):
        return f"{self.short_link.short_code} - {self.ip_address} - {self.clicked_at}"


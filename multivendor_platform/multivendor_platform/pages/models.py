from django.db import models
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
        """Ensure only one instance exists"""
        if not self.pk and AboutPage.objects.exists():
            # If trying to create a new instance when one exists, update the existing one
            existing = AboutPage.objects.first()
            self.pk = existing.pk
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
        """Ensure only one instance exists"""
        if not self.pk and ContactPage.objects.exists():
            # If trying to create a new instance when one exists, update the existing one
            existing = ContactPage.objects.first()
            self.pk = existing.pk
        return super().save(*args, **kwargs)


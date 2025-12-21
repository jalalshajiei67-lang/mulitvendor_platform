"""
Models for SMS Newsletter app
"""
from django.db import models
from django.core.validators import MinLengthValidator
from products.models import Subcategory
from .validators import validate_iranian_phone


class SupplierSMSNewsletter(models.Model):
    """
    Model for managing supplier SMS newsletter subscriptions.
    This is a manually managed list, isolated from seller/buyer users.
    """
    supplier_name = models.CharField(
        max_length=200,
        verbose_name='نام تامین‌کننده',
        help_text='نام شخص تامین‌کننده'
    )
    company_name = models.CharField(
        max_length=200,
        verbose_name='نام شرکت',
        help_text='نام شرکت تامین‌کننده'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='تلفن',
        help_text='شماره تلفن ثابت',
        validators=[validate_iranian_phone],
        blank=True,
        null=True
    )
    mobile = models.CharField(
        max_length=20,
        verbose_name='موبایل',
        help_text='شماره موبایل (برای ارسال پیامک)',
        validators=[validate_iranian_phone],
        unique=True
    )
    working_fields = models.ManyToManyField(
        Subcategory,
        related_name='supplier_newsletters',
        verbose_name='زمینه‌های کاری',
        help_text='زمینه‌های کاری تامین‌کننده (می‌توانید چند مورد انتخاب کنید)',
        blank=True
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
        verbose_name = 'تامین‌کننده خبرنامه پیامکی'
        verbose_name_plural = 'تامین‌کنندگان خبرنامه پیامکی'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.supplier_name} - {self.company_name}'
    
    def get_working_fields_display(self):
        """Return comma-separated list of working fields"""
        return ', '.join([field.name for field in self.working_fields.all()])
    get_working_fields_display.short_description = 'زمینه‌های کاری'


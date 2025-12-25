from django.contrib import admin
from .models import Seller


class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'mobile_number', 'phone', 'get_working_fields_count', 'created_at']
    list_filter = ['working_fields', 'created_at']
    search_fields = ['name', 'company_name', 'mobile_number', 'phone']
    filter_horizontal = ['working_fields']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('name', 'company_name', 'mobile_number', 'phone')
        }),
        ('حوزه‌های کاری', {
            'fields': ('working_fields',),
            'description': 'زیردسته‌بندی‌های مرتبط با این فروشنده را انتخاب کنید'
        }),
    )

    def get_working_fields_count(self, obj):
        """Display count of working fields"""
        count = obj.working_fields.count()
        return f'{count} حوزه کاری'
    get_working_fields_count.short_description = 'تعداد حوزه‌های کاری'


# Register the model
admin.site.register(Seller, SellerAdmin)


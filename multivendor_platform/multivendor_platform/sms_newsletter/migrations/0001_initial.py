# Generated migration for SMS Newsletter app

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0038_delete_subcategoryfeaturetemplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='نام فروشنده (الزامی)', max_length=200, verbose_name='نام فروشنده')),
                ('company_name', models.CharField(blank=True, help_text='نام شرکت (اختیاری)', max_length=200, null=True, verbose_name='نام شرکت')),
                ('mobile_number', models.CharField(help_text='شماره موبایل برای ارسال پیامک (الزامی)', max_length=20, verbose_name='شماره موبایل')),
                ('phone', models.CharField(blank=True, help_text='شماره تلفن اضافی (اختیاری)', max_length=20, null=True, verbose_name='تلفن')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('working_fields', models.ManyToManyField(blank=True, help_text='زیردسته‌بندی‌های مرتبط با این فروشنده', related_name='sellers', to='products.subcategory', verbose_name='حوزه‌های کاری')),
            ],
            options={
                'verbose_name': 'فروشنده',
                'verbose_name_plural': 'فروشندگان',
                'ordering': ['name'],
            },
        ),
    ]


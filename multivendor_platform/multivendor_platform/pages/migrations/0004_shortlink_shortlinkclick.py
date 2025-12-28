# Generated migration for ShortLink and ShortLinkClick models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0003_alter_redirect_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_code', models.CharField(db_index=True, help_text='کد کوتاه برای لینک (مثال: summer-sale)', max_length=100, unique=True, verbose_name='کد کوتاه')),
                ('target_url', models.CharField(help_text='آدرس صفحه داخلی (مثال: /products/special-offer)', max_length=500, verbose_name='آدرس هدف')),
                ('campaign_name', models.CharField(blank=True, help_text='نام کمپین برای شناسایی راحت‌تر', max_length=200, null=True, verbose_name='نام کمپین')),
                ('is_active', models.BooleanField(default=True, help_text='اگر غیرفعال باشد، لینک کار نمی‌کند', verbose_name='فعال')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shortlinks_created', to=settings.AUTH_USER_MODEL, verbose_name='ایجاد شده توسط')),
            ],
            options={
                'verbose_name': 'لینک کوتاه',
                'verbose_name_plural': 'لینک‌های کوتاه',
                'db_table': 'pages_shortlink',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['short_code', 'is_active'], name='pages_short_code_active_idx')],
            },
        ),
        migrations.CreateModel(
            name='ShortLinkClick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آی‌پی')),
                ('device_type', models.CharField(choices=[('mobile', 'موبایل'), ('tablet', 'تبلت'), ('desktop', 'دسکتاپ'), ('unknown', 'نامشخص')], default='unknown', max_length=20, verbose_name='نوع دستگاه')),
                ('clicked_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='زمان کلیک')),
                ('short_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clicks', to='pages.shortlink', verbose_name='لینک کوتاه')),
            ],
            options={
                'verbose_name': 'کلیک لینک',
                'verbose_name_plural': 'کلیک‌های لینک',
                'db_table': 'pages_shortlinkclick',
                'ordering': ['-clicked_at'],
                'indexes': [models.Index(fields=['short_link', 'clicked_at'], name='pages_short_link_time_idx'), models.Index(fields=['ip_address', 'short_link'], name='pages_short_ip_link_idx')],
            },
        ),
    ]

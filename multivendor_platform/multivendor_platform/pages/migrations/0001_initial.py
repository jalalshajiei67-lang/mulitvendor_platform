# Generated initial migration for pages app

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(help_text='عنوان صفحه درباره ما به فارسی', max_length=200, verbose_name='عنوان (فارسی)')),
                ('content_fa', tinymce.models.HTMLField(help_text='محتوای کامل صفحه درباره ما به فارسی', verbose_name='محتوا (فارسی)')),
                ('title_en', models.CharField(blank=True, help_text='About Us page title in English', max_length=200, null=True, verbose_name='Title (English)')),
                ('content_en', tinymce.models.HTMLField(blank=True, help_text='Full About Us page content in English', null=True, verbose_name='Content (English)')),
                ('meta_title_fa', models.CharField(blank=True, help_text='عنوان SEO برای موتورهای جستجو (حداکثر 60 کاراکتر)', max_length=200, null=True, verbose_name='عنوان متا (فارسی)')),
                ('meta_description_fa', models.TextField(blank=True, help_text='توضیحات SEO برای موتورهای جستجو (حداکثر 160 کاراکتر)', max_length=300, null=True, verbose_name='توضیحات متا (فارسی)')),
                ('meta_keywords_fa', models.CharField(blank=True, help_text='کلمات کلیدی را با کاما جدا کنید', max_length=300, null=True, verbose_name='کلمات کلیدی متا (فارسی)')),
                ('meta_title_en', models.CharField(blank=True, help_text='SEO meta title for search engines (max 60 characters)', max_length=200, null=True, verbose_name='Meta Title (English)')),
                ('meta_description_en', models.TextField(blank=True, help_text='SEO meta description for search engines (max 160 characters)', max_length=300, null=True, verbose_name='Meta Description (English)')),
                ('meta_keywords_en', models.CharField(blank=True, help_text='Comma-separated keywords', max_length=300, null=True, verbose_name='Meta Keywords (English)')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'صفحه درباره ما',
                'verbose_name_plural': 'صفحه درباره ما',
                'db_table': 'pages_about',
            },
        ),
        migrations.CreateModel(
            name='ContactPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(help_text='عنوان صفحه تماس با ما به فارسی', max_length=200, verbose_name='عنوان (فارسی)')),
                ('content_fa', tinymce.models.HTMLField(help_text='محتوای کامل صفحه تماس با ما به فارسی', verbose_name='محتوا (فارسی)')),
                ('address_fa', models.TextField(blank=True, help_text='آدرس کامل دفتر یا مکان', null=True, verbose_name='آدرس (فارسی)')),
                ('phone', models.CharField(blank=True, help_text='شماره تلفن تماس', max_length=50, null=True, verbose_name='تلفن')),
                ('email', models.EmailField(blank=True, help_text='آدرس ایمیل تماس', max_length=254, null=True, verbose_name='ایمیل')),
                ('working_hours_fa', models.CharField(blank=True, help_text='ساعات کاری دفتر به فارسی', max_length=200, null=True, verbose_name='ساعات کاری (فارسی)')),
                ('title_en', models.CharField(blank=True, help_text='Contact Us page title in English', max_length=200, null=True, verbose_name='Title (English)')),
                ('content_en', tinymce.models.HTMLField(blank=True, help_text='Full Contact Us page content in English', null=True, verbose_name='Content (English)')),
                ('address_en', models.TextField(blank=True, help_text='Full office or location address', null=True, verbose_name='Address (English)')),
                ('working_hours_en', models.CharField(blank=True, help_text='Office working hours in English', max_length=200, null=True, verbose_name='Working Hours (English)')),
                ('meta_title_fa', models.CharField(blank=True, help_text='عنوان SEO برای موتورهای جستجو (حداکثر 60 کاراکتر)', max_length=200, null=True, verbose_name='عنوان متا (فارسی)')),
                ('meta_description_fa', models.TextField(blank=True, help_text='توضیحات SEO برای موتورهای جستجو (حداکثر 160 کاراکتر)', max_length=300, null=True, verbose_name='توضیحات متا (فارسی)')),
                ('meta_keywords_fa', models.CharField(blank=True, help_text='کلمات کلیدی را با کاما جدا کنید', max_length=300, null=True, verbose_name='کلمات کلیدی متا (فارسی)')),
                ('meta_title_en', models.CharField(blank=True, help_text='SEO meta title for search engines (max 60 characters)', max_length=200, null=True, verbose_name='Meta Title (English)')),
                ('meta_description_en', models.TextField(blank=True, help_text='SEO meta description for search engines (max 160 characters)', max_length=300, null=True, verbose_name='Meta Description (English)')),
                ('meta_keywords_en', models.CharField(blank=True, help_text='Comma-separated keywords', max_length=300, null=True, verbose_name='Meta Keywords (English)')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'صفحه تماس با ما',
                'verbose_name_plural': 'صفحه تماس با ما',
                'db_table': 'pages_contact',
            },
        ),
    ]


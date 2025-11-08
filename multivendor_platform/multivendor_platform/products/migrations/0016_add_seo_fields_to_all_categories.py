# Generated manually on 2025-10-16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_add_product_comment'),
    ]

    operations = [
        # Add SEO fields to Department
        migrations.AddField(
            model_name='department',
            name='image_alt_text',
            field=models.CharField(blank=True, help_text='Alt text for the image (for SEO and accessibility)', max_length=125, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='canonical_url',
            field=models.URLField(blank=True, help_text='Canonical URL for SEO', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='schema_markup',
            field=models.TextField(blank=True, help_text='JSON-LD Schema markup for rich snippets', null=True),
        ),
        
        # Add SEO fields to Category
        migrations.AddField(
            model_name='category',
            name='image_alt_text',
            field=models.CharField(blank=True, help_text='Alt text for the image (for SEO and accessibility)', max_length=125, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='canonical_url',
            field=models.URLField(blank=True, help_text='Canonical URL for SEO', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='schema_markup',
            field=models.TextField(blank=True, help_text='JSON-LD Schema markup for rich snippets', null=True),
        ),
        
        # Add SEO fields to Subcategory
        migrations.AddField(
            model_name='subcategory',
            name='image_alt_text',
            field=models.CharField(blank=True, help_text='Alt text for the image (for SEO and accessibility)', max_length=125, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='canonical_url',
            field=models.URLField(blank=True, help_text='Canonical URL for SEO', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='schema_markup',
            field=models.TextField(blank=True, help_text='JSON-LD Schema markup for rich snippets', null=True),
        ),
    ]


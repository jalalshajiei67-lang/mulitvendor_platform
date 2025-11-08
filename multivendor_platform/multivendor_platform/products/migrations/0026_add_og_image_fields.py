# Generated manually - Add Open Graph image fields to Department, Category, Subcategory, and Product models

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_change_price_to_biginteger'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='og_image',
            field=models.ImageField(blank=True, help_text='Open Graph image for social media sharing', null=True, upload_to='department_og_images/'),
        ),
        migrations.AddField(
            model_name='category',
            name='og_image',
            field=models.ImageField(blank=True, help_text='Open Graph image for social media sharing', null=True, upload_to='category_og_images/'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='og_image',
            field=models.ImageField(blank=True, help_text='Open Graph image for social media sharing', null=True, upload_to='subcategory_og_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='og_image',
            field=models.ImageField(blank=True, help_text='Open Graph image for social media sharing', null=True, upload_to='product_og_images/'),
        ),
    ]





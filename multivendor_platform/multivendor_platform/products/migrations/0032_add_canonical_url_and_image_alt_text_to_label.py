# Generated manually - Add canonical_url and image_alt_text fields to Label model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_product_availability_status_product_condition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='canonical_url',
            field=models.URLField(blank=True, help_text='Canonical URL for SEO', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='label',
            name='image_alt_text',
            field=models.CharField(blank=True, help_text='Alt text for the image (for SEO and accessibility)', max_length=125, null=True),
        ),
    ]


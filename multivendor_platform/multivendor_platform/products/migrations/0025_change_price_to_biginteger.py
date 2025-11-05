# Generated manually - Change price field from PositiveIntegerField to PositiveBigIntegerField
# Supports at least 12 digits (up to 20 digits)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_change_price_to_integer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveBigIntegerField(help_text='Price in smallest currency unit (no decimals, supports at least 12 digits)'),
        ),
    ]


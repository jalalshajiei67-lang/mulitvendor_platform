# Generated manually - Change price field from DecimalField to PositiveIntegerField

from django.db import migrations, models


def convert_price_to_integer(apps, schema_editor):
    """Convert decimal prices to integers by rounding"""
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.all():
        if product.price:
            # Round decimal price to nearest integer
            product.price = int(round(float(product.price)))
            product.save()


def reverse_convert_price(apps, schema_editor):
    """Reverse migration - convert integers back to decimals"""
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.all():
        if product.price:
            # Convert integer back to decimal (add .00)
            product.price = float(product.price)
            product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_add_batch_reporting'),
    ]

    operations = [
        # Run data migration first
        migrations.RunPython(convert_price_to_integer, reverse_convert_price),
        # Then change the field type
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(help_text='Price in smallest currency unit (no decimals)'),
        ),
    ]


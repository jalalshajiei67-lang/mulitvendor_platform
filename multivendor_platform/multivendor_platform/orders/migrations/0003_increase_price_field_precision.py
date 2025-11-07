# Generated migration to increase price field precision for RFQ support
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_add_rfq_fields'),
    ]

    operations = [
        # Increase OrderItem.price precision to support large values
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price in smallest currency unit (supports large values for RFQ)', max_digits=20),
        ),
        # Increase OrderItem.subtotal precision
        migrations.AlterField(
            model_name='orderitem',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        # Increase Order.total_amount precision
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Total amount (null for RFQ, supports large values)', max_digits=20, null=True),
        ),
        # Increase Payment.amount precision
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]




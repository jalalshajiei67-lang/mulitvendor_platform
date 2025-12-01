# Generated migration for lead source and suppliers fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_increase_price_field_precision'),
        ('users', '0005_supplier'),  # Assuming this migration exists for Supplier model
    ]

    operations = [
        # Add email field
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, help_text='Email address (for RFQ)', max_length=254, null=True),
        ),
        # Add lead_source field
        migrations.AddField(
            model_name='order',
            name='lead_source',
            field=models.CharField(blank=True, choices=[('phone', 'Phone'), ('whatsapp', 'WhatsApp'), ('instagram', 'Instagram')], help_text='Source of the lead (phone, whatsapp, instagram)', max_length=20, null=True),
        ),
        # Add suppliers ManyToMany field
        migrations.AddField(
            model_name='order',
            name='suppliers',
            field=models.ManyToManyField(blank=True, help_text='Suppliers who should receive this RFQ', related_name='rfqs', to='users.supplier'),
        ),
    ]











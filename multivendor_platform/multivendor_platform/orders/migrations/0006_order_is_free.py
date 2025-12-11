from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_add_response_tracking_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_free',
            field=models.BooleanField(default=False, help_text='True if this RFQ/lead is free and visible to all sellers'),
        ),
    ]


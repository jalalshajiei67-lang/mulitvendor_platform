from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_is_free'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderVendorView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revealed_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_views', to='orders.order')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_rfqs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('order', 'vendor')},
            },
        ),
        migrations.AddIndex(
            model_name='ordervendorview',
            index=models.Index(fields=['vendor', 'order'], name='orders_orde_vendor__c8d667_idx'),
        ),
    ]


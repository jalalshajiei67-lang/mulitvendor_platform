# Generated migration for RFQ fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('products', '0019_remove_subcategory_departments'),  # Match the dependency from 0001_initial
    ]

    operations = [
        # Make buyer nullable for anonymous RFQ
        migrations.AlterField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(
                blank=True,
                help_text='User who created the order (null for anonymous RFQ)',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='orders',
                to='auth.user'
            ),
        ),
        # Make total_amount nullable for RFQ
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Total amount (null for RFQ)',
                max_digits=10,
                null=True
            ),
        ),
        # Make shipping fields nullable
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(blank=True, help_text='Shipping address (not required for RFQ)', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_phone',
            field=models.CharField(blank=True, help_text='Shipping phone (not required for RFQ)', max_length=20, null=True),
        ),
        # Add RFQ fields
        migrations.AddField(
            model_name='order',
            name='is_rfq',
            field=models.BooleanField(default=False, help_text='True if this is a Request for Quotation'),
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, help_text='Buyer first name (for RFQ)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(blank=True, help_text='Buyer last name (for RFQ)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='company_name',
            field=models.CharField(blank=True, help_text='Company name (for RFQ)', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, help_text='Phone number (for RFQ)', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='unique_needs',
            field=models.TextField(blank=True, help_text="Buyer's unique requirements/needs (for RFQ)", null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='category',
            field=models.ForeignKey(
                blank=True,
                help_text='Category for RFQ (if submitted from category page)',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='rfq_orders',
                to='products.category'
            ),
        ),
        # Create OrderImage model
        migrations.CreateModel(
            name='OrderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='order_images/')),
                ('alt_text', models.CharField(blank=True, help_text='Alt text for this image', max_length=125, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='orders.order')),
            ],
            options={
                'verbose_name': 'Order Image',
                'verbose_name_plural': 'Order Images',
                'ordering': ['created_at'],
            },
        ),
    ]


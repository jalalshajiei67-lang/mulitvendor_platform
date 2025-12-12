from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_ordervendorview'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='commission_amount',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text='Commission amount for this order',
                max_digits=20
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='commission_rate',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Commission rate applied (%)',
                max_digits=5,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='commission_paid',
            field=models.BooleanField(
                default=False,
                help_text='Whether commission has been deducted'
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='commission_paid_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When commission was paid/deducted',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='vendor_payout_amount',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Amount to be paid to vendor after commission',
                max_digits=20,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='vendor_paid',
            field=models.BooleanField(
                default=False,
                help_text='Whether vendor has been paid'
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='vendor_paid_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When vendor was paid',
                null=True
            ),
        ),
    ]

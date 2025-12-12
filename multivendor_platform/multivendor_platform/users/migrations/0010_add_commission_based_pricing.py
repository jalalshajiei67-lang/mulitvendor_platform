from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_commission_tier(apps, schema_editor):
    """Create the commission-based pricing tier."""
    PricingTier = apps.get_model('users', 'PricingTier')
    
    # Create commission tier if it doesn't exist
    PricingTier.objects.get_or_create(
        slug='commission',
        defaults={
            'name': 'Commission',
            'pricing_type': 'commission',
            'is_commission_based': True,
            'commission_rate_low': 5.00,  # 5% for under 1 billion Toman
            'commission_rate_high': 3.00,  # 3% for over 1 billion Toman
            'commission_threshold': 1000000000,  # 1 billion Toman
            'daily_customer_unlock_limit': 0,  # Unlimited
            'lead_exclusivity': 'shared',
            'allow_marketplace_visibility': True,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_pricingtier_vendorsubscription'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Add new fields to PricingTier
        migrations.AddField(
            model_name='pricingtier',
            name='pricing_type',
            field=models.CharField(
                choices=[('subscription', 'Subscription-based'), ('commission', 'Commission-based')],
                default='subscription',
                help_text='Type of pricing model',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='pricingtier',
            name='is_commission_based',
            field=models.BooleanField(
                default=False,
                help_text='True if this tier uses commission-based pricing'
            ),
        ),
        migrations.AddField(
            model_name='pricingtier',
            name='commission_rate_low',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Commission rate (%) for orders under threshold (e.g., 5.00 for 5%)',
                max_digits=5,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='pricingtier',
            name='commission_rate_high',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Commission rate (%) for orders above threshold (e.g., 3.00 for 3%)',
                max_digits=5,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='pricingtier',
            name='commission_threshold',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Threshold amount for commission rate change (e.g., 1000000000 for 1 billion Toman)',
                max_digits=20,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='pricingtier',
            name='monthly_price',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Monthly subscription price (if applicable)',
                max_digits=10,
                null=True
            ),
        ),
        
        # Add commission-related fields to VendorSubscription
        migrations.AddField(
            model_name='vendorsubscription',
            name='contract_signed',
            field=models.BooleanField(
                default=False,
                help_text='Whether vendor has signed the commission contract'
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='contract_signed_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When contract was signed',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='contract_document',
            field=models.FileField(
                blank=True,
                help_text='Signed contract document',
                null=True,
                upload_to='vendor_contracts/'
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='bank_guarantee_submitted',
            field=models.BooleanField(
                default=False,
                help_text='Whether bank guarantee has been submitted'
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='bank_guarantee_document',
            field=models.FileField(
                blank=True,
                help_text='Bank guarantee document',
                null=True,
                upload_to='bank_guarantees/'
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='bank_guarantee_amount',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Amount of bank guarantee',
                max_digits=20,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='bank_guarantee_expiry',
            field=models.DateField(
                blank=True,
                help_text='Bank guarantee expiry date',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='terms_accepted',
            field=models.BooleanField(
                default=False,
                help_text='Whether vendor accepted terms and conditions'
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='terms_accepted_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When terms were accepted',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='admin_approved',
            field=models.BooleanField(
                default=False,
                help_text='Whether admin has approved commission plan activation'
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='admin_approved_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When admin approved',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='admin_approved_by',
            field=models.ForeignKey(
                blank=True,
                help_text='Admin who approved',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='approved_subscriptions',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='rejection_reason',
            field=models.TextField(
                blank=True,
                help_text='Reason for rejection if not approved',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='total_commission_charged',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text='Total commission charged to vendor',
                max_digits=20
            ),
        ),
        migrations.AddField(
            model_name='vendorsubscription',
            name='total_sales_volume',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text='Total sales volume for commission calculation',
                max_digits=20
            ),
        ),
        
        # Create commission tier
        migrations.RunPython(create_commission_tier, migrations.RunPython.noop),
    ]

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_free_tier_and_subscriptions(apps, schema_editor):
    PricingTier = apps.get_model('users', 'PricingTier')
    VendorSubscription = apps.get_model('users', 'VendorSubscription')
    UserProfile = apps.get_model('users', 'UserProfile')

    free_tier, _ = PricingTier.objects.get_or_create(
        slug='free',
        defaults={
            'name': 'Free',
            'daily_customer_unlock_limit': 1,
            'lead_exclusivity': 'shared',
            'allow_marketplace_visibility': True,
        },
    )

    vendor_profiles = UserProfile.objects.filter(role__in=['seller', 'both']).select_related('user')
    for profile in vendor_profiles:
        # Ensure each vendor has a subscription
        VendorSubscription.objects.get_or_create(
            user_id=profile.user_id,
            defaults={
                'tier': free_tier,
                'is_active': True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_add_review_flags'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PricingTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Unique machine-readable identifier', max_length=50, unique=True)),
                ('name', models.CharField(help_text='Display name for the tier', max_length=100)),
                ('daily_customer_unlock_limit', models.PositiveIntegerField(default=1, help_text='How many new customers can be unlocked in a rolling 24h window (0 for unlimited).')),
                ('allow_marketplace_visibility', models.BooleanField(default=True, help_text='If false, products stay hidden from marketplace regardless of other flags.')),
                ('lead_exclusivity', models.CharField(choices=[('shared', 'Shared lead (non-exclusive)'), ('exclusive', 'Exclusive after claim')], default='shared', help_text='Defines whether leads become exclusive when revealed at this tier.', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Pricing Tier',
                'verbose_name_plural': 'Pricing Tiers',
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='VendorSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, help_text='Optional expiration for paid plans', null=True)),
                ('last_customer_unlock_at', models.DateTimeField(blank=True, help_text='Last time a new customer was unlocked', null=True)),
                ('total_customer_unlocks', models.PositiveIntegerField(default=0, help_text='Total unlocks ever made by this vendor')),
                ('is_active', models.BooleanField(default=True)),
                ('tier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='users.pricingtier')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_subscription', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vendor Subscription',
                'verbose_name_plural': 'Vendor Subscriptions',
            },
        ),
        migrations.RunPython(create_free_tier_and_subscriptions, migrations.RunPython.noop),
    ]

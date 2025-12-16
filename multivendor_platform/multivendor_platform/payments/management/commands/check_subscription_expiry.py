"""
Management command to check and handle expired premium subscriptions
Run this daily via cron or Celery Beat
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import VendorSubscription, PricingTier
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check for expired premium subscriptions and revert to free tier'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        now = timezone.now()
        
        # Find expired subscriptions
        expired_subscriptions = VendorSubscription.objects.filter(
            is_active=True,
            expires_at__isnull=False,
            expires_at__lte=now
        ).exclude(
            tier__is_commission_based=True  # Don't expire commission-based plans
        )
        
        count = expired_subscriptions.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No expired subscriptions found'))
            return
        
        self.stdout.write(f'Found {count} expired subscription(s)')
        
        # Get free tier
        free_tier = PricingTier.get_default_free()
        
        for subscription in expired_subscriptions:
            user = subscription.user
            old_tier = subscription.tier
            
            if dry_run:
                self.stdout.write(
                    f'[DRY RUN] Would revert {user.username} from {old_tier.name} to Free tier'
                )
            else:
                try:
                    # Revert to free tier
                    subscription.tier = free_tier
                    subscription.expires_at = None
                    subscription.is_active = True
                    subscription.save()
                    
                    logger.info(f'Reverted {user.username} (ID: {user.id}) from {old_tier.name} to Free tier')
                    self.stdout.write(
                        self.style.WARNING(
                            f'Reverted {user.username} from {old_tier.name} to Free tier'
                        )
                    )
                except Exception as e:
                    logger.error(f'Error reverting subscription for {user.username}: {str(e)}')
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error reverting {user.username}: {str(e)}'
                        )
                    )
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed {count} expired subscription(s)'
                )
            )


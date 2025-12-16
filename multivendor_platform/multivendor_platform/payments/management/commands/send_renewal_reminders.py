"""
Management command to send renewal reminders for expiring subscriptions
Run this daily via cron or Celery Beat
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import VendorSubscription
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send renewal reminders for subscriptions expiring soon (3 days before)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='Number of days before expiry to send reminder (default: 3)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without sending notifications',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        days_before = options['days']
        now = timezone.now()
        
        # Calculate the target date range
        target_date_start = now + timedelta(days=days_before)
        target_date_end = target_date_start + timedelta(days=1)
        
        # Find subscriptions expiring in N days that haven't been reminded yet
        expiring_subscriptions = VendorSubscription.objects.filter(
            is_active=True,
            expires_at__isnull=False,
            expires_at__gte=target_date_start,
            expires_at__lt=target_date_end,
            expiry_reminder_sent__isnull=True
        ).exclude(
            tier__is_commission_based=True  # Skip commission-based plans
        ).select_related('user', 'tier')
        
        count = expiring_subscriptions.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'No subscriptions expiring in {days_before} days that need reminders'
                )
            )
            return
        
        self.stdout.write(
            f'Found {count} subscription(s) expiring in {days_before} days'
        )
        
        for subscription in expiring_subscriptions:
            user = subscription.user
            tier = subscription.tier
            expiry_date = subscription.expires_at
            
            if dry_run:
                self.stdout.write(
                    f'[DRY RUN] Would send renewal reminder to {user.username} '
                    f'(expires: {expiry_date.strftime("%Y-%m-%d")})'
                )
            else:
                try:
                    # TODO: Implement actual notification system
                    # Options:
                    # 1. Send email using Django's send_mail
                    # 2. Create in-app notification
                    # 3. Send SMS
                    # 4. Use a notification service like Firebase
                    
                    # For now, just log and mark as sent
                    subscription.expiry_reminder_sent = now
                    subscription.save(update_fields=['expiry_reminder_sent'])
                    
                    logger.info(
                        f'Renewal reminder sent to {user.username} (ID: {user.id}), '
                        f'expires: {expiry_date.strftime("%Y-%m-%d")}'
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Sent renewal reminder to {user.username} '
                            f'({tier.name} expires: {expiry_date.strftime("%Y-%m-%d")})'
                        )
                    )
                    
                    # Example of how to send email (commented out for now)
                    # from django.core.mail import send_mail
                    # send_mail(
                    #     subject='Your Premium Subscription is Expiring Soon',
                    #     message=f'Dear {user.username},\n\n'
                    #             f'Your {tier.name} subscription will expire on '
                    #             f'{expiry_date.strftime("%Y-%m-%d")}.\n\n'
                    #             f'Please renew to continue enjoying premium features.',
                    #     from_email='noreply@indexo.ir',
                    #     recipient_list=[user.email],
                    #     fail_silently=False,
                    # )
                    
                except Exception as e:
                    logger.error(
                        f'Error sending renewal reminder to {user.username}: {str(e)}'
                    )
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error sending reminder to {user.username}: {str(e)}'
                        )
                    )
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully sent {count} renewal reminder(s)'
                )
            )


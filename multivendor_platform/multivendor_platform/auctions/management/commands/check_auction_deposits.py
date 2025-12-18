"""
Management command to check for expired auction deposits and forfeit them
Runs via cron job (every hour)
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from auctions.models import AuctionRequest, Bid, AuctionDepositPayment, AuctionNotification
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check for expired auction deposits and forfeit them (72-hour rule)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making changes (for testing)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        now = timezone.now()
        
        # First, check for 48-hour warnings
        warning_cutoff = now - timedelta(hours=48)
        warning_auctions = AuctionRequest.objects.filter(
            status='closed',
            closed_at__lt=warning_cutoff,
            closed_at__gte=now - timedelta(hours=72),  # Between 48 and 72 hours
            winner__isnull=True,
            deposit_status='held_in_escrow'
        ).select_related('deposit_payment_detail', 'buyer')
        
        # Check if warning already sent
        for auction in warning_auctions:
            if not AuctionNotification.objects.filter(
                auction=auction,
                notification_type='deposit_forfeiture_warning'
            ).exists():
                if not dry_run:
                    AuctionNotification.objects.create(
                        auction=auction,
                        user=auction.buyer,
                        notification_type='deposit_forfeiture_warning',
                        message=f'هشدار: شما ۴۸ ساعت فرصت دارید تا برنده مناقصه #{auction.id} را انتخاب کنید، در غیر این صورت واریز شما ضبط خواهد شد.'
                    )
                    self.stdout.write(f'  ✓ Warning sent for Auction #{auction.id}')
                else:
                    self.stdout.write(f'  [DRY RUN] Would send warning for Auction #{auction.id}')
        
        # Find auctions that:
        # 1. Are closed (status='closed')
        # 2. Closed more than 72 hours ago
        # 3. Buyer hasn't selected a winner (winner is None)
        # 4. Deposit status is 'held_in_escrow'
        cutoff_time = now - timedelta(hours=72)
        
        expired_auctions = AuctionRequest.objects.filter(
            status='closed',
            closed_at__lt=cutoff_time,
            winner__isnull=True,
            deposit_status='held_in_escrow'
        ).select_related('deposit_payment_detail', 'buyer').prefetch_related('bids')
        
        count = expired_auctions.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No expired deposits found'))
            return
        
        self.stdout.write(f'Found {count} auction(s) with expired deposits')
        
        for auction in expired_auctions:
            self.stdout.write(f'\nProcessing Auction #{auction.id}')
            
            if not auction.deposit_payment_detail:
                self.stdout.write(self.style.WARNING(f'  No deposit payment found, skipping'))
                continue
            
            deposit_amount = auction.deposit_payment_detail.amount
            
            # Get top 2 bidders (by price, lowest first for reverse auction)
            bids = auction.bids.order_by('price')[:2]
            
            if not bids:
                self.stdout.write(self.style.WARNING(f'  No bids found, skipping'))
                continue
            
            # Calculate split:
            # 50% to platform (admin fee)
            # 25% to top bidder
            # 25% to second bidder (if exists)
            platform_fee = deposit_amount * Decimal('0.5')
            bidder_1_amount = deposit_amount * Decimal('0.25')
            bidder_2_amount = deposit_amount * Decimal('0.25') if len(bids) > 1 else Decimal('0')
            
            if dry_run:
                self.stdout.write(f'  [DRY RUN] Would forfeit deposit:')
                self.stdout.write(f'    Platform fee: {platform_fee} Toman')
                self.stdout.write(f'    Bidder #1 ({bids[0].seller.username}): {bidder_1_amount} Toman')
                if len(bids) > 1:
                    self.stdout.write(f'    Bidder #2 ({bids[1].seller.username}): {bidder_2_amount} Toman')
                self.stdout.write(f'    Mark auction as abandoned')
            else:
                # Update deposit payment status
                payment = auction.deposit_payment_detail
                payment.status = 'forfeited'
                payment.save(update_fields=['status'])
                
                # Update auction status
                auction.status = 'abandoned'
                auction.deposit_status = 'forfeited'
                auction.save(update_fields=['status', 'deposit_status'])
                
                # Create notifications
                # Notify buyer
                AuctionNotification.objects.create(
                    auction=auction,
                    user=auction.buyer,
                    notification_type='deposit_forfeited',
                    message=f'Your deposit for auction #{auction.id} has been forfeited because you did not select a winner within 72 hours.'
                )
                
                # Notify bidders
                for idx, bid in enumerate(bids, 1):
                    amount = bidder_1_amount if idx == 1 else bidder_2_amount
                    AuctionNotification.objects.create(
                        auction=auction,
                        user=bid.seller,
                        notification_type='deposit_forfeited',
                        message=f'You received {amount} Toman compensation for auction #{auction.id} as the buyer did not select a winner.'
                    )
                
                self.stdout.write(self.style.SUCCESS(f'  ✓ Forfeited deposit for Auction #{auction.id}'))
                self.stdout.write(f'    Platform: {platform_fee} Toman')
                self.stdout.write(f'    Bidder #1: {bidder_1_amount} Toman')
                if len(bids) > 1:
                    self.stdout.write(f'    Bidder #2: {bidder_2_amount} Toman')
        
        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f'\n✓ Processed {count} auction(s)'))
        else:
            self.stdout.write(self.style.WARNING(f'\n[DRY RUN] Would process {count} auction(s)'))


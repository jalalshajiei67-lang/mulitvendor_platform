# users/management/commands/sync_contacts_from_orders.py
from django.core.management.base import BaseCommand
from django.db.models import Q
from orders.models import Order, OrderItem
from users.models import SellerContact


class Command(BaseCommand):
    help = 'Auto-create CRM contacts from existing orders/RFQs for sellers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually creating contacts',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No contacts will be created')
            )
        
        # Get all orders that have buyer information
        orders = Order.objects.filter(
            Q(is_rfq=True) | Q(buyer__isnull=False)
        ).select_related('buyer').prefetch_related('items__seller')
        
        created_count = 0
        skipped_count = 0
        error_count = 0
        
        for order in orders:
            # Get sellers who have items in this order
            order_items = order.items.all()
            sellers = set()
            
            for item in order_items:
                if item.seller:
                    sellers.add(item.seller)
                elif item.product and item.product.vendor:
                    sellers.add(item.product.vendor)
            
            if not sellers:
                continue
            
            # Extract contact information
            if order.is_rfq:
                # RFQ has buyer info in order fields
                first_name = order.first_name
                last_name = order.last_name
                company_name = order.company_name
                phone = order.phone_number
                email = order.email
            else:
                # Regular order has buyer as User
                if not order.buyer:
                    continue
                first_name = order.buyer.first_name
                last_name = order.buyer.last_name
                company_name = None
                phone = order.buyer.username if order.buyer.username else None
                email = order.buyer.email
            
            # Skip if no contact info
            if not (first_name or last_name or phone or email):
                skipped_count += 1
                continue
            
            # Create contact for each seller
            for seller in sellers:
                try:
                    # Check if contact already exists (by phone or email)
                    existing_contact = None
                    if phone:
                        existing_contact = SellerContact.objects.filter(
                            seller=seller, phone=phone
                        ).first()
                    if not existing_contact and email:
                        existing_contact = SellerContact.objects.filter(
                            seller=seller, email=email
                        ).first()
                    
                    if existing_contact:
                        # Update source_order if not set
                        if not existing_contact.source_order:
                            if not dry_run:
                                existing_contact.source_order = order
                                existing_contact.save(update_fields=['source_order'])
                            self.stdout.write(
                                f'  - Contact already exists for {seller.username}: {first_name} {last_name}'
                            )
                        skipped_count += 1
                        continue
                    
                    # Create new contact
                    if not dry_run:
                        contact = SellerContact.objects.create(
                            seller=seller,
                            first_name=first_name or '',
                            last_name=last_name or '',
                            company_name=company_name,
                            phone=phone or '',
                            email=email,
                            source_order=order
                        )
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✓ Created contact for {seller.username}: {first_name} {last_name} (from order {order.order_number})'
                            )
                        )
                    else:
                        created_count += 1
                        self.stdout.write(
                            f'  - Would create contact for {seller.username}: {first_name} {last_name} (from order {order.order_number})'
                        )
                        
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f'  ✗ Failed to create contact for seller {seller.username} from order {order.order_number}: {e}'
                        )
                    )
        
        self.stdout.write('\n' + '='*60)
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would create {created_count} contact(s)')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Successfully created {created_count} contact(s)')
            )
        self.stdout.write(f'  Skipped (already exists): {skipped_count}')
        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(f'  Errors: {error_count}')
            )


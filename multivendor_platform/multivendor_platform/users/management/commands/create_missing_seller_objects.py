"""
Management command to create missing VendorProfile and Supplier objects for sellers.
This fixes existing users who registered as sellers but don't have all required objects.

Usage:
    python manage.py create_missing_seller_objects
    python manage.py create_missing_seller_objects --dry-run
"""
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from users.models import UserProfile, VendorProfile, Supplier, VendorSubscription


class Command(BaseCommand):
    help = 'Create missing VendorProfile and Supplier objects for sellers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating anything',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Find all users with seller or both role
        seller_profiles = UserProfile.objects.filter(role__in=['seller', 'both']).select_related('user')
        
        self.stdout.write(f"Found {seller_profiles.count()} seller profiles")
        
        missing_vendor_profiles = []
        missing_suppliers = []
        missing_subscriptions = []
        
        for profile in seller_profiles:
            user = profile.user
            
            # Check VendorProfile
            try:
                vendor_profile = user.vendor_profile
            except VendorProfile.DoesNotExist:
                missing_vendor_profiles.append(user)
                vendor_profile = None
            
            # Check Supplier
            try:
                supplier = user.supplier
            except Supplier.DoesNotExist:
                missing_suppliers.append(user)
            
            # Check VendorSubscription
            if vendor_profile:
                try:
                    subscription = user.vendor_subscription
                except VendorSubscription.DoesNotExist:
                    missing_subscriptions.append(user)
        
        # Report findings
        self.stdout.write(self.style.WARNING(f"\nMissing objects:"))
        self.stdout.write(f"  - VendorProfiles: {len(missing_vendor_profiles)}")
        self.stdout.write(f"  - Suppliers: {len(missing_suppliers)}")
        self.stdout.write(f"  - VendorSubscriptions: {len(missing_subscriptions)}")
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nDry run complete. Use without --dry-run to create objects.'))
            return
        
        # Create missing objects
        created_vendor_profiles = 0
        created_suppliers = 0
        created_subscriptions = 0
        errors = []
        
        # Create missing VendorProfiles
        for user in missing_vendor_profiles:
            try:
                with transaction.atomic():
                    store_name = self._generate_unique_store_name(user.username)
                    vendor_profile = VendorProfile.objects.create(
                        user=user,
                        store_name=store_name,
                        description=''
                    )
                    created_vendor_profiles += 1
                    self.stdout.write(self.style.SUCCESS(f"✓ Created VendorProfile for {user.username} (ID: {user.id})"))
            except IntegrityError as e:
                errors.append(f"Failed to create VendorProfile for {user.username}: {e}")
                self.stdout.write(self.style.ERROR(f"✗ Failed to create VendorProfile for {user.username}: {e}"))
            except Exception as e:
                errors.append(f"Unexpected error creating VendorProfile for {user.username}: {e}")
                self.stdout.write(self.style.ERROR(f"✗ Unexpected error for {user.username}: {e}"))
        
        # Create missing Suppliers
        for user in missing_suppliers:
            try:
                with transaction.atomic():
                    # Get vendor profile to use store name
                    try:
                        vendor_profile = user.vendor_profile
                        company_name = vendor_profile.store_name
                    except VendorProfile.DoesNotExist:
                        company_name = f"شرکت {user.get_full_name() or user.username}"
                    
                    supplier = Supplier.objects.create(
                        vendor=user,
                        name=company_name,
                        is_active=True,
                    )
                    created_suppliers += 1
                    self.stdout.write(self.style.SUCCESS(f"✓ Created Supplier for {user.username} (ID: {user.id})"))
            except IntegrityError as e:
                errors.append(f"Failed to create Supplier for {user.username}: {e}")
                self.stdout.write(self.style.ERROR(f"✗ Failed to create Supplier for {user.username}: {e}"))
            except Exception as e:
                errors.append(f"Unexpected error creating Supplier for {user.username}: {e}")
                self.stdout.write(self.style.ERROR(f"✗ Unexpected error for {user.username}: {e}"))
        
        # Create missing VendorSubscriptions
        for user in missing_subscriptions:
            try:
                # Use the class method which handles creation
                subscription = VendorSubscription.for_user(user)
                created_subscriptions += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created VendorSubscription for {user.username} (ID: {user.id})"))
            except Exception as e:
                errors.append(f"Failed to create VendorSubscription for {user.username}: {e}")
                self.stdout.write(self.style.ERROR(f"✗ Failed to create VendorSubscription for {user.username}: {e}"))
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS("SUMMARY"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))
        self.stdout.write(f"Created VendorProfiles: {created_vendor_profiles}")
        self.stdout.write(f"Created Suppliers: {created_suppliers}")
        self.stdout.write(f"Created VendorSubscriptions: {created_subscriptions}")
        
        if errors:
            self.stdout.write(self.style.ERROR(f"\nErrors encountered: {len(errors)}"))
            for error in errors:
                self.stdout.write(self.style.ERROR(f"  - {error}"))
        else:
            self.stdout.write(self.style.SUCCESS("\n✓ All objects created successfully!"))
    
    def _generate_unique_store_name(self, username):
        """Generate a unique store name using UUID"""
        unique_suffix = uuid.uuid4().hex[:6]
        base_name = f"فروشگاه_{username}_{unique_suffix}"
        
        # Ensure uniqueness
        counter = 1
        store_name = base_name
        while VendorProfile.objects.filter(store_name=store_name).exists():
            store_name = f"{base_name}_{counter}"
            counter += 1
        
        return store_name


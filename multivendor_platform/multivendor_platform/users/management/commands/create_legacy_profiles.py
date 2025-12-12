# users/management/commands/create_legacy_profiles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile


class Command(BaseCommand):
    help = 'Create UserProfile for all User objects that do not have one (legacy users)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually creating profiles',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find all users without a UserProfile
        users_without_profile = User.objects.filter(profile__isnull=True)
        count = users_without_profile.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('✓ All users already have UserProfile. No action needed.')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'Found {count} user(s) without UserProfile')
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No profiles will be created')
            )
            for user in users_without_profile[:10]:  # Show first 10
                self.stdout.write(f'  - Would create profile for: {user.username} (ID: {user.id})')
            if count > 10:
                self.stdout.write(f'  ... and {count - 10} more')
            return
        
        # Create profiles
        created_count = 0
        for user in users_without_profile:
            try:
                UserProfile.objects.create(
                    user=user,
                    role='buyer',  # Safe default role
                    phone=''  # Empty phone, not populated with username
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Created profile for user: {user.username} (ID: {user.id})')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Failed to create profile for user {user.username} (ID: {user.id}): {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count} UserProfile(s)')
        )
        
        # Clean up phone field data
        self.stdout.write('\nCleaning up phone field data...')
        profiles_with_phone_as_username = UserProfile.objects.filter(
            phone__isnull=False
        ).exclude(phone='')
        
        cleaned_count = 0
        for profile in profiles_with_phone_as_username:
            if profile.phone == profile.user.username:
                profile.phone = ''
                profile.save()
                cleaned_count += 1
        
        if cleaned_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Cleaned up {cleaned_count} profile(s) where phone == username')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✓ No phone fields need cleanup')
            )




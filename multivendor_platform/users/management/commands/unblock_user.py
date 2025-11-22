from django.core.management.base import BaseCommand
from users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Unblock a user by username or phone number'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Username or phone number of the user to unblock'
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all blocked users'
        )

    def handle(self, *args, **options):
        if options['list']:
            blocked_profiles = UserProfile.objects.filter(is_blocked=True)
            if not blocked_profiles.exists():
                self.stdout.write(self.style.SUCCESS('No blocked users found'))
                return
            
            self.stdout.write(self.style.WARNING(f'Found {blocked_profiles.count()} blocked users:'))
            for profile in blocked_profiles:
                self.stdout.write(
                    f'  - {profile.user.username} (ID: {profile.user.id}, Role: {profile.role})'
                )
            return

        username = options['username']
        
        try:
            # Try to find user by username or phone
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" not found')
            )
            return
        
        try:
            profile = user.profile
            if not profile.is_blocked:
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" is not blocked')
                )
                return
            
            profile.is_blocked = False
            profile.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'User "{username}" has been unblocked successfully!')
            )
        except UserProfile.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User profile for "{username}" not found')
            )



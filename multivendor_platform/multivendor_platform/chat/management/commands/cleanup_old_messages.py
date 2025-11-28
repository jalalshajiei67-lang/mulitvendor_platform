from django.core.management.base import BaseCommand
from chat.models import ChatMessage, TypingStatus


class Command(BaseCommand):
    help = 'Delete chat messages older than 90 days (3 months) and clean up stale typing statuses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Number of days to keep messages (default: 90)'
        )

    def handle(self, *args, **options):
        days = options['days']
        
        # Delete old messages
        self.stdout.write('Deleting messages older than {} days...'.format(days))
        deleted_count = ChatMessage.delete_old_messages(days=days)
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully deleted {} old messages'.format(deleted_count)
            )
        )
        
        # Clean up stale typing statuses (older than 5 minutes)
        self.stdout.write('Cleaning up stale typing statuses...')
        TypingStatus.cleanup_stale_statuses(minutes=5)
        self.stdout.write(
            self.style.SUCCESS('Successfully cleaned up stale typing statuses')
        )






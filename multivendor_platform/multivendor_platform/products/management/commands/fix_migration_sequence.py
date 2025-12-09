# products/management/commands/fix_migration_sequence.py
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Fix the django_migrations table sequence when it gets out of sync (PostgreSQL only)'

    def handle(self, *args, **options):
        # Check if we're using PostgreSQL
        db_engine = settings.DATABASES['default']['ENGINE']
        
        if 'postgresql' not in db_engine.lower():
            self.stdout.write(
                self.style.WARNING(
                    'This command is only for PostgreSQL databases. '
                    f'Current database engine: {db_engine}'
                )
            )
            return

        with connection.cursor() as cursor:
            # Get the current max ID from django_migrations
            cursor.execute("SELECT MAX(id) FROM django_migrations;")
            max_id = cursor.fetchone()[0]
            
            if max_id is None:
                self.stdout.write(
                    self.style.WARNING('No migrations found in django_migrations table')
                )
                return

            # Get the current sequence value
            cursor.execute(
                "SELECT last_value FROM django_migrations_id_seq;"
            )
            current_seq = cursor.fetchone()[0]

            self.stdout.write(
                f'Current max ID in django_migrations: {max_id}'
            )
            self.stdout.write(
                f'Current sequence value: {current_seq}'
            )

            if current_seq <= max_id:
                # Reset the sequence to max_id + 1
                new_seq_value = max_id + 1
                cursor.execute(
                    f"SELECT setval('django_migrations_id_seq', {new_seq_value}, false);"
                )
                
                # Verify the fix
                cursor.execute(
                    "SELECT last_value FROM django_migrations_id_seq;"
                )
                new_seq = cursor.fetchone()[0]
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Sequence reset successfully! New sequence value: {new_seq}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'You can now run migrations again: python manage.py migrate'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Sequence is already correct. No action needed.'
                    )
                )


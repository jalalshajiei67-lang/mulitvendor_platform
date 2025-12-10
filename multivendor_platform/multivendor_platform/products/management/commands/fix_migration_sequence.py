# products/management/commands/fix_migration_sequence.py
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Fix Django system table sequences when they get out of sync (PostgreSQL only)'

    def fix_sequence(self, cursor, table_name, sequence_name):
        """Fix a single sequence for a given table"""
        try:
            # Get the current max ID
            cursor.execute(f"SELECT MAX(id) FROM {table_name};")
            max_id = cursor.fetchone()[0]
            
            if max_id is None:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠️  No records found in {table_name}, skipping...')
                )
                return False

            # Get the current sequence value
            cursor.execute(f"SELECT last_value FROM {sequence_name};")
            current_seq = cursor.fetchone()[0]

            if current_seq <= max_id:
                # Reset the sequence to max_id + 1
                new_seq_value = max_id + 1
                cursor.execute(
                    f"SELECT setval('{sequence_name}', {new_seq_value}, false);"
                )
                
                # Verify the fix
                cursor.execute(f"SELECT last_value FROM {sequence_name};")
                new_seq = cursor.fetchone()[0]
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ {table_name}: reset from {current_seq} to {new_seq}'
                    )
                )
                return True
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ {table_name}: sequence is correct (current: {current_seq}, max_id: {max_id})'
                    )
                )
                return False
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'  ✗ {table_name}: Error - {e}')
            )
            return False

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

        self.stdout.write(self.style.SUCCESS('Checking and fixing Django system table sequences...'))
        self.stdout.write('')

        with connection.cursor() as cursor:
            fixed_any = False
            
            # Fix django_migrations sequence
            self.stdout.write('1. Checking django_migrations...')
            if self.fix_sequence(cursor, 'django_migrations', 'django_migrations_id_seq'):
                fixed_any = True
            
            # Fix django_content_type sequence
            self.stdout.write('2. Checking django_content_type...')
            if self.fix_sequence(cursor, 'django_content_type', 'django_content_type_id_seq'):
                fixed_any = True
            
            self.stdout.write('')
            
            if fixed_any:
                self.stdout.write(
                    self.style.SUCCESS(
                        '✓ Sequences fixed! You can now run migrations again: python manage.py migrate'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        '✓ All sequences are correct. No action needed.'
                    )
                )


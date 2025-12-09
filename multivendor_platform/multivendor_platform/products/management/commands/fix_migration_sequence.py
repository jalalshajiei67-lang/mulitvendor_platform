# products/management/commands/fix_migration_sequence.py
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Fix all database sequences when they get out of sync (PostgreSQL only)'

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

        self.stdout.write('Checking all database sequences...')
        
        with connection.cursor() as cursor:
            # Get all sequences and their associated tables
            # This query works with PostgreSQL 9.1+ (more compatible than pg_sequences)
            cursor.execute("""
                SELECT 
                    t.oid::regclass::text as table_name,
                    a.attname as column_name,
                    pg_get_serial_sequence(t.oid::regclass::text, a.attname) as sequence_name
                FROM pg_class t
                JOIN pg_attribute a ON a.attrelid = t.oid
                JOIN pg_namespace n ON n.oid = t.relnamespace
                WHERE n.nspname = 'public'
                AND a.attnum > 0
                AND NOT a.attisdropped
                AND a.attname = 'id'
                AND pg_get_serial_sequence(t.oid::regclass::text, a.attname) IS NOT NULL
                ORDER BY t.relname;
            """)
            
            sequences = cursor.fetchall()
            fixed_count = 0
            
            for table_name, column_name, sequence_name in sequences:
                try:
                    # Get max ID from the table
                    cursor.execute(f'SELECT MAX("{column_name}") FROM {table_name};')
                    max_id_result = cursor.fetchone()
                    max_id = max_id_result[0] if max_id_result else None
                    
                    if max_id is None:
                        # Table is empty, set sequence to 1
                        cursor.execute(f"SELECT setval('{sequence_name}', 1, false);")
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Reset {sequence_name} to 1 (empty table)')
                        )
                        fixed_count += 1
                        continue
                    
                    # Get current sequence value
                    cursor.execute(f"SELECT last_value, is_called FROM {sequence_name};")
                    seq_result = cursor.fetchone()
                    current_seq = seq_result[0] if seq_result else 0
                    is_called = seq_result[1] if seq_result else False
                    
                    # Calculate what the next value would be
                    if is_called:
                        next_seq = current_seq + 1
                    else:
                        next_seq = current_seq
                    
                    if next_seq <= max_id:
                        new_seq_value = max_id + 1
                        cursor.execute(f"SELECT setval('{sequence_name}', {new_seq_value}, false);")
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✓ Fixed {sequence_name}: {next_seq} → {new_seq_value} '
                                f'(max_id: {max_id})'
                            )
                        )
                        fixed_count += 1
                except Exception as e:
                    # Some tables might have issues, skip silently
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️  Skipped {sequence_name}: {e}')
                    )
            
            if fixed_count == 0:
                self.stdout.write(
                    self.style.SUCCESS('✓ All sequences are correct. No action needed.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Fixed {fixed_count} sequence(s)')
                )
                self.stdout.write(
                    self.style.SUCCESS('You can now run migrations again: python manage.py migrate')
                )


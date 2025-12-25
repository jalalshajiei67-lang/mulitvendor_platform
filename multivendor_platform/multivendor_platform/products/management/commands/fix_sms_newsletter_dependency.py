# products/management/commands/fix_sms_newsletter_dependency.py
"""
Fix migration dependency issue where sms_newsletter.0001_initial 
depends on products.0038 but 0038 may not be marked as applied.

Usage:
    python manage.py fix_sms_newsletter_dependency
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    help = 'Fix migration dependency issue for sms_newsletter.0001_initial'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fake',
            action='store_true',
            help='Fake-apply migration 0038 without running it',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking migration state...")
        
        recorder = MigrationRecorder(connection)
        
        # Check if products.0038 is applied
        m38_applied = recorder.migration_qs.filter(
            app='products',
            name='0038_delete_subcategoryfeaturetemplate'
        ).exists()
        
        self.stdout.write(
            f"   products.0038_delete_subcategoryfeaturetemplate: "
            f"{'✓ Applied' if m38_applied else '✗ Not Applied'}"
        )
        
        if m38_applied:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✅ Migration 0038 is already applied. No action needed."
                )
            )
            return
        
        # Check if the table exists
        table_exists = self._check_table_exists('products_subcategoryfeaturetemplate')
        self.stdout.write(
            f"   products_subcategoryfeaturetemplate table: "
            f"{'✓ Exists' if table_exists else '✗ Does not exist'}"
        )
        
        if not table_exists or options['fake']:
            self.stdout.write(
                "\n📝 Fake-applying migration 0038..."
            )
            from django.core.management import call_command
            call_command('migrate', 'products', '0038', '--fake', verbosity=1)
            self.stdout.write(
                self.style.SUCCESS("✅ Migration 0038 fake-applied successfully!")
            )
        else:
            self.stdout.write(
                "\n📝 Table exists - applying migration 0038 normally..."
            )
            from django.core.management import call_command
            call_command('migrate', 'products', '0038', verbosity=1)
            self.stdout.write(
                self.style.SUCCESS("✅ Migration 0038 applied successfully!")
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                "\n✅ Migration dependency issue fixed!"
            )
        )
        self.stdout.write("   You can now run: python manage.py migrate")

    def _check_table_exists(self, table_name):
        """Check if a table exists in the database"""
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = %s
                    );
                """, [table_name])
                return cursor.fetchone()[0]
            else:  # SQLite
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name = ?;
                """, [table_name])
                return cursor.fetchone() is not None


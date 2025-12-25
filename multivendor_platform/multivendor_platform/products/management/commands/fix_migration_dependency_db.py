# products/management/commands/fix_migration_dependency_db.py
"""
Directly fix migration dependency in database by inserting the migration record.

This bypasses Django's consistency check since we're fixing an inconsistency.
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fix migration dependency by directly inserting migration record into database'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing migration dependency in database...")
        
        recorder = MigrationRecorder(connection)
        
        # Check if migration 0038 is already recorded
        exists = recorder.migration_qs.filter(
            app='products',
            name='0038_delete_subcategoryfeaturetemplate'
        ).exists()
        
        if exists:
            self.stdout.write(
                self.style.SUCCESS(
                    "✅ Migration 0038 is already recorded in database."
                )
            )
            return
        
        # Insert the migration record using Django's recorder
        self.stdout.write("   Inserting migration record for products.0038...")
        
        recorder.record_applied('products', '0038_delete_subcategoryfeaturetemplate')
        
        # Verify
        verified = recorder.migration_qs.filter(
            app='products',
            name='0038_delete_subcategoryfeaturetemplate'
        ).exists()
        
        if verified:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✅ Migration dependency fixed!"
                )
            )
            self.stdout.write(
                "   Migration products.0038_delete_subcategoryfeaturetemplate "
                "is now recorded as applied."
            )
            self.stdout.write(
                "\n   You can now run: python manage.py migrate"
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    "\n❌ Failed to insert migration record."
                )
            )


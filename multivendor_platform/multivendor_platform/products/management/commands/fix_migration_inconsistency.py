# products/management/commands/fix_migration_inconsistency.py
import json
import os
import time
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

# #region agent log
LOG_PATH = "/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log"
# #endregion

def log_debug(session_id, run_id, hypothesis_id, location, message, data=None):
    """Log debug information to file"""
    try:
        log_entry = {
            "sessionId": session_id,
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000)
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass  # Silently fail if logging doesn't work


class Command(BaseCommand):
    help = 'Fix inconsistent migration history where 0037 is applied but 0036 is not'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        # #region agent log
        log_debug(
            "debug-session",
            "run1",
            "A",
            "fix_migration_inconsistency.py:handle",
            "Command started",
            {"dry_run": options.get("dry_run", False)}
        )
        # #endregion

        dry_run = options['dry_run']
        
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

        self.stdout.write(self.style.SUCCESS('Checking migration history consistency...'))
        self.stdout.write('')

        with connection.cursor() as cursor:
            # #region agent log
            log_debug(
                "debug-session",
                "run1",
                "B",
                "fix_migration_inconsistency.py:handle",
                "Checking migration state in database",
                {}
            )
            # #endregion

            # Check current migration state
            cursor.execute("""
                SELECT app, name, applied 
                FROM django_migrations 
                WHERE app = 'products' 
                AND name IN ('0036_subcategory_feature_template', '0038_delete_subcategoryfeaturetemplate')
                ORDER BY name;
            """)
            
            migrations = cursor.fetchall()
            
            # #region agent log
            log_debug(
                "debug-session",
                "run1",
                "C",
                "fix_migration_inconsistency.py:handle",
                "Migration state retrieved",
                {"migrations": [{"app": m[0], "name": m[1], "applied": str(m[2])} for m in migrations]}
            )
            # #endregion

            migration_dict = {name: applied for app, name, applied in migrations}
            
            m36_applied = migration_dict.get('0036_subcategory_feature_template', False)
            m38_applied = migration_dict.get('0038_delete_subcategoryfeaturetemplate', False)

            self.stdout.write(f'Migration 0036 (subcategory_feature_template): {"✓ Applied" if m36_applied else "✗ Not Applied"}')
            self.stdout.write(f'Migration 0038 (delete_subcategoryfeaturetemplate): {"✓ Applied" if m38_applied else "✗ Not Applied"}')
            self.stdout.write('')

            # #region agent log
            log_debug(
                "debug-session",
                "run1",
                "D",
                "fix_migration_inconsistency.py:handle",
                "Migration state analyzed",
                {
                    "m36_applied": m36_applied,
                    "m38_applied": m38_applied,
                    "inconsistent": m38_applied and not m36_applied
                }
            )
            # #endregion

            # Check for inconsistency
            if m38_applied and not m36_applied:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ INCONSISTENCY DETECTED: '
                        'Migration 0038 is applied but its dependency 0036 is not!'
                    )
                )
                self.stdout.write('')

                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(
                            'DRY RUN: Would mark migration 0036 as applied (fake)'
                        )
                    )
                    # #region agent log
                    log_debug(
                        "debug-session",
                        "run1",
                        "E",
                        "fix_migration_inconsistency.py:handle",
                        "Dry run - would fix inconsistency",
                        {}
                    )
                    # #endregion
                else:
                    # Fix: Mark 0036 as applied (fake it)
                    # Since 0038 depends on 0036 and 0038 is already applied,
                    # it means 0036's changes must have been applied somehow
                    # We'll fake 0036 to make the history consistent
                    
                    # #region agent log
                    log_debug(
                        "debug-session",
                        "run1",
                        "F",
                        "fix_migration_inconsistency.py:handle",
                        "Fixing inconsistency - marking 0036 as applied",
                        {}
                    )
                    # #endregion

                    # Check if migration record already exists (shouldn't, but be safe)
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM django_migrations 
                        WHERE app = 'products' 
                        AND name = '0036_subcategory_feature_template';
                    """)
                    exists = cursor.fetchone()[0] > 0
                    
                    # #region agent log
                    log_debug(
                        "debug-session",
                        "run1",
                        "F1",
                        "fix_migration_inconsistency.py:handle",
                        "Checked if 0036 migration record exists",
                        {"exists": exists}
                    )
                    # #endregion

                    if not exists:
                        cursor.execute("""
                            INSERT INTO django_migrations (app, name, applied)
                            VALUES ('products', '0036_subcategory_feature_template', NOW());
                        """)
                    else:
                        # Update the existing record to mark it as applied
                        cursor.execute("""
                            UPDATE django_migrations 
                            SET applied = NOW()
                            WHERE app = 'products' 
                            AND name = '0036_subcategory_feature_template';
                        """)
                    
                    # Verify the fix
                    cursor.execute("""
                        SELECT applied 
                        FROM django_migrations 
                        WHERE app = 'products' 
                        AND name = '0036_subcategory_feature_template';
                    """)
                    
                    result = cursor.fetchone()
                    
                    # #region agent log
                    log_debug(
                        "debug-session",
                        "run1",
                        "G",
                        "fix_migration_inconsistency.py:handle",
                        "Fix applied - verifying",
                        {"migration_0036_exists": result is not None}
                    )
                    # #endregion

                    if result:
                        self.stdout.write(
                            self.style.SUCCESS(
                                '✅ Fixed! Migration 0036 is now marked as applied.'
                            )
                        )
                        self.stdout.write(
                            '   You can now run migrations: python manage.py migrate'
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                '❌ Failed to mark migration 0036 as applied.'
                            )
                        )
            elif not m36_applied and not m37_applied:
                self.stdout.write(
                    self.style.SUCCESS(
                        '✓ Both migrations are not applied. This is normal - they will be applied in order.'
                    )
                )
                # #region agent log
                log_debug(
                    "debug-session",
                    "run1",
                    "H",
                    "fix_migration_inconsistency.py:handle",
                    "Both migrations not applied - normal state",
                    {}
                )
                # #endregion
            elif m36_applied and m37_applied:
                self.stdout.write(
                    self.style.SUCCESS(
                        '✓ Both migrations are applied. Migration history is consistent.'
                    )
                )
                # #region agent log
                log_debug(
                    "debug-session",
                    "run1",
                    "I",
                    "fix_migration_inconsistency.py:handle",
                    "Both migrations applied - consistent state",
                    {}
                )
                # #endregion
            elif m36_applied and not m38_applied:
                self.stdout.write(
                    self.style.SUCCESS(
                        '✓ Migration 0036 is applied. Migration 0038 will be applied when you run migrations.'
                    )
                )
                # #region agent log
                log_debug(
                    "debug-session",
                    "run1",
                    "J",
                    "fix_migration_inconsistency.py:handle",
                    "0036 applied, 0037 pending - normal state",
                    {}
                )
                # #endregion

            self.stdout.write('')


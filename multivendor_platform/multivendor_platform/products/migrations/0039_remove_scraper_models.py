# Generated manually to delete scraper models
# This migration removes ProductScrapeJob and ScrapeJobBatch models
# These models were removed from models.py and all related code has been deleted

from django.db import migrations, connection


def drop_tables_if_exist(apps, schema_editor):
    """
    Conditionally drop the scraper tables if they exist.
    This handles both fresh databases and databases that already have the tables.
    """
    if connection.vendor == 'postgresql':
        # PostgreSQL: Drop tables if they exist (CASCADE to handle foreign keys)
        schema_editor.execute("""
            DROP TABLE IF EXISTS products_productscrapejob CASCADE;
        """)
        schema_editor.execute("""
            DROP TABLE IF EXISTS products_scrapejobbatch CASCADE;
        """)
    else:
        # SQLite: Check if tables exist before dropping
        cursor = connection.cursor()
        
        # Drop ProductScrapeJob table
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='products_productscrapejob';
        """)
        if cursor.fetchone():
            schema_editor.execute("DROP TABLE products_productscrapejob;")
        
        # Drop ScrapeJobBatch table
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='products_scrapejobbatch';
        """)
        if cursor.fetchone():
            schema_editor.execute("DROP TABLE products_scrapejobbatch;")


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_delete_subcategoryfeaturetemplate'),
    ]

    operations = [
        # Separate database operations from state changes
        # This allows us to conditionally drop the tables while always updating Django's state
        migrations.SeparateDatabaseAndState(
            database_operations=[
                # Drop tables only if they exist (idempotent)
                migrations.RunPython(drop_tables_if_exist, migrations.RunPython.noop),
            ],
            state_operations=[
                # Always update Django's migration state to remove the models
                migrations.DeleteModel(
                    name='ProductScrapeJob',
                ),
                migrations.DeleteModel(
                    name='ScrapeJobBatch',
                ),
            ],
        ),
    ]


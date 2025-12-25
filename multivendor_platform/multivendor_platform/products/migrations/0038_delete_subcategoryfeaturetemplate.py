# Generated manually to delete SubcategoryFeatureTemplate model
# This model was removed from models.py but migrations 0036 and 0037 created/modified it
# Migration 0038 properly removes it to sync Django state with models.py
# This migration is idempotent - safe to run even if table doesn't exist

from django.db import migrations, connection


def drop_table_if_exists(apps, schema_editor):
    """
    Conditionally drop the table if it exists.
    This handles both fresh databases and databases that already have the table.
    """
    if connection.vendor == 'postgresql':
        # PostgreSQL: Drop table if it exists
        schema_editor.execute("""
            DROP TABLE IF EXISTS products_subcategoryfeaturetemplate CASCADE;
        """)
    else:
        # SQLite: Check if table exists before dropping
        cursor = connection.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='products_subcategoryfeaturetemplate';
        """)
        if cursor.fetchone():
            schema_editor.execute("DROP TABLE products_subcategoryfeaturetemplate;")


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_remove_subcategoryfeaturetemplate_unique_subcategory_feature_name_and_more'),
    ]

    operations = [
        # Separate database operations from state changes
        # This allows us to conditionally drop the table while always updating Django's state
        migrations.SeparateDatabaseAndState(
            database_operations=[
                # Drop table only if it exists (idempotent)
                migrations.RunPython(drop_table_if_exists, migrations.RunPython.noop),
            ],
            state_operations=[
                # Always update Django's migration state to remove the model
                migrations.DeleteModel(
                    name='SubcategoryFeatureTemplate',
                ),
            ],
        ),
    ]


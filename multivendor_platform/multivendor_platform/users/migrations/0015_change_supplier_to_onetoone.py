# Generated migration to enforce one supplier per user
# This migration changes Supplier.vendor from ForeignKey to OneToOneField

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def remove_duplicate_suppliers(apps, schema_editor):
    """
    Data migration: Remove duplicate suppliers, keeping only the first one per user.
    This ensures each user has at most one supplier before we change to OneToOneField.
    """
    Supplier = apps.get_model('users', 'Supplier')
    
    # Group suppliers by vendor
    from django.db.models import Min
    from collections import defaultdict
    
    # Find duplicate suppliers per vendor
    vendor_suppliers = defaultdict(list)
    for supplier in Supplier.objects.all().order_by('id'):
        vendor_suppliers[supplier.vendor_id].append(supplier.id)
    
    # Keep the first supplier for each vendor, delete the rest
    deleted_count = 0
    for vendor_id, supplier_ids in vendor_suppliers.items():
        if len(supplier_ids) > 1:
            # Keep the first (lowest ID), delete the rest
            keep_id = min(supplier_ids)
            to_delete = [sid for sid in supplier_ids if sid != keep_id]
            Supplier.objects.filter(id__in=to_delete).delete()
            deleted_count += len(to_delete)
    
    if deleted_count > 0:
        print(f"Removed {deleted_count} duplicate supplier(s) to enforce one-per-user rule")


def reverse_remove_duplicates(apps, schema_editor):
    """
    Reverse migration: Cannot recreate deleted suppliers, so this is a no-op.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0014_rename_users_conta_note_contact_idx_users_conta_contact_cc7c9b_idx_and_more'),
    ]

    operations = [
        # Step 1: Remove duplicate suppliers (data migration) - MUST happen first
        migrations.RunPython(remove_duplicate_suppliers, reverse_remove_duplicates),
        
        # Step 2: Remove unique_together constraint before changing field type
        migrations.AlterUniqueTogether(
            name='supplier',
            unique_together=set(),  # Remove unique_together constraint
        ),
        
        # Step 3: Change ForeignKey to OneToOneField
        # This will automatically add a unique constraint on vendor
        migrations.AlterField(
            model_name='supplier',
            name='vendor',
            field=models.OneToOneField(
                help_text='The user/vendor who manages this supplier. Each user can only have one supplier profile.',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='supplier',  # Changed from 'suppliers' to 'supplier'
                to=settings.AUTH_USER_MODEL
            ),
        ),
    ]


# Generated manually for Phase 5: Invitation System
# This migration updates the Invitation model from 0003 to match Phase 5 specification

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0003_supplierengagement_endorsements_received_and_more'),
        ('users', '0007_otp'),
    ]

    operations = [
        # Remove old Invitation model if it exists (from 0003)
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS gamification_invitation;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Create new Invitation model with Phase 5 structure
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_code', models.CharField(db_index=True, max_length=50, unique=True)),
                ('invitee_email', models.EmailField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('expired', 'Expired')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_invitations', to='users.vendorprofile')),
                ('invitee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_invitation', to='users.vendorprofile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='invitation',
            index=models.Index(fields=['invite_code'], name='gamificatio_invite_code_idx'),
        ),
        migrations.AddIndex(
            model_name='invitation',
            index=models.Index(fields=['status', 'created_at'], name='gamificatio_status_created_idx'),
        ),
    ]


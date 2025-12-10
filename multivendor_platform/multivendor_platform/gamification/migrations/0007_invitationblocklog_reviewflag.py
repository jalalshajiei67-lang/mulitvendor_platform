from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('gamification', '0006_rename_gamificatio_invite_code_idx_gamificatio_invite__517957_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='invitee_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='ReviewFlagLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('reason', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cleared', models.BooleanField(default=False)),
                ('cleared_at', models.DateTimeField(blank=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('cleared_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cleared_review_flag_logs', to=settings.AUTH_USER_MODEL)),
                ('vendor_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_flag_logs', to='users.vendorprofile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='InvitationBlockLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitee_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('invitee_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('reason', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved', models.BooleanField(default=False)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_block_logs', to='users.vendorprofile')),
                ('resolved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_invitation_block_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='invitationblocklog',
            index=models.Index(fields=['reason', 'created_at'], name='gamificatio_reason_57b697_idx'),
        ),
        migrations.AddIndex(
            model_name='reviewflaglog',
            index=models.Index(fields=['reason', 'created_at'], name='gamificatio_reason_35c6f5_idx'),
        ),
    ]


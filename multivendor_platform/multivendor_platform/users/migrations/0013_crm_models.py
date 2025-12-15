# Generated manually for CRM models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0011_add_contact_phone_landline'),
        ('orders', '0001_initial'),
    ]

    operations = [
        # Drop old duplicate index if it exists from a previous partial migration
        migrations.RunSQL(
            "DROP INDEX IF EXISTS users_conta_seller_i_idx;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.CreateModel(
            name='SellerContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, help_text='General notes about the contact', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_contacts', to=settings.AUTH_USER_MODEL)),
                ('source_order', models.ForeignKey(blank=True, help_text='Order/RFQ that created this contact', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_contacts', to='orders.order')),
            ],
            options={
                'verbose_name': 'Seller Contact',
                'verbose_name_plural': 'Seller Contacts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ContactNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_notes', to='users.sellercontact')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_notes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact Note',
                'verbose_name_plural': 'Contact Notes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ContactTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('due_date', models.DateTimeField()),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(blank=True, help_text='Optional: link task to a contact', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='users.sellercontact')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crm_tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact Task',
                'verbose_name_plural': 'Contact Tasks',
                'ordering': ['due_date', '-priority'],
            },
        ),
        migrations.AddIndex(
            model_name='sellercontact',
            index=models.Index(fields=['seller', '-created_at'], name='users_selle_seller_i_idx'),
        ),
        migrations.AddIndex(
            model_name='sellercontact',
            index=models.Index(fields=['phone'], name='users_selle_phone_idx'),
        ),
        migrations.AddIndex(
            model_name='sellercontact',
            index=models.Index(fields=['email'], name='users_selle_email_idx'),
        ),
        migrations.AddIndex(
            model_name='contactnote',
            index=models.Index(fields=['contact', '-created_at'], name='users_conta_note_contact_idx'),
        ),
        migrations.AddIndex(
            model_name='contactnote',
            index=models.Index(fields=['seller', '-created_at'], name='users_conta_note_seller_idx'),
        ),
        migrations.AddIndex(
            model_name='contacttask',
            index=models.Index(fields=['seller', 'status', 'due_date'], name='users_conta_task_seller_idx'),
        ),
        migrations.AddIndex(
            model_name='contacttask',
            index=models.Index(fields=['contact', 'status'], name='users_conta_task_contact_idx'),
        ),
        migrations.AddIndex(
            model_name='contacttask',
            index=models.Index(fields=['due_date'], name='users_conta_due_dat_idx'),
        ),
    ]


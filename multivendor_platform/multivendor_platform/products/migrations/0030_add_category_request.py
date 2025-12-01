# Generated manually for CategoryRequest model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0029_label_categories_label_departments'),
        ('users', '0007_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_name', models.CharField(help_text='Name of the subcategory requested by supplier', max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('admin_notes', models.TextField(blank=True, help_text='Admin notes or rejection reason', null=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(blank=True, help_text='Product that triggered this request', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_request', to='products.product')),
                ('reviewed_by', models.ForeignKey(blank=True, help_text='Admin who reviewed this request', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_category_requests', to=settings.AUTH_USER_MODEL)),
                ('supplier', models.ForeignKey(help_text='Supplier who requested the category', on_delete=django.db.models.deletion.CASCADE, related_name='category_requests', to='users.supplier')),
            ],
            options={
                'verbose_name': 'Category Request',
                'verbose_name_plural': 'Category Requests',
                'ordering': ['-created_at'],
            },
        ),
    ]




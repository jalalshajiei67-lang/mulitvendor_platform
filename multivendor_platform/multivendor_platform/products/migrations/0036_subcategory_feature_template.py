# Generated manually for SubcategoryFeatureTemplate

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_product_marketplace_hide'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubcategoryFeatureTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(help_text='نام ویژگی', max_length=200)),
                ('is_required', models.BooleanField(default=False, help_text='آیا این ویژگی الزامی است؟')),
                ('sort_order', models.PositiveIntegerField(default=0, help_text='ترتیب نمایش')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_templates', to='products.subcategory')),
            ],
            options={
                'verbose_name': 'Subcategory Feature Template',
                'verbose_name_plural': 'Subcategory Feature Templates',
                'ordering': ['sort_order', 'created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='subcategoryfeaturetemplate',
            constraint=models.UniqueConstraint(fields=('subcategory', 'feature_name'), name='unique_subcategory_feature_name'),
        ),
    ]


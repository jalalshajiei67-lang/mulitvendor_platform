from django.db import migrations, models


def approve_existing_products(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Product.objects.all().update(approval_status='approved')


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_labelmanagementproxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='approval_status',
            field=models.CharField(
                choices=[
                    ('pending', 'در انتظار تایید'),
                    ('approved', 'تایید شده'),
                    ('rejected', 'رد شده'),
                ],
                default='pending',
                help_text='وضعیت تایید ادمین برای انتشار محصول',
                max_length=20,
            ),
        ),
        migrations.RunPython(approve_existing_products, migrations.RunPython.noop),
    ]


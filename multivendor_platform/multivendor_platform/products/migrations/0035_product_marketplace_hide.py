from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0034_product_approval_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_marketplace_hidden',
            field=models.BooleanField(
                default=False,
                help_text="اگر فعال باشد، محصول از مارکت‌پلیس اصلی مخفی می‌شود و فقط در مینی‌وبسایت و داشبورد فروشنده دیده می‌شود.",
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='marketplace_hide_reason',
            field=models.TextField(
                blank=True,
                null=True,
                help_text="یادداشت دوستانه ادمین برای توضیح دلیل عدم نمایش (مثلا وجود واترمارک یا اطلاعات فروشنده).",
            ),
        ),
    ]


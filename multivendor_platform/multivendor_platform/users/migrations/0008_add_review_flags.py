from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='flag_reason',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='productreview',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliercomment',
            name='flag_reason',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='suppliercomment',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
    ]


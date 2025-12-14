from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_add_commission_based_pricing'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorprofile',
            name='contact_phone_landline',
            field=models.CharField(
                blank=True,
                help_text='Landline/office phone number',
                max_length=20,
                null=True
            ),
        ),
    ]


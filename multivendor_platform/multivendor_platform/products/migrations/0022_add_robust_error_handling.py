# Generated manually for robust error handling

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_productscrapejob'),
    ]

    operations = [
        migrations.AddField(
            model_name='productscrapejob',
            name='error_details',
            field=models.JSONField(blank=True, help_text='Detailed error information from error handler', null=True),
        ),
        migrations.AddField(
            model_name='productscrapejob',
            name='retry_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of times this job has been retried'),
        ),
        migrations.AddField(
            model_name='productscrapejob',
            name='last_retry_at',
            field=models.DateTimeField(blank=True, help_text='When the last retry occurred', null=True),
        ),
        migrations.AlterField(
            model_name='productscrapejob',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('processing', 'Processing'),
                    ('completed', 'Completed'),
                    ('completed_with_warnings', 'Completed with Warnings'),
                    ('failed', 'Failed')
                ],
                default='pending',
                max_length=30
            ),
        ),
    ]

# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blogpost_linked_subcategories'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='display_locations',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Select where this post should be displayed. Can select multiple locations.'
            ),
        ),
        migrations.RunPython(
            code=lambda apps, schema_editor: apps.get_model('blog', 'BlogPost').objects.update(display_locations=['main_blog']),
            reverse_code=migrations.RunPython.noop,
        ),
    ]


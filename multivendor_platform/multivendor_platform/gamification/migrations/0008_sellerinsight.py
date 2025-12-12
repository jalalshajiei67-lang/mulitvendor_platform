from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_pricingtier_vendorsubscription'),
        ('gamification', '0007_invitationblocklog_reviewflag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointshistory',
            name='reason',
            field=models.CharField(choices=[('login', 'Login'), ('product_save', 'Product Save'), ('profile_update', 'Profile Update'), ('mini_site', 'Mini Website Update'), ('fast_response', 'Fast Order Response'), ('tutorial', 'Watched Tutorial'), ('insight_share', 'Insight Share'), ('insight_comment', 'Insight Comment'), ('insight_like', 'Insight Liked'), ('badge', 'Badge Earned'), ('section_completion', 'Section Completion'), ('peer_invitation', 'Peer Invitation'), ('endorsement_received', 'Endorsement Received'), ('custom', 'Custom Action')], default='custom', max_length=30),
        ),
        migrations.CreateModel(
            name='SellerInsight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_insights', to=settings.AUTH_USER_MODEL)),
                ('vendor_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insights', to='users.vendorprofile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SellerInsightComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('insight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='gamification.sellerinsight')),
                ('vendor_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insight_comments', to='users.vendorprofile')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='sellerinsight',
            index=models.Index(fields=['created_at'], name='gamificati_created_0adf81_idx'),
        ),
        migrations.AddIndex(
            model_name='sellerinsightcomment',
            index=models.Index(fields=['insight', 'created_at'], name='gamificati_insight__55a5a4_idx'),
        ),
    ]

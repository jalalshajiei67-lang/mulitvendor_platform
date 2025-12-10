from django.db import migrations


def create_initial_badges(apps, schema_editor):
    Badge = apps.get_model('gamification', 'Badge')

    badges = [
        {
            'slug': 'recruiter',
            'title': 'جذب همکار',
            'tier': 'gold',
            'icon': 'mdi-account-plus',
            'description': 'دعوت 5 یا بیشتر همکار موفق',
            'criteria': {'invitations_accepted': {'min': 5}},
            'category': 'social',
        },
        {
            'slug': 'customer_favorite',
            'title': 'محبوب مشتریان',
            'tier': 'gold',
            'icon': 'mdi-star',
            'description': '20 یا بیشتر نظر مثبت از مشتریان',
            'criteria': {'positive_reviews': {'min': 20}},
            'category': 'reputation',
        },
        {
            'slug': 'fast_responder',
            'title': 'پاسخ‌گوی سریع',
            'tier': 'silver',
            'icon': 'mdi-lightning-bolt',
            'description': 'میانگین زمان پاسخ کمتر از 60 دقیقه',
            'criteria': {'avg_response_minutes': {'max': 60}},
            'category': 'responsiveness',
        },
    ]

    for badge in badges:
        Badge.objects.update_or_create(
            slug=badge['slug'],
            defaults=badge,
        )


def remove_initial_badges(apps, schema_editor):
    Badge = apps.get_model('gamification', 'Badge')
    Badge.objects.filter(slug__in=['recruiter', 'customer_favorite', 'fast_responder']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0004_invitation_model_update'),
    ]

    operations = [
        migrations.RunPython(create_initial_badges, reverse_code=remove_initial_badges),
    ]


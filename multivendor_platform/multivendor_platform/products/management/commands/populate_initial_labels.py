from django.core.management.base import BaseCommand

from ...models import Label, LabelGroup


class Command(BaseCommand):
    help = 'Seed initial label groups and labels for the SEO-driven catalog filters.'

    LABEL_GROUPS = [
        {
            'name': 'صنایع',
            'slug': 'industry',
            'description': 'صنایع و کاربردهایی که ماشین‌آلات شما در آن‌ها استفاده می‌شوند.',
            'display_order': 10,
            'is_active': True
        },
        {
            'name': 'اندازه',
            'slug': 'size',
            'description': 'اندازه یا ظرفیت ماشین‌آلات.',
            'display_order': 20,
            'is_active': True
        },
        {
            'name': 'وضعیت',
            'slug': 'status',
            'description': 'وضعیت‌های تبلیغاتی مانند جدید یا پرفروش.',
            'display_order': 30,
            'is_active': True
        }
    ]

    LABELS = [
        {
            'name': 'ماشین‌آلات مواد غذایی',
            'slug': 'food-processing-machinery',
            'group_slug': 'industry',
            'description': 'ماشین‌آلات مخصوص خطوط تولید مواد غذایی.',
            'color': '#69F0AE',
            'is_filterable': True,
            'is_seo_page': True,
            'seo_title': 'ماشین‌آلات مواد غذایی | ایندکسو',
            'seo_description': 'ماشین‌آلات مواد غذایی صنعتی با پشتیبانی از فروشندگان متعدد.',
            'seo_h1': 'ماشین‌آلات مواد غذایی',
            'display_order': 10
        },
        {
            'name': 'ماشین‌آلات بسته‌بندی',
            'slug': 'packaging-machinery',
            'group_slug': 'industry',
            'description': 'راهکارهای بسته‌بندی برای انواع محصولات.',
            'color': '#FFB300',
            'is_filterable': True,
            'is_seo_page': True,
            'seo_title': 'ماشین‌آلات بسته‌بندی صنعتی',
            'seo_description': 'ماشین‌آلات بسته‌بندی سریع و دقیق با پشتیبانی چنددسته‌ای.',
            'seo_h1': 'ماشین‌آلات بسته‌بندی',
            'display_order': 20
        },
        {
            'name': 'ماشین‌آلات کوچک',
            'slug': 'small-machinery',
            'group_slug': 'size',
            'description': 'ماشین‌آلات جمع‌وجور و فضای محدود.',
            'color': '#26C6DA',
            'is_filterable': True,
            'is_seo_page': False,
            'display_order': 10
        },
        {
            'name': 'ماشین‌آلات متوسط',
            'slug': 'medium-machinery',
            'group_slug': 'size',
            'description': 'ماشین‌آلات با ظرفیت متوسط برای خط تولید‌های متوسط.',
            'color': '#42A5F5',
            'is_filterable': True,
            'display_order': 20
        },
        {
            'name': 'ماشین‌آلات بزرگ',
            'slug': 'large-machinery',
            'group_slug': 'size',
            'description': 'ماشین‌آلات با توان و ظرفیت بالا برای کارخانه‌های بزرگ.',
            'color': '#AB47BC',
            'is_filterable': True,
            'display_order': 30
        },
        {
            'name': 'جدید',
            'slug': 'new',
            'group_slug': 'status',
            'description': 'محصولات تازه وارد بازار.',
            'color': '#00C853',
            'is_promotional': True,
            'display_order': 10
        },
        {
            'name': 'پرفروش',
            'slug': 'popular',
            'group_slug': 'status',
            'description': 'محصولاتی که بیشترین تقاضا را دارند.',
            'color': '#FF8F00',
            'is_promotional': True,
            'display_order': 20
        }
    ]

    def handle(self, *args, **options):
        created_groups = 0
        for group_data in self.LABEL_GROUPS:
            group, created = LabelGroup.objects.update_or_create(
                slug=group_data['slug'],
                defaults={
                    'name': group_data['name'],
                    'description': group_data.get('description', ''),
                    'display_order': group_data.get('display_order', 0),
                    'is_active': group_data.get('is_active', True)
                }
            )
            if created:
                created_groups += 1

        created_labels = 0
        for label_data in self.LABELS:
            group = LabelGroup.objects.get(slug=label_data['group_slug'])
            defaults = {
                'name': label_data['name'],
                'description': label_data.get('description', ''),
                'label_group': group,
                'color': label_data.get('color'),
                'is_promotional': label_data.get('is_promotional', False),
                'is_filterable': label_data.get('is_filterable', True),
                'is_seo_page': label_data.get('is_seo_page', False),
                'seo_title': label_data.get('seo_title'),
                'seo_description': label_data.get('seo_description'),
                'seo_h1': label_data.get('seo_h1'),
                'display_order': label_data.get('display_order', 0),
                'is_active': True
            }
            label, created = Label.objects.update_or_create(slug=label_data['slug'], defaults=defaults)
            if created:
                created_labels += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_groups} label groups.'))
        self.stdout.write(self.style.SUCCESS(f'Created {created_labels} labels.'))


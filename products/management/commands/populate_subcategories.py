# products/management/commands/populate_subcategories.py
from django.core.management.base import BaseCommand
from products.models import Category, Subcategory

class Command(BaseCommand):
    help = 'Populate the database with sample subcategories'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample subcategories...')
        
        # Subcategories data
        subcategories_data = [
            # Electronics subcategories
            {
                'name': 'گوشی هوشمند',
                'slug': 'smartphone',
                'description': 'انواع گوشی‌های هوشمند',
                'category_slugs': ['mobile-tablet']
            },
            {
                'name': 'تبلت',
                'slug': 'tablet',
                'description': 'تبلت‌های مختلف',
                'category_slugs': ['mobile-tablet']
            },
            {
                'name': 'لپ‌تاپ',
                'slug': 'laptop',
                'description': 'انواع لپ‌تاپ',
                'category_slugs': ['laptop-computer']
            },
            {
                'name': 'کامپیوتر رومیزی',
                'slug': 'desktop',
                'description': 'کامپیوتر دسکتاپ',
                'category_slugs': ['laptop-computer']
            },
            {
                'name': 'دوربین دیجیتال',
                'slug': 'digital-camera',
                'description': 'دوربین‌های دیجیتال',
                'category_slugs': ['camera']
            },
            # Fashion subcategories
            {
                'name': 'پیراهن مردانه',
                'slug': 'mens-shirt',
                'description': 'پیراهن و تیشرت مردانه',
                'category_slugs': ['mens-clothing']
            },
            {
                'name': 'شلوار مردانه',
                'slug': 'mens-pants',
                'description': 'شلوار مردانه',
                'category_slugs': ['mens-clothing']
            },
            {
                'name': 'مانتو',
                'slug': 'manteau',
                'description': 'مانتو و تونیک',
                'category_slugs': ['womens-clothing']
            },
            {
                'name': 'شلوار زنانه',
                'slug': 'womens-pants',
                'description': 'شلوار زنانه',
                'category_slugs': ['womens-clothing']
            },
            {
                'name': 'کفش اسپرت',
                'slug': 'sneakers',
                'description': 'کفش اسپرت و کتانی',
                'category_slugs': ['shoes']
            },
            {
                'name': 'کفش مجلسی',
                'slug': 'formal-shoes',
                'description': 'کفش مجلسی و رسمی',
                'category_slugs': ['shoes']
            },
            # Home & Kitchen subcategories
            {
                'name': 'ظروف آشپزخانه',
                'slug': 'cookware',
                'description': 'قابلمه، تابه و...',
                'category_slugs': ['kitchen-appliances']
            },
            {
                'name': 'لوازم برقی آشپزخانه',
                'slug': 'kitchen-electronics',
                'description': 'مایکروویو، توستر و...',
                'category_slugs': ['kitchen-appliances']
            },
            {
                'name': 'مبل راحتی',
                'slug': 'sofa',
                'description': 'کاناپه و مبل',
                'category_slugs': ['furniture']
            },
            {
                'name': 'میز و صندلی',
                'slug': 'table-chair',
                'description': 'میز و صندلی ناهارخوری',
                'category_slugs': ['furniture']
            },
            {
                'name': 'تابلو دیواری',
                'slug': 'wall-art',
                'description': 'تابلو و نقاشی',
                'category_slugs': ['decoration']
            },
            # Sports subcategories
            {
                'name': 'دمبل و وزنه',
                'slug': 'weights',
                'description': 'وزنه و دمبل ورزشی',
                'category_slugs': ['sports-equipment']
            },
            {
                'name': 'تردمیل',
                'slug': 'treadmill',
                'description': 'تردمیل خانگی',
                'category_slugs': ['sports-equipment']
            },
            {
                'name': 'لباس ورزشی مردانه',
                'slug': 'mens-sportswear',
                'description': 'ست ورزشی مردانه',
                'category_slugs': ['sports-clothing']
            },
            {
                'name': 'لباس ورزشی زنانه',
                'slug': 'womens-sportswear',
                'description': 'ست ورزشی زنانه',
                'category_slugs': ['sports-clothing']
            },
            # Books & Media subcategories
            {
                'name': 'رمان',
                'slug': 'novel',
                'description': 'کتاب‌های رمان',
                'category_slugs': ['books']
            },
            {
                'name': 'کتاب آموزشی',
                'slug': 'educational-books',
                'description': 'کتاب‌های آموزشی',
                'category_slugs': ['books']
            },
            {
                'name': 'ساز',
                'slug': 'instruments',
                'description': 'آلات موسیقی',
                'category_slugs': ['music']
            },
            # Beauty & Health subcategories
            {
                'name': 'لوازم آرایش',
                'slug': 'makeup',
                'description': 'لوازم آرایش و زیبایی',
                'category_slugs': ['cosmetics']
            },
            {
                'name': 'عطر و ادکلن',
                'slug': 'perfume',
                'description': 'عطر و ادکلن',
                'category_slugs': ['cosmetics']
            },
            {
                'name': 'مراقبت پوست',
                'slug': 'skincare',
                'description': 'محصولات مراقبت پوست',
                'category_slugs': ['hygiene']
            }
        ]
        
        for sub_data in subcategories_data:
            subcategory, created = Subcategory.objects.get_or_create(
                slug=sub_data['slug'],
                defaults={
                    'name': sub_data['name'],
                    'description': sub_data['description'],
                    'is_active': True,
                    'sort_order': 0
                }
            )
            
            # Add categories to subcategory
            for cat_slug in sub_data['category_slugs']:
                try:
                    cat = Category.objects.get(slug=cat_slug)
                    subcategory.categories.add(cat)
                except Category.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  ⚠ دسته‌بندی با slug "{cat_slug}" یافت نشد'))
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ زیردسته ایجاد شد: {subcategory.name}'))
            else:
                self.stdout.write(f'  ○ زیردسته موجود است: {subcategory.name}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ همه زیردسته‌ها با موفقیت ایجاد شدند!'))
        self.stdout.write(f'تعداد زیردسته‌ها: {Subcategory.objects.filter(is_active=True).count()}')


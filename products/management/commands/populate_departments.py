# products/management/commands/populate_departments.py
from django.core.management.base import BaseCommand
from products.models import Department, Category

class Command(BaseCommand):
    help = 'Populate the database with sample departments and categories'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample departments and categories...')
        
        # Create departments
        departments_data = [
            {
                'name': 'الکترونیکی',
                'slug': 'electronics',
                'description': 'تمام محصولات الکترونیکی و دیجیتال',
                'is_active': True,
                'sort_order': 1
            },
            {
                'name': 'مد و پوشاک',
                'slug': 'fashion',
                'description': 'لباس، کفش و اکسسوری',
                'is_active': True,
                'sort_order': 2
            },
            {
                'name': 'خانه و آشپزخانه',
                'slug': 'home-kitchen',
                'description': 'لوازم خانگی و آشپزخانه',
                'is_active': True,
                'sort_order': 3
            },
            {
                'name': 'ورزش و سرگرمی',
                'slug': 'sports',
                'description': 'تجهیزات ورزشی و سرگرمی',
                'is_active': True,
                'sort_order': 4
            },
            {
                'name': 'کتاب و رسانه',
                'slug': 'books-media',
                'description': 'کتاب، موسیقی و رسانه دیجیتال',
                'is_active': True,
                'sort_order': 5
            },
            {
                'name': 'زیبایی و سلامت',
                'slug': 'beauty-health',
                'description': 'محصولات زیبایی و بهداشتی',
                'is_active': True,
                'sort_order': 6
            }
        ]
        
        departments = []
        for dept_data in departments_data:
            department, created = Department.objects.get_or_create(
                slug=dept_data['slug'],
                defaults=dept_data
            )
            departments.append(department)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ بخش ایجاد شد: {department.name}'))
            else:
                self.stdout.write(f'○ بخش موجود است: {department.name}')
        
        # Create categories for each department
        categories_data = [
            # Electronics categories
            {
                'name': 'موبایل و تبلت',
                'slug': 'mobile-tablet',
                'description': 'گوشی هوشمند و تبلت',
                'department_slugs': ['electronics']
            },
            {
                'name': 'لپ‌تاپ و کامپیوتر',
                'slug': 'laptop-computer',
                'description': 'لپ‌تاپ، کامپیوتر و لوازم جانبی',
                'department_slugs': ['electronics']
            },
            {
                'name': 'دوربین',
                'slug': 'camera',
                'description': 'دوربین دیجیتال و تجهیزات عکاسی',
                'department_slugs': ['electronics']
            },
            # Fashion categories
            {
                'name': 'لباس مردانه',
                'slug': 'mens-clothing',
                'description': 'پوشاک مردانه',
                'department_slugs': ['fashion']
            },
            {
                'name': 'لباس زنانه',
                'slug': 'womens-clothing',
                'description': 'پوشاک زنانه',
                'department_slugs': ['fashion']
            },
            {
                'name': 'کفش',
                'slug': 'shoes',
                'description': 'کفش مردانه و زنانه',
                'department_slugs': ['fashion']
            },
            # Home & Kitchen categories
            {
                'name': 'لوازم آشپزخانه',
                'slug': 'kitchen-appliances',
                'description': 'لوازم و تجهیزات آشپزخانه',
                'department_slugs': ['home-kitchen']
            },
            {
                'name': 'مبلمان',
                'slug': 'furniture',
                'description': 'مبل، میز و صندلی',
                'department_slugs': ['home-kitchen']
            },
            {
                'name': 'دکوراسیون',
                'slug': 'decoration',
                'description': 'لوازم دکوری و تزیینی',
                'department_slugs': ['home-kitchen']
            },
            # Sports categories
            {
                'name': 'تجهیزات ورزشی',
                'slug': 'sports-equipment',
                'description': 'وسایل و تجهیزات ورزشی',
                'department_slugs': ['sports']
            },
            {
                'name': 'پوشاک ورزشی',
                'slug': 'sports-clothing',
                'description': 'لباس و کفش ورزشی',
                'department_slugs': ['sports']
            },
            # Books & Media categories
            {
                'name': 'کتاب',
                'slug': 'books',
                'description': 'کتاب‌های چاپی و دیجیتال',
                'department_slugs': ['books-media']
            },
            {
                'name': 'موسیقی',
                'slug': 'music',
                'description': 'موسیقی و آلات موسیقی',
                'department_slugs': ['books-media']
            },
            # Beauty & Health categories
            {
                'name': 'آرایشی',
                'slug': 'cosmetics',
                'description': 'لوازم آرایشی و زیبایی',
                'department_slugs': ['beauty-health']
            },
            {
                'name': 'بهداشتی',
                'slug': 'hygiene',
                'description': 'محصولات بهداشتی و مراقبت شخصی',
                'department_slugs': ['beauty-health']
            }
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True,
                    'sort_order': 0
                }
            )
            
            # Add departments to category
            for dept_slug in cat_data['department_slugs']:
                dept = Department.objects.get(slug=dept_slug)
                category.departments.add(dept)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ دسته‌بندی ایجاد شد: {category.name}'))
            else:
                self.stdout.write(f'  ○ دسته‌بندی موجود است: {category.name}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ همه داده‌ها با موفقیت ایجاد شدند!'))
        self.stdout.write(f'تعداد بخش‌ها: {Department.objects.filter(is_active=True).count()}')
        self.stdout.write(f'تعداد دسته‌بندی‌ها: {Category.objects.filter(is_active=True).count()}')


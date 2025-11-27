# products/management/commands/populate.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from products.models import Department, Category, Subcategory, Product
from users.models import Supplier
from blog.models import BlogCategory, BlogPost
import random
import re

User = get_user_model()


def generate_persian_slug(name, model_class, existing_pk=None):
    """
    Generate a slug from Persian text.
    Falls back to transliteration or ID-based slug if slugify returns empty.
    """
    # Try to slugify the name
    base_slug = slugify(name)
    
    # If slugify returns empty (common with Persian), create a fallback
    if not base_slug or base_slug.strip() == '':
        # Remove special characters and create a simple slug
        base_slug = re.sub(r'[^\w\s-]', '', name.lower())
        base_slug = re.sub(r'[-\s]+', '-', base_slug)
        # If still empty, use a hash-based fallback
        if not base_slug or base_slug.strip() == '':
            base_slug = f"item-{abs(hash(name)) % 100000}"
    
    # Ensure uniqueness
    slug = base_slug
    counter = 1
    queryset = model_class.objects.all()
    if existing_pk:
        queryset = queryset.exclude(pk=existing_pk)
    
    while queryset.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug


class Command(BaseCommand):
    help = 'Populate staging database with Persian placeholder data: departments, categories, subcategories, suppliers, products, and blog posts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate staging data...'))
        
        # Step 1: Create or get admin user for suppliers
        admin_user, created = User.objects.get_or_create(
            username='admin_staging',
            defaults={
                'email': 'admin@staging.local',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'مدیر',
                'last_name': 'سیستم'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))
        else:
            self.stdout.write(f'Using existing admin user: {admin_user.username}')
        
        # Step 2: Create Departments (Persian)
        self.stdout.write('\n--- Creating Departments ---')
        departments_data = [
            {
                'name': 'الکترونیک',
                'description': 'دستگاه‌های الکترونیکی و گجت‌ها',
                'sort_order': 1
            },
            {
                'name': 'پوشاک و مد',
                'description': 'لباس، کفش و لوازم مد',
                'sort_order': 2
            },
            {
                'name': 'خانه و باغ',
                'description': 'لوازم خانه و باغبانی',
                'sort_order': 3
            },
            {
                'name': 'ورزش و تناسب اندام',
                'description': 'تجهیزات ورزشی و تناسب اندام',
                'sort_order': 4
            },
            {
                'name': 'کتاب و رسانه',
                'description': 'کتاب، فیلم و رسانه دیجیتال',
                'sort_order': 5
            }
        ]
        
        departments = []
        for dept_data in departments_data:
            # Generate slug first
            slug = generate_persian_slug(dept_data['name'], Department)
            
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={
                    **dept_data,
                    'slug': slug  # Explicitly set the slug
                }
            )
            
            # If department exists but has empty slug, update it
            if not created and (not dept.slug or dept.slug.strip() == ''):
                dept.slug = generate_persian_slug(dept_data['name'], Department, existing_pk=dept.pk)
                dept.save(update_fields=['slug'])
            
            departments.append(dept)
            if created:
                self.stdout.write(f'  ✓ Created department: {dept.name}')
            else:
                self.stdout.write(f'  - Using existing department: {dept.name}')
        
        # Step 3: Create Categories (Persian) linked to departments
        self.stdout.write('\n--- Creating Categories ---')
        categories_data = [
            # Electronics department
            {'name': 'موبایل و تبلت', 'description': 'گوشی موبایل و تبلت', 'department': departments[0]},
            {'name': 'لپ تاپ و کامپیوتر', 'description': 'لپ تاپ و کامپیوتر', 'department': departments[0]},
            {'name': 'هدفون و اسپیکر', 'description': 'هدفون و اسپیکر', 'department': departments[0]},
            # Fashion department
            {'name': 'لباس مردانه', 'description': 'لباس‌های مردانه', 'department': departments[1]},
            {'name': 'لباس زنانه', 'description': 'لباس‌های زنانه', 'department': departments[1]},
            {'name': 'کفش', 'description': 'کفش مردانه و زنانه', 'department': departments[1]},
            # Home department
            {'name': 'مبلمان', 'description': 'مبلمان و دکوراسیون', 'department': departments[2]},
            {'name': 'لوازم آشپزخانه', 'description': 'لوازم آشپزخانه', 'department': departments[2]},
            # Sports department
            {'name': 'ورزش‌های هوازی', 'description': 'تجهیزات ورزش‌های هوازی', 'department': departments[3]},
            {'name': 'ورزش‌های قدرتی', 'description': 'تجهیزات ورزش‌های قدرتی', 'department': departments[3]},
        ]
        
        categories = []
        for cat_data in categories_data:
            # Generate slug first
            slug = generate_persian_slug(cat_data['name'], Category)
            
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': slug
                }
            )
            
            # If category exists but has empty slug, update it
            if not created and (not category.slug or category.slug.strip() == ''):
                category.slug = generate_persian_slug(cat_data['name'], Category, existing_pk=category.pk)
                category.save(update_fields=['slug'])
            
            # Link to department
            category.departments.add(cat_data['department'])
            categories.append(category)
            if created:
                self.stdout.write(f'  ✓ Created category: {category.name}')
            else:
                self.stdout.write(f'  - Using existing category: {category.name}')
        
        # Step 4: Create Subcategories (Persian) linked to categories
        self.stdout.write('\n--- Creating Subcategories ---')
        subcategories_data = [
            # Mobile and Tablet
            {'name': 'گوشی هوشمند', 'description': 'گوشی‌های هوشمند', 'category': categories[0]},
            {'name': 'تبلت', 'description': 'تبلت‌ها', 'category': categories[0]},
            # Laptop and Computer
            {'name': 'لپ تاپ', 'description': 'لپ تاپ‌ها', 'category': categories[1]},
            {'name': 'کامپیوتر رومیزی', 'description': 'کامپیوترهای رومیزی', 'category': categories[1]},
            # Headphones and Speakers
            {'name': 'هدفون بی‌سیم', 'description': 'هدفون‌های بی‌سیم', 'category': categories[2]},
            {'name': 'اسپیکر بلوتوث', 'description': 'اسپیکرهای بلوتوث', 'category': categories[2]},
            # Men's Clothing
            {'name': 'تی‌شرت', 'description': 'تی‌شرت مردانه', 'category': categories[3]},
            {'name': 'شلوار', 'description': 'شلوار مردانه', 'category': categories[3]},
            # Women's Clothing
            {'name': 'لباس', 'description': 'لباس زنانه', 'category': categories[4]},
            {'name': 'شال و روسری', 'description': 'شال و روسری', 'category': categories[4]},
            # Shoes
            {'name': 'کفش مردانه', 'description': 'کفش‌های مردانه', 'category': categories[5]},
            {'name': 'کفش زنانه', 'description': 'کفش‌های زنانه', 'category': categories[5]},
            # Furniture
            {'name': 'مبل', 'description': 'مبلمان راحتی', 'category': categories[6]},
            {'name': 'میز و صندلی', 'description': 'میز و صندلی', 'category': categories[6]},
            # Kitchen
            {'name': 'قابلمه و تابه', 'description': 'قابلمه و تابه', 'category': categories[7]},
            {'name': 'ظروف غذاخوری', 'description': 'ظروف غذاخوری', 'category': categories[7]},
            # Aerobic Sports
            {'name': 'دوچرخه ثابت', 'description': 'دوچرخه‌های ثابت', 'category': categories[8]},
            {'name': 'تردمیل', 'description': 'تردمیل', 'category': categories[8]},
            # Strength Sports
            {'name': 'دمبل و هالتر', 'description': 'دمبل و هالتر', 'category': categories[9]},
            {'name': 'نیمکت ورزشی', 'description': 'نیمکت‌های ورزشی', 'category': categories[9]},
        ]
        
        subcategories = []
        for subcat_data in subcategories_data:
            # Generate slug first
            slug = generate_persian_slug(subcat_data['name'], Subcategory)
            
            subcategory, created = Subcategory.objects.get_or_create(
                name=subcat_data['name'],
                defaults={
                    'description': subcat_data['description'],
                    'slug': slug
                }
            )
            
            # If subcategory exists but has empty slug, update it
            if not created and (not subcategory.slug or subcategory.slug.strip() == ''):
                subcategory.slug = generate_persian_slug(subcat_data['name'], Subcategory, existing_pk=subcategory.pk)
                subcategory.save(update_fields=['slug'])
            
            # Link to category
            subcategory.categories.add(subcat_data['category'])
            subcategories.append(subcategory)
            if created:
                self.stdout.write(f'  ✓ Created subcategory: {subcategory.name}')
            else:
                self.stdout.write(f'  - Using existing subcategory: {subcategory.name}')
        
        # Step 5: Create Suppliers (Persian)
        self.stdout.write('\n--- Creating Suppliers ---')
        suppliers_data = [
            {
                'name': 'شرکت الکترونیک پارس',
                'website': 'https://example.com/pars-electronics',
                'phone': '021-12345678',
                'mobile': '09121234567',
                'email': 'info@pars-electronics.local',
                'address': 'تهران، خیابان ولیعصر، پلاک 123',
                'description': 'شرکت پیشرو در زمینه فروش تجهیزات الکترونیکی و دیجیتال'
            },
            {
                'name': 'فروشگاه مد و پوشاک تهران',
                'website': 'https://example.com/tehran-fashion',
                'phone': '021-87654321',
                'mobile': '09129876543',
                'email': 'info@tehran-fashion.local',
                'address': 'تهران، خیابان جمهوری، پلاک 456',
                'description': 'فروشگاه تخصصی پوشاک و مد روز با کیفیت بالا'
            },
            {
                'name': 'لوازم خانگی بهینه',
                'website': 'https://example.com/behine-home',
                'phone': '021-11223344',
                'mobile': '09131122334',
                'email': 'info@behine-home.local',
                'address': 'تهران، خیابان آزادی، پلاک 789',
                'description': 'تامین کننده لوازم خانگی و دکوراسیون منزل'
            },
            {
                'name': 'ورزش و تناسب اندام ایران',
                'website': 'https://example.com/iran-sports',
                'phone': '021-55667788',
                'mobile': '09145566778',
                'email': 'info@iran-sports.local',
                'address': 'تهران، خیابان انقلاب، پلاک 321',
                'description': 'فروشگاه تخصصی تجهیزات ورزشی و تناسب اندام'
            },
            {
                'name': 'کتاب و فرهنگ',
                'website': 'https://example.com/book-culture',
                'phone': '021-99887766',
                'mobile': '09159988776',
                'email': 'info@book-culture.local',
                'address': 'تهران، خیابان کریمخان، پلاک 654',
                'description': 'فروشگاه کتاب و محصولات فرهنگی'
            }
        ]
        
        suppliers = []
        for supplier_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=supplier_data['name'],
                website=supplier_data['website'],
                defaults={
                    **supplier_data,
                    'vendor': admin_user
                }
            )
            suppliers.append(supplier)
            if created:
                self.stdout.write(f'  ✓ Created supplier: {supplier.name}')
            else:
                self.stdout.write(f'  - Using existing supplier: {supplier.name}')
        
        # Step 6: Create Products (Persian) linked to suppliers and subcategories
        self.stdout.write('\n--- Creating Products ---')
        products_data = [
            # Electronics products
            {
                'name': 'گوشی هوشمند سامسونگ گلکسی S24',
                'description': 'گوشی هوشمند با صفحه نمایش 6.2 اینچی، دوربین 50 مگاپیکسلی و پردازنده قدرتمند',
                'price': 25000000,  # 25,000,000 Toman in smallest unit
                'stock': 15,
                'supplier': suppliers[0],
                'subcategory': subcategories[0],  # گوشی هوشمند
                'primary_category': categories[0]  # موبایل و تبلت
            },
            {
                'name': 'تبلت اپل آیپد پرو',
                'description': 'تبلت 11 اینچی با پردازنده M2 و صفحه نمایش Liquid Retina',
                'price': 35000000,
                'stock': 8,
                'supplier': suppliers[0],
                'subcategory': subcategories[1],  # تبلت
                'primary_category': categories[0]
            },
            {
                'name': 'لپ تاپ لنوو ThinkPad',
                'description': 'لپ تاپ 14 اینچی با پردازنده Intel Core i7 و 16GB RAM',
                'price': 45000000,
                'stock': 12,
                'supplier': suppliers[0],
                'subcategory': subcategories[2],  # لپ تاپ
                'primary_category': categories[1]  # لپ تاپ و کامپیوتر
            },
            {
                'name': 'هدفون سونی WH-1000XM5',
                'description': 'هدفون بی‌سیم با حذف نویز فعال و باتری 30 ساعته',
                'price': 12000000,
                'stock': 25,
                'supplier': suppliers[0],
                'subcategory': subcategories[4],  # هدفون بی‌سیم
                'primary_category': categories[2]  # هدفون و اسپیکر
            },
            # Fashion products
            {
                'name': 'تی‌شرت مردانه پنبه‌ای',
                'description': 'تی‌شرت مردانه از جنس پنبه 100% با طراحی ساده و راحت',
                'price': 250000,
                'stock': 50,
                'supplier': suppliers[1],
                'subcategory': subcategories[6],  # تی‌شرت
                'primary_category': categories[3]  # لباس مردانه
            },
            {
                'name': 'شلوار جین مردانه',
                'description': 'شلوار جین کلاسیک با برش راسته و جنس با کیفیت',
                'price': 800000,
                'stock': 30,
                'supplier': suppliers[1],
                'subcategory': subcategories[7],  # شلوار
                'primary_category': categories[3]
            },
            {
                'name': 'لباس زنانه تابستانی',
                'description': 'لباس زنانه با پارچه خنک و مناسب فصل تابستان',
                'price': 600000,
                'stock': 40,
                'supplier': suppliers[1],
                'subcategory': subcategories[8],  # لباس
                'primary_category': categories[4]  # لباس زنانه
            },
            # Home products
            {
                'name': 'مبل راحتی 3 نفره',
                'description': 'مبل راحتی با روکش پارچه و طراحی مدرن',
                'price': 15000000,
                'stock': 5,
                'supplier': suppliers[2],
                'subcategory': subcategories[12],  # مبل
                'primary_category': categories[6]  # مبلمان
            },
            {
                'name': 'ست قابلمه استیل',
                'description': 'ست 5 تکه قابلمه از جنس استیل ضد زنگ',
                'price': 2000000,
                'stock': 20,
                'supplier': suppliers[2],
                'subcategory': subcategories[14],  # قابلمه و تابه
                'primary_category': categories[7]  # لوازم آشپزخانه
            },
            # Sports products
            {
                'name': 'دوچرخه ثابت ورزشی',
                'description': 'دوچرخه ثابت با نمایشگر دیجیتال و تنظیم مقاومت',
                'price': 8000000,
                'stock': 10,
                'supplier': suppliers[3],
                'subcategory': subcategories[16],  # دوچرخه ثابت
                'primary_category': categories[8]  # ورزش‌های هوازی
            },
            {
                'name': 'دمبل قابل تنظیم',
                'description': 'ست دمبل قابل تنظیم از 2.5 تا 25 کیلوگرم',
                'price': 3000000,
                'stock': 15,
                'supplier': suppliers[3],
                'subcategory': subcategories[18],  # دمبل و هالتر
                'primary_category': categories[9]  # ورزش‌های قدرتی
            }
        ]
        
        products_created = 0
        for product_data in products_data:
            # Generate unique slug using helper function
            slug = generate_persian_slug(product_data['name'], Product)
            
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'vendor': admin_user,
                    'supplier': product_data['supplier'],
                    'primary_category': product_data['primary_category'],
                    'is_active': True
                }
            )
            
            # Add subcategory
            if product_data.get('subcategory'):
                product.subcategories.add(product_data['subcategory'])
            
            if created:
                products_created += 1
                self.stdout.write(f'  ✓ Created product: {product.name}')
            else:
                self.stdout.write(f'  - Using existing product: {product.name}')
        
        # Step 7: Create Blog Categories (Persian)
        self.stdout.write('\n--- Creating Blog Categories ---')
        blog_categories_data = [
            {
                'name': 'فناوری',
                'description': 'مقالات مربوط به فناوری و تکنولوژی',
                'color': '#007bff'
            },
            {
                'name': 'تجارت',
                'description': 'مقالات مربوط به تجارت و کسب و کار',
                'color': '#28a745'
            },
            {
                'name': 'سبک زندگی',
                'description': 'مقالات مربوط به سبک زندگی و سلامت',
                'color': '#ffc107'
            },
            {
                'name': 'آموزش',
                'description': 'مقالات آموزشی و راهنما',
                'color': '#dc3545'
            },
            {
                'name': 'اخبار',
                'description': 'اخبار و رویدادهای روز',
                'color': '#17a2b8'
            }
        ]
        
        blog_categories = []
        for blog_cat_data in blog_categories_data:
            # Generate slug first
            slug = generate_persian_slug(blog_cat_data['name'], BlogCategory)
            
            blog_category, created = BlogCategory.objects.get_or_create(
                name=blog_cat_data['name'],
                defaults={
                    **blog_cat_data,
                    'slug': slug
                }
            )
            
            # If blog category exists but has empty slug, update it
            if not created and (not blog_category.slug or blog_category.slug.strip() == ''):
                blog_category.slug = generate_persian_slug(blog_cat_data['name'], BlogCategory, existing_pk=blog_category.pk)
                blog_category.save(update_fields=['slug'])
            
            blog_categories.append(blog_category)
            if created:
                self.stdout.write(f'  ✓ Created blog category: {blog_category.name}')
            else:
                self.stdout.write(f'  - Using existing blog category: {blog_category.name}')
        
        # Step 8: Create Blog Posts (Persian)
        self.stdout.write('\n--- Creating Blog Posts ---')
        blog_posts_data = [
            {
                'title': 'راهنمای خرید گوشی هوشمند در سال 1403',
                'excerpt': 'نکات مهم برای انتخاب بهترین گوشی هوشمند با توجه به نیازهای شما',
                'content': '''<p>انتخاب گوشی هوشمند مناسب می‌تواند کار دشواری باشد با توجه به تنوع زیاد در بازار. در این مقاله به بررسی نکات مهم برای خرید گوشی هوشمند می‌پردازیم.</p>
                
                <h2>مهم‌ترین فاکتورها</h2>
                <ul>
                <li><strong>پردازنده:</strong> قدرت پردازنده یکی از مهم‌ترین فاکتورهاست</li>
                <li><strong>دوربین:</strong> کیفیت دوربین برای عکاسی و فیلمبرداری</li>
                <li><strong>باتری:</strong> ظرفیت باتری و طول عمر آن</li>
                <li><strong>صفحه نمایش:</strong> کیفیت و اندازه صفحه نمایش</li>
                </ul>
                
                <h2>نتیجه‌گیری</h2>
                <p>با در نظر گیری این فاکتورها می‌توانید بهترین انتخاب را داشته باشید.</p>''',
                'category': blog_categories[0],  # فناوری
                'status': 'published',
                'is_featured': True
            },
            {
                'title': 'راه‌اندازی کسب و کار آنلاین موفق',
                'excerpt': 'مراحل راه‌اندازی یک کسب و کار آنلاین موفق و سودآور',
                'content': '''<p>راه‌اندازی کسب و کار آنلاین در دنیای امروز فرصت‌های زیادی را فراهم می‌کند. در این مقاله به مراحل راه‌اندازی یک کسب و کار آنلاین موفق می‌پردازیم.</p>
                
                <h2>مراحل راه‌اندازی</h2>
                <ol>
                <li>انتخاب حوزه فعالیت</li>
                <li>بررسی بازار و رقبا</li>
                <li>طراحی وب‌سایت</li>
                <li>بازاریابی و تبلیغات</li>
                <li>مدیریت و توسعه</li>
                </ol>
                
                <h2>نکات مهم</h2>
                <p>صبر و پشتکار از مهم‌ترین عوامل موفقیت در کسب و کار آنلاین است.</p>''',
                'category': blog_categories[1],  # تجارت
                'status': 'published',
                'is_featured': True
            },
            {
                'title': 'راهکارهای حفظ سلامت در محیط کار',
                'excerpt': 'نکات مهم برای حفظ سلامت جسمی و روحی در محیط کار',
                'content': '''<p>حفظ سلامت در محیط کار از اهمیت بالایی برخوردار است. در این مقاله به راهکارهای عملی برای حفظ سلامت می‌پردازیم.</p>
                
                <h2>نکات مهم</h2>
                <ul>
                <li>نشستن صحیح پشت میز</li>
                <li>استراحت منظم</li>
                <li>نوشیدن آب کافی</li>
                <li>ورزش منظم</li>
                </ul>
                
                <p>با رعایت این نکات می‌توانید سلامت خود را در محیط کار حفظ کنید.</p>''',
                'category': blog_categories[2],  # سبک زندگی
                'status': 'published',
                'is_featured': False
            },
            {
                'title': 'آموزش مقدماتی برنامه‌نویسی پایتون',
                'excerpt': 'شروع یادگیری برنامه‌نویسی با زبان پایتون',
                'content': '''<p>پایتون یکی از محبوب‌ترین زبان‌های برنامه‌نویسی است که برای مبتدیان بسیار مناسب است.</p>
                
                <h2>مقدمات پایتون</h2>
                <p>پایتون یک زبان سطح بالا و تفسیری است که خوانایی بالایی دارد.</p>
                
                <h3>نصب پایتون</h3>
                <p>برای شروع کار با پایتون ابتدا باید آن را نصب کنید.</p>
                
                <h3>اولین برنامه</h3>
                <pre><code>print("سلام دنیا!")</code></pre>
                
                <p>با این کد ساده می‌توانید اولین برنامه خود را بنویسید.</p>''',
                'category': blog_categories[3],  # آموزش
                'status': 'published',
                'is_featured': True
            },
            {
                'title': 'اخبار تکنولوژی هفته',
                'excerpt': 'خلاصه اخبار مهم تکنولوژی در هفته گذشته',
                'content': '''<p>در این هفته اخبار مهمی در حوزه تکنولوژی منتشر شده است.</p>
                
                <h2>اخبار مهم</h2>
                <ul>
                <li>رونمایی از محصولات جدید</li>
                <li>به‌روزرسانی‌های نرم‌افزاری</li>
                <li>روندهای جدید در صنعت</li>
                </ul>
                
                <p>برای اطلاعات بیشتر به منابع خبری معتبر مراجعه کنید.</p>''',
                'category': blog_categories[4],  # اخبار
                'status': 'published',
                'is_featured': False
            }
        ]
        
        blog_posts_created = 0
        for post_data in blog_posts_data:
            # Generate unique slug using helper function
            slug = generate_persian_slug(post_data['title'], BlogPost)
            
            post, created = BlogPost.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': post_data['title'],
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'],
                    'author': admin_user,
                    'category': post_data['category'],
                    'status': post_data['status'],
                    'is_featured': post_data.get('is_featured', False),
                    'published_at': timezone.now() if post_data['status'] == 'published' else None
                }
            )
            
            if created:
                blog_posts_created += 1
                self.stdout.write(f'  ✓ Created blog post: {post.title}')
            else:
                self.stdout.write(f'  - Using existing blog post: {post.title}')
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✓ Population completed successfully!'))
        self.stdout.write('='*60)
        self.stdout.write(f'Summary:')
        self.stdout.write(f'  - Departments: {len(departments)}')
        self.stdout.write(f'  - Categories: {len(categories)}')
        self.stdout.write(f'  - Subcategories: {len(subcategories)}')
        self.stdout.write(f'  - Suppliers: {len(suppliers)}')
        self.stdout.write(f'  - Products: {products_created} created')
        self.stdout.write(f'  - Blog Categories: {len(blog_categories)}')
        self.stdout.write(f'  - Blog Posts: {blog_posts_created} created')
        self.stdout.write('='*60)


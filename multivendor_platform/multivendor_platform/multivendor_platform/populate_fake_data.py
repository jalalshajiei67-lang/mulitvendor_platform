#!/usr/bin/env python
"""
Django management script to populate fake data for the multivendor platform.
All data will be in Persian (Farsi).

Usage:
    python manage.py shell < populate_fake_data.py
    OR
    python populate_fake_data.py (if run from project root with proper Django setup)
"""

import os
import sys
import django
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
import random
import re

# Setup Django environment
if __name__ == '__main__':
    # Add the project directory to the Python path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, BASE_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
    django.setup()

from faker import Faker
from faker.providers import BaseProvider
from django.contrib.auth import get_user_model
from products.models import Department, Category, Subcategory, Product
from blog.models import BlogCategory, BlogPost
from users.models import VendorProfile, Supplier

User = get_user_model()

# Initialize Faker with Persian locale
fake = Faker('fa_IR')
Faker.seed(42)  # For reproducible results

# Persian-specific data providers
class PersianProvider(BaseProvider):
    """Custom provider for Persian-specific fake data"""
    
    # Persian department names
    departments = [
        'الکترونیک و دیجیتال',
        'پوشاک و مد',
        'خانه و آشپزخانه',
        'کتاب و لوازم تحریر',
        'ورزش و سفر',
        'زیبایی و سلامت',
        'خودرو و موتورسیکلت',
        'کودک و نوزاد',
        'صنعتی و تجاری',
        'غذا و نوشیدنی',
    ]
    
    # Persian category names
    categories = {
        'الکترونیک و دیجیتال': [
            'موبایل و تبلت',
            'لپ تاپ و کامپیوتر',
            'گوشی و هدفون',
            'دوربین و عکاسی',
            'گیمینگ',
        ],
        'پوشاک و مد': [
            'لباس مردانه',
            'لباس زنانه',
            'کفش',
            'اکسسوری',
            'ساعت و جواهرات',
        ],
        'خانه و آشپزخانه': [
            'مبلمان',
            'دکوراسیون',
            'ظروف آشپزخانه',
            'لوازم برقی',
            'رختخواب و حمام',
        ],
        'کتاب و لوازم تحریر': [
            'کتاب',
            'لوازم تحریر',
            'نقاشی و طراحی',
            'مجلات',
        ],
        'ورزش و سفر': [
            'ورزشی',
            'سفر و گردشگری',
            'کمپینگ',
            'اسباب بازی',
        ],
        'زیبایی و سلامت': [
            'آرایشی',
            'بهداشتی',
            'عطر و ادکلن',
            'مراقبت پوست',
        ],
        'خودرو و موتورسیکلت': [
            'قطعات خودرو',
            'لوازم جانبی',
            'موتورسیکلت',
        ],
        'کودک و نوزاد': [
            'لباس کودک',
            'اسباب بازی',
            'لوازم نوزاد',
        ],
        'صنعتی و تجاری': [
            'ماشین آلات',
            'ابزار',
            'مواد اولیه',
        ],
        'غذا و نوشیدنی': [
            'مواد غذایی',
            'نوشیدنی',
            'شیرینی و شکلات',
        ],
    }
    
    # Persian subcategory names
    subcategories = {
        'موبایل و تبلت': ['گوشی هوشمند', 'تبلت', 'قاب و محافظ', 'شارژر'],
        'لپ تاپ و کامپیوتر': ['لپ تاپ', 'کامپیوتر رومیزی', 'ماوس و کیبورد', 'مانیتور'],
        'لباس مردانه': ['تی شرت', 'شلوار', 'کت و شلوار', 'لباس ورزشی'],
        'لباس زنانه': ['لباس', 'دامن', 'شلوار', 'لباس مجلسی'],
        'کفش': ['کفش ورزشی', 'کفش رسمی', 'صندل', 'بوت'],
        'مبلمان': ['مبل', 'صندلی', 'میز', 'کمد'],
        'دکوراسیون': ['تابلو', 'گلدان', 'روشنایی', 'پرده'],
        'ظروف آشپزخانه': ['قابلمه', 'ظروف چینی', 'چاقو', 'سرویس قاشق و چنگال'],
        'کتاب': ['رمان', 'تاریخی', 'علمی', 'کودک'],
        'ورزشی': ['توپ', 'لباس ورزشی', 'کفش ورزشی', 'لوازم بدنسازی'],
        'آرایشی': ['رژ لب', 'سایه چشم', 'فونداسیون', 'ریمل'],
        'قطعات خودرو': ['موتور', 'گیربکس', 'لاستیک', 'باتری'],
    }
    
    # Persian company/vendor names
    company_suffixes = ['شرکت', 'گروه', 'صنایع', 'کارخانه', 'تولیدی', 'توزیع']
    company_types = ['الکترونیک', 'پوشاک', 'صنعتی', 'غذایی', 'خودرو', 'ساختمانی']
    
    def persian_department(self):
        return self.random_element(self.departments)
    
    def persian_category(self, department=None):
        if department and department in self.categories:
            return self.random_element(self.categories[department])
        # Return random category from any department
        all_categories = []
        for cats in self.categories.values():
            all_categories.extend(cats)
        return self.random_element(all_categories)
    
    def persian_subcategory(self, category=None):
        if category and category in self.subcategories:
            return self.random_element(self.subcategories[category])
        # Return random subcategory
        all_subcategories = []
        for subs in self.subcategories.values():
            all_subcategories.extend(subs)
        return self.random_element(all_subcategories) if all_subcategories else 'زیردسته تست'
    
    def persian_company_name(self):
        suffix = self.random_element(self.company_suffixes)
        company_type = self.random_element(self.company_types)
        name = fake.company()
        return f"{suffix} {company_type} {name.split()[0]}"
    
    def persian_product_name(self, subcategory=None):
        adjectives = ['عالی', 'برتر', 'ممتاز', 'ویژه', 'حرفه‌ای', 'پیشرفته']
        adjective = self.random_element(adjectives)
        base_name = fake.word()
        return f"{base_name} {adjective}"


# Add custom provider
fake.add_provider(PersianProvider)


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


def create_departments(count=10):
    """Create fake departments"""
    print(f"Creating {count} departments...")
    departments = []
    for i in range(count):
        dept_name = fake.persian_department()
        # Ensure uniqueness
        while Department.objects.filter(name=dept_name).exists():
            dept_name = fake.persian_department()
        
        # Generate slug manually to avoid empty slug issues
        dept_slug = generate_persian_slug(dept_name, Department)
        
        dept = Department.objects.create(
            name=dept_name,
            slug=dept_slug,
            description=fake.text(max_nb_chars=200),
            meta_title=f"{dept_name} - خرید آنلاین",
            meta_description=fake.text(max_nb_chars=160),
            is_active=True,
            sort_order=i,
        )
        departments.append(dept)
        print(f"  ✓ Created department: {dept.name} (slug: {dept.slug})")
    return departments


def create_categories(departments, count_per_dept=3):
    """Create fake categories linked to departments"""
    print(f"\nCreating categories (about {count_per_dept} per department)...")
    categories = []
    for dept in departments:
        dept_categories = []
        for i in range(count_per_dept):
            cat_name = fake.persian_category(dept.name)
            # Ensure uniqueness
            while Category.objects.filter(name=cat_name).exists():
                cat_name = fake.persian_category(dept.name)
            
            # Generate slug manually
            cat_slug = generate_persian_slug(cat_name, Category)
            
            cat = Category.objects.create(
                name=cat_name,
                slug=cat_slug,
                description=fake.text(max_nb_chars=200),
                meta_title=f"{cat_name} - خرید آنلاین",
                meta_description=fake.text(max_nb_chars=160),
                is_active=True,
                sort_order=i,
            )
            cat.departments.add(dept)
            categories.append(cat)
            dept_categories.append(cat)
            print(f"  ✓ Created category: {cat.name} (in {dept.name})")
    return categories


def create_subcategories(categories, count_per_cat=2):
    """Create fake subcategories linked to categories"""
    print(f"\nCreating subcategories (about {count_per_cat} per category)...")
    subcategories = []
    for cat in categories:
        cat_subcategories = []
        for i in range(count_per_cat):
            subcat_name = fake.persian_subcategory(cat.name)
            # Ensure uniqueness
            while Subcategory.objects.filter(name=subcat_name).exists():
                subcat_name = fake.persian_subcategory(cat.name)
            
            # Generate slug manually
            subcat_slug = generate_persian_slug(subcat_name, Subcategory)
            
            subcat = Subcategory.objects.create(
                name=subcat_name,
                slug=subcat_slug,
                description=fake.text(max_nb_chars=200),
                meta_title=f"{subcat_name} - خرید آنلاین",
                meta_description=fake.text(max_nb_chars=160),
                is_active=True,
                sort_order=i,
            )
            subcat.categories.add(cat)
            subcategories.append(subcat)
            cat_subcategories.append(subcat)
            print(f"  ✓ Created subcategory: {subcat.name} (in {cat.name})")
    return subcategories


def create_vendors(count=10):
    """Create fake vendors (users with VendorProfile)"""
    print(f"\nCreating {count} vendors...")
    vendors = []
    for i in range(count):
        # Create user
        username = fake.user_name() + str(random.randint(1000, 9999))
        email = fake.email()
        # Ensure uniqueness
        while User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            username = fake.user_name() + str(random.randint(1000, 9999))
            email = fake.email()
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password='testpass123',  # Default password for fake users
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        
        # Create vendor profile
        store_name = fake.persian_company_name()
        while VendorProfile.objects.filter(store_name=store_name).exists():
            store_name = fake.persian_company_name()
        
        vendor_profile = VendorProfile.objects.create(
            user=user,
            store_name=store_name,
            description=fake.text(max_nb_chars=500),
            contact_email=email,
            contact_phone=fake.phone_number(),
            website=fake.url(),
            address=fake.address(),
            about=fake.text(max_nb_chars=300),
            slogan=fake.sentence(nb_words=6),
            year_established=random.randint(1350, 1400),  # Persian year
            employee_count=random.randint(5, 500),
            is_approved=True,
        )
        vendors.append(vendor_profile)
        print(f"  ✓ Created vendor: {vendor_profile.store_name} ({user.username})")
    return vendors


def create_suppliers(vendors, count_per_vendor=2):
    """Create fake suppliers linked to vendors"""
    print(f"\nCreating suppliers (about {count_per_vendor} per vendor)...")
    suppliers = []
    for vendor in vendors:
        for i in range(count_per_vendor):
            supplier_name = fake.persian_company_name()
            website = fake.url()
            # Ensure uniqueness based on name and website
            while Supplier.objects.filter(name=supplier_name, website=website).exists():
                supplier_name = fake.persian_company_name()
                website = fake.url()
            
            supplier = Supplier.objects.create(
                vendor=vendor.user,
                name=supplier_name,
                website=website,
                phone=fake.phone_number(),
                mobile=fake.phone_number(),
                email=fake.email(),
                address=fake.address(),
                description=fake.text(max_nb_chars=300),
                is_active=True,
            )
            suppliers.append(supplier)
            print(f"  ✓ Created supplier: {supplier.name} (managed by {vendor.store_name})")
    return suppliers


def create_products(vendors, suppliers, subcategories, count_per_vendor=20):
    """Create fake products"""
    print(f"\nCreating products (about {count_per_vendor} per vendor)...")
    products = []
    availability_choices = ['in_stock', 'made_to_order']
    condition_choices = ['new', 'used']
    origin_choices = ['iran', 'imported']
    
    for vendor in vendors:
        vendor_suppliers = [s for s in suppliers if s.vendor == vendor.user]
        vendor_products = []
        
        for i in range(count_per_vendor):
            # Select random subcategory
            subcategory = random.choice(subcategories)
            
            # Select supplier if available
            supplier = random.choice(vendor_suppliers) if vendor_suppliers else None
            
            # Get primary category from subcategory
            primary_category = subcategory.categories.first()
            
            product_name = fake.persian_product_name(subcategory.name)
            # Generate slug manually to avoid empty slug issues
            slug = generate_persian_slug(product_name, Product)
            
            availability = random.choice(availability_choices)
            condition = random.choice(condition_choices) if availability == 'in_stock' else None
            lead_time = random.randint(7, 30) if availability == 'made_to_order' else None
            
            product = Product.objects.create(
                vendor=vendor.user,
                supplier=supplier,
                name=product_name,
                slug=slug,
                description=fake.text(max_nb_chars=1000),
                price=random.randint(100000, 50000000),  # Price in smallest currency unit
                stock=random.randint(0, 1000) if availability == 'in_stock' else 0,
                availability_status=availability,
                condition=condition,
                origin=random.choice(origin_choices),
                lead_time_days=lead_time,
                meta_title=f"{product_name} - خرید آنلاین",
                meta_description=fake.text(max_nb_chars=160),
                is_active=True,
                primary_category=primary_category,
            )
            product.subcategories.add(subcategory)
            products.append(product)
            vendor_products.append(product)
        
        print(f"  ✓ Created {len(vendor_products)} products for {vendor.store_name}")
    
    return products


def create_blog_categories(count=8):
    """Create fake blog categories"""
    print(f"\nCreating {count} blog categories...")
    blog_categories = []
    colors = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1', '#e83e8c', '#fd7e14']
    
    blog_category_names = [
        'اخبار و رویدادها',
        'راهنمای خرید',
        'نقد و بررسی',
        'آموزش و ترفندها',
        'مقایسه محصولات',
        'راهنمای استفاده',
        'صنعت و فناوری',
        'سبک زندگی',
    ]
    
    for i, name in enumerate(blog_category_names[:count]):
        # Ensure uniqueness
        while BlogCategory.objects.filter(name=name).exists():
            name = name + " " + str(random.randint(1, 100))
        
        # Generate slug manually
        blog_cat_slug = generate_persian_slug(name, BlogCategory)
        
        blog_cat = BlogCategory.objects.create(
            name=name,
            slug=blog_cat_slug,
            description=fake.text(max_nb_chars=200),
            color=colors[i % len(colors)],
            is_active=True,
        )
        blog_categories.append(blog_cat)
        print(f"  ✓ Created blog category: {blog_cat.name}")
    
    return blog_categories


def create_blog_posts(blog_categories, vendors, count_per_category=5):
    """Create fake blog posts"""
    print(f"\nCreating blog posts (about {count_per_category} per category)...")
    blog_posts = []
    status_choices = ['draft', 'published', 'published', 'published']  # More published than draft
    
    for blog_cat in blog_categories:
        for i in range(count_per_category):
            # Select random author from vendors
            author = random.choice(vendors).user
            
            title = fake.sentence(nb_words=6)
            # Generate slug manually to avoid empty slug issues
            slug = generate_persian_slug(title, BlogPost)
            
            status = random.choice(status_choices)
            published_at = timezone.now() - timedelta(days=random.randint(0, 90)) if status == 'published' else None
            
            post = BlogPost.objects.create(
                author=author,
                category=blog_cat,
                title=title,
                slug=slug,
                excerpt=fake.text(max_nb_chars=500),
                content=fake.text(max_nb_chars=2000),
                status=status,
                is_featured=random.choice([True, False, False, False]),  # 25% featured
                view_count=random.randint(0, 10000) if status == 'published' else 0,
                published_at=published_at,
                meta_title=f"{title} - بلاگ",
                meta_description=fake.text(max_nb_chars=300),
            )
            blog_posts.append(post)
            print(f"  ✓ Created blog post: {post.title} ({status})")
    
    return blog_posts


def fix_empty_slugs():
    """Fix any existing empty slugs in the database"""
    print("\nChecking for empty slugs...")
    
    # Fix Department empty slugs
    depts_with_empty_slug = Department.objects.filter(slug__isnull=True) | Department.objects.filter(slug='')
    for dept in depts_with_empty_slug:
        dept.slug = generate_persian_slug(dept.name, Department, existing_pk=dept.pk)
        dept.save(update_fields=['slug'])
        print(f"  ✓ Fixed slug for department: {dept.name}")
    
    # Fix Category empty slugs
    cats_with_empty_slug = Category.objects.filter(slug__isnull=True) | Category.objects.filter(slug='')
    for cat in cats_with_empty_slug:
        cat.slug = generate_persian_slug(cat.name, Category, existing_pk=cat.pk)
        cat.save(update_fields=['slug'])
        print(f"  ✓ Fixed slug for category: {cat.name}")
    
    # Fix Subcategory empty slugs
    subcats_with_empty_slug = Subcategory.objects.filter(slug__isnull=True) | Subcategory.objects.filter(slug='')
    for subcat in subcats_with_empty_slug:
        subcat.slug = generate_persian_slug(subcat.name, Subcategory, existing_pk=subcat.pk)
        subcat.save(update_fields=['slug'])
        print(f"  ✓ Fixed slug for subcategory: {subcat.name}")
    
    # Fix BlogCategory empty slugs
    blog_cats_with_empty_slug = BlogCategory.objects.filter(slug__isnull=True) | BlogCategory.objects.filter(slug='')
    for blog_cat in blog_cats_with_empty_slug:
        blog_cat.slug = generate_persian_slug(blog_cat.name, BlogCategory, existing_pk=blog_cat.pk)
        blog_cat.save(update_fields=['slug'])
        print(f"  ✓ Fixed slug for blog category: {blog_cat.name}")
    
    # Fix BlogPost empty slugs
    posts_with_empty_slug = BlogPost.objects.filter(slug__isnull=True) | BlogPost.objects.filter(slug='')
    for post in posts_with_empty_slug:
        post.slug = generate_persian_slug(post.title, BlogPost, existing_pk=post.pk)
        post.save(update_fields=['slug'])
        print(f"  ✓ Fixed slug for blog post: {post.title}")
    
    # Fix Product empty slugs
    products_with_empty_slug = Product.objects.filter(slug__isnull=True) | Product.objects.filter(slug='')
    for product in products_with_empty_slug:
        product.slug = generate_persian_slug(product.name, Product, existing_pk=product.pk)
        product.save(update_fields=['slug'])
        print(f"  ✓ Fixed slug for product: {product.name}")


def main():
    """Main function to populate all fake data"""
    print("=" * 60)
    print("Starting fake data population (Persian/Farsi)")
    print("=" * 60)
    
    # Fix any existing empty slugs first
    fix_empty_slugs()
    
    # Check if data already exists
    if Department.objects.exists():
        response = input("\n⚠️  Data already exists. Continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
    
    try:
        # Create departments
        departments = create_departments(count=10)
        
        # Create categories
        categories = create_categories(departments, count_per_dept=3)
        
        # Create subcategories
        subcategories = create_subcategories(categories, count_per_cat=2)
        
        # Create vendors
        vendors = create_vendors(count=10)
        
        # Create suppliers
        suppliers = create_suppliers(vendors, count_per_vendor=2)
        
        # Create products
        products = create_products(vendors, suppliers, subcategories, count_per_vendor=20)
        
        # Create blog categories
        blog_categories = create_blog_categories(count=8)
        
        # Create blog posts
        blog_posts = create_blog_posts(blog_categories, vendors, count_per_category=5)
        
        print("\n" + "=" * 60)
        print("✅ Fake data population completed successfully!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  - Departments: {len(departments)}")
        print(f"  - Categories: {len(categories)}")
        print(f"  - Subcategories: {len(subcategories)}")
        print(f"  - Vendors: {len(vendors)}")
        print(f"  - Suppliers: {len(suppliers)}")
        print(f"  - Products: {len(products)}")
        print(f"  - Blog Categories: {len(blog_categories)}")
        print(f"  - Blog Posts: {len(blog_posts)}")
        print("\nNote: All vendor users have password: testpass123")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    main()


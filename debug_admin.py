#!/usr/bin/env python
"""
Django Admin Debug Script
Run this to diagnose admin dashboard issues
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'multivendor_platform', 'multivendor_platform'))
django.setup()

from django.contrib.admin.sites import site
from products.models import Product, Department, Category, Subcategory
from users.models import UserProfile, Supplier
from blog.models import BlogPost, BlogCategory
from orders.models import Order

def check_admin_registration():
    """Check if all models are registered in admin"""
    print("\n" + "="*60)
    print("🔍 CHECKING ADMIN REGISTRATIONS")
    print("="*60)
    
    registered_models = site._registry
    print(f"\n✅ Total Registered Models: {len(registered_models)}\n")
    
    for model, admin_class in registered_models.items():
        print(f"  • {model._meta.label}: {admin_class.__class__.__name__}")
    
    return registered_models

def check_database_data():
    """Check if database has data"""
    print("\n" + "="*60)
    print("📊 CHECKING DATABASE DATA")
    print("="*60)
    
    models_to_check = [
        ('Products', Product),
        ('Departments', Department),
        ('Categories', Category),
        ('Subcategories', Subcategory),
        ('User Profiles', UserProfile),
        ('Suppliers', Supplier),
        ('Blog Posts', BlogPost),
        ('Blog Categories', BlogCategory),
        ('Orders', Order),
    ]
    
    for name, model in models_to_check:
        try:
            count = model.objects.count()
            status = "✅" if count > 0 else "⚠️ EMPTY"
            print(f"\n  {status} {name}: {count} records")
            
            if count > 0 and count <= 3:
                # Show sample data
                print(f"     Sample: {list(model.objects.all()[:3])}")
        except Exception as e:
            print(f"\n  ❌ {name}: ERROR - {str(e)}")

def check_admin_list_display_errors():
    """Test list_display methods for errors"""
    print("\n" + "="*60)
    print("🧪 TESTING LIST_DISPLAY METHODS")
    print("="*60)
    
    # Test Product Admin
    print("\n📦 Testing Product Admin...")
    try:
        products = Product.objects.all()[:1]
        if products:
            product = products[0]
            print(f"  Testing product: {product}")
            
            # Test each custom method
            from products.admin import ProductAdmin
            admin = ProductAdmin(Product, site)
            
            try:
                result = admin.get_subcategories(product)
                print(f"  ✅ get_subcategories(): {result}")
            except Exception as e:
                print(f"  ❌ get_subcategories() ERROR: {e}")
            
            try:
                result = admin.get_category_path(product)
                print(f"  ✅ get_category_path(): {result}")
            except Exception as e:
                print(f"  ❌ get_category_path() ERROR: {e}")
            
            try:
                result = admin.image_count(product)
                print(f"  ✅ image_count(): {result}")
            except Exception as e:
                print(f"  ❌ image_count() ERROR: {e}")
            
            try:
                result = admin.comment_count(product)
                print(f"  ✅ comment_count(): {result}")
            except Exception as e:
                print(f"  ❌ comment_count() ERROR: {e}")
        else:
            print("  ⚠️ No products in database to test")
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
    
    # Test Subcategory Admin
    print("\n📂 Testing Subcategory Admin...")
    try:
        subcategories = Subcategory.objects.all()[:1]
        if subcategories:
            subcat = subcategories[0]
            print(f"  Testing subcategory: {subcat}")
            
            from products.admin import SubcategoryAdmin
            admin = SubcategoryAdmin(Subcategory, site)
            
            try:
                result = admin.get_departments(subcat)
                print(f"  ✅ get_departments(): {result}")
            except Exception as e:
                print(f"  ❌ get_departments() ERROR: {e}")
            
            try:
                result = admin.get_categories(subcat)
                print(f"  ✅ get_categories(): {result}")
            except Exception as e:
                print(f"  ❌ get_categories() ERROR: {e}")
        else:
            print("  ⚠️ No subcategories in database to test")
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def check_migrations():
    """Check if migrations are applied"""
    print("\n" + "="*60)
    print("🔄 CHECKING MIGRATIONS")
    print("="*60)
    
    from django.db import connection
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT app, name FROM django_migrations ORDER BY app, name")
        migrations = cursor.fetchall()
        
        apps = {}
        for app, name in migrations:
            if app not in apps:
                apps[app] = []
            apps[app].append(name)
        
        print(f"\n✅ Migrations applied for {len(apps)} apps:\n")
        for app, migration_list in sorted(apps.items()):
            print(f"  • {app}: {len(migration_list)} migrations")
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def check_static_files():
    """Check static files configuration"""
    print("\n" + "="*60)
    print("📁 CHECKING STATIC FILES CONFIG")
    print("="*60)
    
    from django.conf import settings
    
    print(f"\n  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  DEBUG: {settings.DEBUG}")
    
    if os.path.exists(settings.STATIC_ROOT):
        static_files = len([f for f in os.listdir(settings.STATIC_ROOT) if os.path.isfile(os.path.join(settings.STATIC_ROOT, f))])
        print(f"  ✅ STATIC_ROOT exists with {static_files} files")
    else:
        print(f"  ⚠️ STATIC_ROOT directory doesn't exist - run: python manage.py collectstatic")

def check_superuser():
    """Check if superuser exists"""
    print("\n" + "="*60)
    print("👤 CHECKING SUPERUSER")
    print("="*60)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    superusers = User.objects.filter(is_superuser=True)
    print(f"\n  Superusers found: {superusers.count()}")
    
    for user in superusers:
        print(f"    • {user.username} ({user.email})")
        print(f"      - is_active: {user.is_active}")
        print(f"      - is_staff: {user.is_staff}")
        print(f"      - is_superuser: {user.is_superuser}")

def main():
    print("\n" + "="*70)
    print("🔧 DJANGO ADMIN DIAGNOSTIC TOOL")
    print("="*70)
    
    try:
        check_admin_registration()
        check_database_data()
        check_admin_list_display_errors()
        check_migrations()
        check_static_files()
        check_superuser()
        
        print("\n" + "="*70)
        print("✅ DIAGNOSTIC COMPLETE")
        print("="*70)
        print("\n📝 Check the output above for any ❌ or ⚠️ symbols")
        print("   These indicate issues that need to be fixed.\n")
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()


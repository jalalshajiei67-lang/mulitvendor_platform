#!/usr/bin/env python
"""
Script to check for missing image files referenced in the database.
Run this in Django shell or as a management command.
"""
import os
from django.core.files.storage import default_storage
from multivendor_platform.products.models import ProductImage, Product
from multivendor_platform.blog.models import BlogPost


def check_missing_images():
    """Check for missing image files and report them."""
    print("=" * 60)
    print("Checking for missing image files...")
    print("=" * 60)
    
    # Check ProductImages
    print("\n[Product Images]")
    total_product_images = ProductImage.objects.count()
    print(f"Total ProductImage records: {total_product_images}")
    
    missing_product_images = []
    for img in ProductImage.objects.all():
        if img.image:
            try:
                # Check if file exists
                if not default_storage.exists(img.image.name):
                    missing_product_images.append({
                        'id': img.id,
                        'product_id': img.product.id,
                        'product_name': img.product.name,
                        'image_path': img.image.name,
                        'url': img.image.url if hasattr(img.image, 'url') else None
                    })
            except Exception as e:
                print(f"Error checking image {img.id}: {e}")
    
    print(f"Missing ProductImage files: {len(missing_product_images)}")
    if missing_product_images:
        print("\nMissing ProductImage files:")
        for item in missing_product_images[:20]:  # Show first 20
            print(f"  ID {item['id']}: Product '{item['product_name']}' (ID: {item['product_id']})")
            print(f"    Path: {item['image_path']}")
            if item['url']:
                print(f"    URL: {item['url']}")
    
    # Check Products (legacy image field)
    print("\n[Product Legacy Images]")
    products_with_images = Product.objects.exclude(image='')
    print(f"Products with legacy image field: {products_with_images.count()}")
    
    missing_product_legacy = []
    for product in products_with_images:
        if product.image:
            try:
                if not default_storage.exists(product.image.name):
                    missing_product_legacy.append({
                        'id': product.id,
                        'name': product.name,
                        'image_path': product.image.name
                    })
            except Exception as e:
                print(f"Error checking product {product.id}: {e}")
    
    print(f"Missing Product legacy image files: {len(missing_product_legacy)}")
    if missing_product_legacy:
        print("\nMissing Product legacy images:")
        for item in missing_product_legacy[:10]:
            print(f"  Product ID {item['id']}: '{item['name']}'")
            print(f"    Path: {item['image_path']}")
    
    # Check Blog Posts
    print("\n[Blog Post Images]")
    blogs_with_images = BlogPost.objects.exclude(featured_image='')
    print(f"Blog posts with featured images: {blogs_with_images.count()}")
    
    missing_blog_images = []
    for blog in blogs_with_images:
        if blog.featured_image:
            try:
                if not default_storage.exists(blog.featured_image.name):
                    missing_blog_images.append({
                        'id': blog.id,
                        'title': blog.title,
                        'image_path': blog.featured_image.name
                    })
            except Exception as e:
                print(f"Error checking blog {blog.id}: {e}")
    
    print(f"Missing BlogPost image files: {len(missing_blog_images)}")
    if missing_blog_images:
        print("\nMissing BlogPost images:")
        for item in missing_blog_images[:10]:
            print(f"  Blog ID {item['id']}: '{item['title']}'")
            print(f"    Path: {item['image_path']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_missing = len(missing_product_images) + len(missing_product_legacy) + len(missing_blog_images)
    print(f"Total missing image files: {total_missing}")
    print(f"  - ProductImage: {len(missing_product_images)}")
    print(f"  - Product (legacy): {len(missing_product_legacy)}")
    print(f"  - BlogPost: {len(missing_blog_images)}")
    
    return {
        'product_images': missing_product_images,
        'product_legacy': missing_product_legacy,
        'blog_images': missing_blog_images
    }


if __name__ == '__main__':
    import django
    import sys
    import os
    
    # Setup Django
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
    django.setup()
    
    check_missing_images()


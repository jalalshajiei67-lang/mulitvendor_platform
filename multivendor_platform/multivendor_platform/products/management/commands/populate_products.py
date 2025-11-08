# products/management/commands/populate_products.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product, Category
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample product data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample product data...')
        
        # Create or get users
        users_data = [
            {
                'username': 'techvendor',
                'email': 'tech@example.com',
                'first_name': 'Tech',
                'last_name': 'Vendor'
            },
            {
                'username': 'fashionstore',
                'email': 'fashion@example.com',
                'first_name': 'Fashion',
                'last_name': 'Store'
            },
            {
                'username': 'homegoods',
                'email': 'home@example.com',
                'first_name': 'Home',
                'last_name': 'Goods'
            },
            {
                'username': 'sportsgear',
                'email': 'sports@example.com',
                'first_name': 'Sports',
                'last_name': 'Gear'
            }
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            else:
                self.stdout.write(f'Using existing user: {user.username}')
            users.append(user)
        
        # Create or get categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and gadgets'
            },
            {
                'name': 'Fashion & Clothing',
                'description': 'Clothing, shoes, and fashion accessories'
            },
            {
                'name': 'Home & Garden',
                'description': 'Home improvement and garden supplies'
            },
            {
                'name': 'Sports & Fitness',
                'description': 'Sports equipment and fitness gear'
            },
            {
                'name': 'Books & Media',
                'description': 'Books, movies, and digital media'
            },
            {
                'name': 'Health & Beauty',
                'description': 'Health products and beauty supplies'
            },
            {
                'name': 'Automotive',
                'description': 'Car parts and automotive accessories'
            },
            {
                'name': 'Toys & Games',
                'description': 'Toys, games, and entertainment'
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Using existing category: {category.name}')
        
        # Create sample products
        products_data = [
            # Electronics
            {
                'name': 'iPhone 15 Pro',
                'description': 'Latest iPhone with advanced camera system and A17 Pro chip. Features titanium design, ProRAW photography, and all-day battery life.',
                'price': 999.99,
                'stock': 50,
                'category': categories[0],  # Electronics
                'vendor': users[0],  # techvendor
                'is_active': True
            },
            {
                'name': 'MacBook Air M3',
                'description': 'Ultra-thin laptop with M3 chip, 13-inch Liquid Retina display, and up to 18 hours of battery life. Perfect for work and creativity.',
                'price': 1299.99,
                'stock': 25,
                'category': categories[0],  # Electronics
                'vendor': users[0],  # techvendor
                'is_active': True
            },
            {
                'name': 'Sony WH-1000XM5 Headphones',
                'description': 'Industry-leading noise canceling wireless headphones with 30-hour battery life and crystal clear sound quality.',
                'price': 399.99,
                'stock': 75,
                'category': categories[0],  # Electronics
                'vendor': users[0],  # techvendor
                'is_active': True
            },
            {
                'name': 'Samsung 4K Smart TV 55"',
                'description': '55-inch 4K UHD Smart TV with HDR10+ support, built-in streaming apps, and voice control capabilities.',
                'price': 699.99,
                'stock': 15,
                'category': categories[0],  # Electronics
                'vendor': users[0],  # techvendor
                'is_active': True
            },
            {
                'name': 'Nintendo Switch OLED',
                'description': 'Gaming console with 7-inch OLED screen, enhanced audio, and 64GB internal storage. Includes Joy-Con controllers.',
                'price': 349.99,
                'stock': 40,
                'category': categories[0],  # Electronics
                'vendor': users[0],  # techvendor
                'is_active': True
            },
            
            # Fashion & Clothing
            {
                'name': 'Premium Cotton T-Shirt',
                'description': '100% organic cotton t-shirt with modern fit. Available in multiple colors. Soft, breathable, and comfortable for everyday wear.',
                'price': 29.99,
                'stock': 100,
                'category': categories[1],  # Fashion & Clothing
                'vendor': users[1],  # fashionstore
                'is_active': True
            },
            {
                'name': 'Designer Jeans',
                'description': 'High-quality denim jeans with perfect fit and modern styling. Made from premium cotton with stretch for comfort.',
                'price': 89.99,
                'stock': 60,
                'category': categories[1],  # Fashion & Clothing
                'vendor': users[1],  # fashionstore
                'is_active': True
            },
            {
                'name': 'Leather Jacket',
                'description': 'Genuine leather jacket with classic design. Features multiple pockets, zipper closure, and timeless style.',
                'price': 199.99,
                'stock': 20,
                'category': categories[1],  # Fashion & Clothing
                'vendor': users[1],  # fashionstore
                'is_active': True
            },
            {
                'name': 'Running Shoes',
                'description': 'Lightweight running shoes with advanced cushioning technology. Perfect for jogging, training, and everyday wear.',
                'price': 129.99,
                'stock': 80,
                'category': categories[1],  # Fashion & Clothing
                'vendor': users[1],  # fashionstore
                'is_active': True
            },
            {
                'name': 'Winter Coat',
                'description': 'Warm winter coat with water-resistant material and insulated lining. Perfect for cold weather protection.',
                'price': 159.99,
                'stock': 35,
                'category': categories[1],  # Fashion & Clothing
                'vendor': users[1],  # fashionstore
                'is_active': True
            },
            
            # Home & Garden
            {
                'name': 'Smart Home Hub',
                'description': 'Central control hub for all your smart home devices. Compatible with Alexa, Google Assistant, and Apple HomeKit.',
                'price': 149.99,
                'stock': 30,
                'category': categories[2],  # Home & Garden
                'vendor': users[2],  # homegoods
                'is_active': True
            },
            {
                'name': 'Garden Tool Set',
                'description': 'Complete set of professional garden tools including shovel, rake, pruners, and gloves. Perfect for gardening enthusiasts.',
                'price': 79.99,
                'stock': 45,
                'category': categories[2],  # Home & Garden
                'vendor': users[2],  # homegoods
                'is_active': True
            },
            {
                'name': 'LED Desk Lamp',
                'description': 'Adjustable LED desk lamp with multiple brightness levels and color temperatures. USB charging port included.',
                'price': 49.99,
                'stock': 65,
                'category': categories[2],  # Home & Garden
                'vendor': users[2],  # homegoods
                'is_active': True
            },
            {
                'name': 'Air Purifier',
                'description': 'HEPA air purifier with smart sensors and app control. Removes 99.97% of airborne particles and allergens.',
                'price': 299.99,
                'stock': 20,
                'category': categories[2],  # Home & Garden
                'vendor': users[2],  # homegoods
                'is_active': True
            },
            {
                'name': 'Kitchen Knife Set',
                'description': 'Professional-grade stainless steel knife set with wooden block. Includes chef knife, paring knife, and bread knife.',
                'price': 119.99,
                'stock': 25,
                'category': categories[2],  # Home & Garden
                'vendor': users[2],  # homegoods
                'is_active': True
            },
            
            # Sports & Fitness
            {
                'name': 'Yoga Mat Premium',
                'description': 'Non-slip yoga mat with extra cushioning and carrying strap. Perfect for yoga, pilates, and fitness routines.',
                'price': 39.99,
                'stock': 90,
                'category': categories[3],  # Sports & Fitness
                'vendor': users[3],  # sportsgear
                'is_active': True
            },
            {
                'name': 'Dumbbell Set',
                'description': 'Adjustable dumbbell set with weight plates from 5-50 lbs. Perfect for home gym and strength training.',
                'price': 199.99,
                'stock': 15,
                'category': categories[3],  # Sports & Fitness
                'vendor': users[3],  # sportsgear
                'is_active': True
            },
            {
                'name': 'Basketball',
                'description': 'Official size basketball with premium leather construction. Perfect for indoor and outdoor play.',
                'price': 24.99,
                'stock': 50,
                'category': categories[3],  # Sports & Fitness
                'vendor': users[3],  # sportsgear
                'is_active': True
            },
            {
                'name': 'Fitness Tracker',
                'description': 'Smart fitness tracker with heart rate monitor, GPS, and 7-day battery life. Tracks steps, calories, and sleep.',
                'price': 149.99,
                'stock': 40,
                'category': categories[3],  # Sports & Fitness
                'vendor': users[3],  # sportsgear
                'is_active': True
            },
            {
                'name': 'Tennis Racket',
                'description': 'Professional tennis racket with carbon fiber construction and advanced string technology for optimal performance.',
                'price': 179.99,
                'stock': 30,
                'category': categories[3],  # Sports & Fitness
                'vendor': users[3],  # sportsgear
                'is_active': True
            },
            
            # Books & Media
            {
                'name': 'Programming Book: Python Mastery',
                'description': 'Comprehensive guide to Python programming with practical examples and real-world projects. Perfect for beginners and advanced developers.',
                'price': 49.99,
                'stock': 25,
                'category': categories[4],  # Books & Media
                'vendor': users[0],  # techvendor
                'is_active': True
            },
            {
                'name': 'Bluetooth Speaker',
                'description': 'Portable Bluetooth speaker with 360-degree sound and 12-hour battery life. Waterproof design for outdoor use.',
                'price': 79.99,
                'stock': 60,
                'category': categories[4],  # Books & Media
                'vendor': users[0],  # techvendor
                'is_active': True
            },
            {
                'name': 'Wireless Earbuds',
                'description': 'True wireless earbuds with active noise cancellation and 6-hour battery life. Includes charging case.',
                'price': 129.99,
                'stock': 70,
                'category': categories[4],  # Books & Media
                'vendor': users[0],  # techvendor
                'is_active': True
            },
            
            # Health & Beauty
            {
                'name': 'Skincare Set',
                'description': 'Complete skincare routine set with cleanser, toner, moisturizer, and serum. Natural ingredients for all skin types.',
                'price': 89.99,
                'stock': 40,
                'category': categories[5],  # Health & Beauty
                'vendor': users[1],  # fashionstore
                'is_active': True
            },
            {
                'name': 'Electric Toothbrush',
                'description': 'Advanced electric toothbrush with multiple cleaning modes and 2-week battery life. Includes travel case.',
                'price': 99.99,
                'stock': 35,
                'category': categories[5],  # Health & Beauty
                'vendor': users[1],  # fashionstore
                'is_active': True
            },
            {
                'name': 'Hair Dryer Professional',
                'description': 'Professional hair dryer with ionic technology and multiple heat settings. Reduces frizz and speeds up drying time.',
                'price': 79.99,
                'stock': 20,
                'category': categories[5],  # Health & Beauty
                'vendor': users[1],  # fashionstore
                'is_active': True
            },
            
            # Automotive
            {
                'name': 'Car Phone Mount',
                'description': 'Magnetic car phone mount with strong hold and 360-degree rotation. Compatible with all smartphone sizes.',
                'price': 19.99,
                'stock': 80,
                'category': categories[6],  # Automotive
                'vendor': users[2],  # homegoods
                'is_active': True
            },
            {
                'name': 'Car Charger USB',
                'description': 'Dual USB car charger with fast charging technology. Compatible with all devices and includes LED indicator.',
                'price': 15.99,
                'stock': 100,
                'category': categories[6],  # Automotive
                'vendor': users[2],  # homegoods
                'is_active': True
            },
            {
                'name': 'Car Air Freshener',
                'description': 'Long-lasting car air freshener with natural fragrance. Easy to install and lasts up to 30 days.',
                'price': 8.99,
                'stock': 150,
                'category': categories[6],  # Automotive
                'vendor': users[2],  # homegoods
                'is_active': True
            },
            
            # Toys & Games
            {
                'name': 'Board Game Collection',
                'description': 'Family board game collection with 5 popular games. Perfect for family game nights and entertainment.',
                'price': 59.99,
                'stock': 30,
                'category': categories[7],  # Toys & Games
                'vendor': users[3],  # sportsgear
                'is_active': True
            },
            {
                'name': 'Building Blocks Set',
                'description': 'Educational building blocks set with 500 pieces. Encourages creativity and problem-solving skills.',
                'price': 39.99,
                'stock': 45,
                'category': categories[7],  # Toys & Games
                'vendor': users[3],  # sportsgear
                'is_active': True
            },
            {
                'name': 'Remote Control Car',
                'description': 'High-speed remote control car with 2.4GHz controller and rechargeable battery. Perfect for outdoor fun.',
                'price': 79.99,
                'stock': 25,
                'category': categories[7],  # Toys & Games
                'vendor': users[3],  # sportsgear
                'is_active': True
            }
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
            else:
                self.stdout.write(f'Using existing product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated products with sample data!')
        )
        self.stdout.write(f'Created {len(users)} users, {len(categories)} categories, and {len(products_data)} products')

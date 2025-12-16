from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Product, Category, Department, Subcategory, ProductImage
from decimal import Decimal

User = get_user_model()


class DepartmentModelTest(TestCase):
    """Test Department model"""
    
    def test_department_creation(self):
        """Test creating a department"""
        dept = Department.objects.create(
            name='Electronics',
            description='Electronic items'
        )
        self.assertEqual(dept.name, 'Electronics')
        self.assertEqual(dept.slug, 'electronics')
        self.assertTrue(dept.is_active)
    
    def test_department_slug_auto_generation(self):
        """Test that slug is auto-generated from name"""
        dept = Department.objects.create(name='Home & Garden')
        self.assertEqual(dept.slug, 'home-garden')
    
    def test_department_str(self):
        """Test department string representation"""
        dept = Department.objects.create(name='Books')
        self.assertEqual(str(dept), 'Books')


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        """Set up test data"""
        self.department = Department.objects.create(
            name='Electronics',
            slug='electronics'
        )
    
    def test_category_creation(self):
        """Test creating a category"""
        category = Category.objects.create(
            name='Smartphones',
            description='Mobile phones'
        )
        category.departments.add(self.department)
        self.assertEqual(category.name, 'Smartphones')
        self.assertEqual(category.slug, 'smartphones')
        self.assertTrue(category.is_active)
    
    def test_category_str(self):
        """Test category string representation"""
        category = Category.objects.create(name='Laptops')
        self.assertEqual(str(category), 'Laptops')


class SubcategoryModelTest(TestCase):
    """Test Subcategory model"""
    
    def setUp(self):
        """Set up test data"""
        self.department = Department.objects.create(name='Electronics')
        self.category = Category.objects.create(name='Smartphones')
        self.category.departments.add(self.department)
    
    def test_subcategory_creation(self):
        """Test creating a subcategory"""
        subcat = Subcategory.objects.create(
            name='iPhone',
            description='Apple iPhones'
        )
        subcat.categories.add(self.category)
        self.assertEqual(subcat.name, 'iPhone')
        self.assertEqual(subcat.slug, 'iphone')
        self.assertTrue(subcat.is_active)
    
    def test_subcategory_get_departments(self):
        """Test getting departments through categories"""
        subcat = Subcategory.objects.create(name='Android Phones')
        subcat.categories.add(self.category)
        departments = subcat.get_departments()
        self.assertIn(self.department, departments)


class ProductModelTest(TestCase):
    """Test Product model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testvendor',
            email='test@example.com',
            password='testpass123'
        )
        self.department = Department.objects.create(name='Electronics')
        self.category = Category.objects.create(name='Smartphones')
        self.category.departments.add(self.department)
        self.subcategory = Subcategory.objects.create(name='iPhone')
        self.subcategory.categories.add(self.category)
    
    def test_product_creation(self):
        """Test creating a product"""
        product = Product.objects.create(
            name='iPhone 14 Pro',
            description='Latest iPhone model',
            price=Decimal('999.99'),
            vendor=self.user,
            primary_category=self.category,
            stock=10,
            approval_status=Product.APPROVAL_STATUS_APPROVED  # Set to approved so is_active becomes True
        )
        product.subcategories.add(self.subcategory)
        self.assertEqual(product.name, 'iPhone 14 Pro')
        self.assertEqual(product.price, Decimal('999.99'))
        self.assertEqual(product.vendor, self.user)
        self.assertTrue(product.is_active)
        self.assertEqual(product.stock, 10)
    
    def test_product_slug_generation(self):
        """Test product slug is generated from name"""
        product = Product.objects.create(
            name='Samsung Galaxy S23',
            description='Android phone',
            price=Decimal('799.99'),
            vendor=self.user,
            primary_category=self.category,
            stock=5
        )
        self.assertTrue(product.slug)
        self.assertIn('samsung', product.slug.lower())
    
    def test_product_str(self):
        """Test product string representation"""
        product = Product.objects.create(
            name='Test Product',
            description='Test',
            price=Decimal('100.00'),
            vendor=self.user,
            primary_category=self.category,
            stock=1
        )
        self.assertEqual(str(product), 'Test Product')
    
    def test_product_in_stock(self):
        """Test product stock availability"""
        product = Product.objects.create(
            name='Product with Stock',
            description='Test',
            price=Decimal('50.00'),
            vendor=self.user,
            primary_category=self.category,
            stock=5
        )
        self.assertTrue(product.stock > 0)
        
        product.stock = 0
        product.save()
        self.assertEqual(product.stock, 0)


class ProductAPITest(TestCase):
    """Test Product API endpoints"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testvendor',
            email='test@example.com',
            password='testpass123'
        )
        self.department = Department.objects.create(name='Electronics')
        self.category = Category.objects.create(name='Smartphones')
        self.category.departments.add(self.department)
    
    def test_product_list_endpoint(self):
        """Test getting product list"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
    
    def test_department_list_endpoint(self):
        """Test getting department list"""
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, 200)
    
    def test_category_list_endpoint(self):
        """Test getting category list"""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
    
    def test_product_list_contains_departments(self):
        """Test that department list returns departments"""
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, 200)
        # Should be JSON response
        self.assertEqual(response['Content-Type'], 'application/json')


class ProductImageTest(TestCase):
    """Test ProductImage model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testvendor',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test',
            price=Decimal('100.00'),
            vendor=self.user,
            primary_category=self.category,
            stock=10
        )
    
    def test_product_image_creation(self):
        """Test creating a product image"""
        image = ProductImage.objects.create(
            product=self.product,
            alt_text='Product image',
            sort_order=1
        )
        self.assertEqual(image.product, self.product)
        self.assertEqual(image.alt_text, 'Product image')
        self.assertEqual(image.sort_order, 1)

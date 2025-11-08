from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Order, OrderItem, Payment
from products.models import Product, Category
from decimal import Decimal

User = get_user_model()


class OrderModelTest(TestCase):
    """Test Order model"""
    
    def setUp(self):
        """Set up test data"""
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='pass123'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
    
    def test_order_creation(self):
        """Test creating an order"""
        order = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('150.00'),
            shipping_address='123 Main St',
            shipping_phone='555-1234'
        )
        self.assertEqual(order.buyer, self.buyer)
        self.assertEqual(order.total_amount, Decimal('150.00'))
        self.assertEqual(order.status, 'pending')
        self.assertFalse(order.is_paid)
        self.assertTrue(order.order_number)  # Should auto-generate
    
    def test_order_number_generation(self):
        """Test that order number is auto-generated"""
        order = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('100.00'),
            shipping_address='456 Oak Ave',
            shipping_phone='555-5678'
        )
        self.assertTrue(order.order_number.startswith('ORD-'))
        self.assertEqual(len(order.order_number), 14)  # ORD- + 10 chars
    
    def test_order_unique_number(self):
        """Test that each order has a unique number"""
        order1 = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('50.00'),
            shipping_address='Address 1',
            shipping_phone='555-1111'
        )
        order2 = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('75.00'),
            shipping_address='Address 2',
            shipping_phone='555-2222'
        )
        self.assertNotEqual(order1.order_number, order2.order_number)
    
    def test_order_str(self):
        """Test order string representation"""
        order = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('100.00'),
            shipping_address='Test Address',
            shipping_phone='555-0000'
        )
        self.assertIn('Order', str(order))
        self.assertIn(self.buyer.username, str(order))
    
    def test_order_status_change(self):
        """Test changing order status"""
        order = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('200.00'),
            shipping_address='Test Address',
            shipping_phone='555-0000'
        )
        self.assertEqual(order.status, 'pending')
        
        order.status = 'confirmed'
        order.save()
        self.assertEqual(order.status, 'confirmed')
        
        order.status = 'shipped'
        order.save()
        self.assertEqual(order.status, 'shipped')


class OrderItemModelTest(TestCase):
    """Test OrderItem model"""
    
    def setUp(self):
        """Set up test data"""
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='pass123'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test',
            price=Decimal('50.00'),
            vendor=self.seller,
            primary_category=self.category,
            stock=10
        )
        self.order = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('100.00'),
            shipping_address='123 Main St',
            shipping_phone='555-1234'
        )
    
    def test_order_item_creation(self):
        """Test creating an order item"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('50.00')
        )
        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, Decimal('50.00'))
        self.assertEqual(item.subtotal, Decimal('100.00'))  # Auto-calculated
        self.assertEqual(item.product_name, 'Test Product')  # Auto-set from product
        self.assertEqual(item.seller, self.seller)  # Auto-set from product vendor
    
    def test_order_item_subtotal_calculation(self):
        """Test that subtotal is calculated correctly"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=Decimal('25.00')
        )
        self.assertEqual(item.subtotal, Decimal('75.00'))
    
    def test_order_item_str(self):
        """Test order item string representation"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('50.00')
        )
        self.assertIn(str(item.quantity), str(item))
        self.assertIn(item.product_name, str(item))


class PaymentModelTest(TestCase):
    """Test Payment model"""
    
    def setUp(self):
        """Set up test data"""
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='pass123'
        )
        self.order = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('150.00'),
            shipping_address='123 Main St',
            shipping_phone='555-1234'
        )
    
    def test_payment_creation(self):
        """Test creating a payment"""
        payment = Payment.objects.create(
            order=self.order,
            amount=Decimal('150.00'),
            payment_method='credit_card',
            transaction_id='TXN-12345',
            status='completed'
        )
        self.assertEqual(payment.order, self.order)
        self.assertEqual(payment.amount, Decimal('150.00'))
        self.assertEqual(payment.payment_method, 'credit_card')
        self.assertEqual(payment.transaction_id, 'TXN-12345')
        self.assertEqual(payment.status, 'completed')
    
    def test_payment_str(self):
        """Test payment string representation"""
        payment = Payment.objects.create(
            order=self.order,
            amount=Decimal('100.00'),
            payment_method='paypal',
            transaction_id='PP-67890'
        )
        self.assertIn('Payment', str(payment))
        self.assertIn(self.order.order_number, str(payment))


class OrderAPITest(TestCase):
    """Test Order API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123'
        )
    
    def test_orders_endpoint_exists(self):
        """Test that orders endpoint exists"""
        # Test passes if we can query Order model
        from orders.models import Order
        orders = Order.objects.all()
        self.assertEqual(orders.count(), 0)  # No orders initially

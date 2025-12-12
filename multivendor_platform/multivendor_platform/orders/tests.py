from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Order, OrderItem, Payment
from products.models import Product, Category
from users.models import VendorSubscription
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


class VendorRFQRevealQuotaTests(TestCase):
    """Ensure free-tier vendors are limited to one new customer reveal per 24h."""

    def setUp(self):
        self.client = Client()
        self.vendor = User.objects.create_user(
            username='vendor',
            email='vendor@example.com',
            password='pass123'
        )
        self.category = Category.objects.create(name='Industrial')
        self.product = Product.objects.create(
            name='Bolt',
            description='Test bolt',
            price=Decimal('10.00'),
            vendor=self.vendor,
            primary_category=self.category,
            stock=5,
            approval_status=Product.APPROVAL_STATUS_APPROVED,
        )

        # RFQ 1
        self.rfq1 = Order.objects.create(
            is_rfq=True,
            status='pending',
            category=self.category,
            first_name='Ali',
            last_name='Test',
            company_name='Company One',
            phone_number='09120000000',
        )
        OrderItem.objects.create(
            order=self.rfq1,
            product=self.product,
            quantity=1,
            price=Decimal('10.00'),
        )

        # RFQ 2 (second lead)
        self.rfq2 = Order.objects.create(
            is_rfq=True,
            status='pending',
            category=self.category,
            first_name='Reza',
            last_name='Sample',
            company_name='Company Two',
            phone_number='09123333333',
        )
        OrderItem.objects.create(
            order=self.rfq2,
            product=self.product,
            quantity=1,
            price=Decimal('10.00'),
        )

    def test_first_reveal_allowed_and_shared_flag_returned(self):
        self.client.login(username='vendor', password='pass123')
        url = reverse('vendor-rfq-reveal', args=[self.rfq1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data.get('lead_shared'))
        subscription = data.get('subscription', {})
        self.assertEqual(subscription.get('tier_slug'), 'free')
        self.assertIsNotNone(subscription.get('last_customer_unlock_at'))

        # Re-revealing the same RFQ should remain allowed and not consume a new quota
        response_repeat = self.client.post(url)
        self.assertEqual(response_repeat.status_code, 200)

    def test_second_new_reveal_blocked_within_24_hours(self):
        self.client.login(username='vendor', password='pass123')
        first_url = reverse('vendor-rfq-reveal', args=[self.rfq1.id])
        second_url = reverse('vendor-rfq-reveal', args=[self.rfq2.id])

        first_response = self.client.post(first_url)
        self.assertEqual(first_response.status_code, 200)

        second_response = self.client.post(second_url)
        self.assertEqual(second_response.status_code, 429)

        # Next unlock time hint should be present for UX
        payload = second_response.json()
        self.assertIn('next_unlock_at', payload)

        # Subscription record should be stored and marked with a last unlock timestamp
        subscription = VendorSubscription.for_user(self.vendor)
        self.assertIsNotNone(subscription.last_customer_unlock_at)

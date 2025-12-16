"""
Tests for Payment System
"""
from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import PremiumSubscriptionPayment, PaymentInvoice
from .zibal_service import ZibalService


class PremiumSubscriptionPaymentModelTest(TestCase):
    """Tests for PremiumSubscriptionPayment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_payment(self):
        """Test creating a payment record"""
        payment = PremiumSubscriptionPayment.objects.create(
            user=self.user,
            billing_period='monthly',
            amount=15000000,  # 1.5 million Toman in Rial
            track_id='test123'
        )
        
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.billing_period, 'monthly')
        self.assertEqual(payment.amount, 15000000)
        self.assertEqual(payment.status, 'pending')
    
    def test_get_amount_toman(self):
        """Test converting Rial to Toman"""
        payment = PremiumSubscriptionPayment.objects.create(
            user=self.user,
            billing_period='monthly',
            amount=15000000,
            track_id='test123'
        )
        
        self.assertEqual(payment.get_amount_toman(), 1500000.0)
    
    def test_mark_as_paid(self):
        """Test marking payment as paid"""
        payment = PremiumSubscriptionPayment.objects.create(
            user=self.user,
            billing_period='monthly',
            amount=15000000,
            track_id='test123'
        )
        
        payment.mark_as_paid(ref_number='REF123', card_number='6037-****-****-1234')
        
        self.assertEqual(payment.status, 'paid')
        self.assertEqual(payment.ref_number, 'REF123')
        self.assertEqual(payment.card_number, '6037-****-****-1234')
        self.assertIsNotNone(payment.paid_at)
    
    def test_get_subscription_duration_days(self):
        """Test getting subscription duration"""
        payment = PremiumSubscriptionPayment.objects.create(
            user=self.user,
            billing_period='monthly',
            amount=15000000,
            track_id='test123'
        )
        
        self.assertEqual(payment.get_subscription_duration_days(), 30)
        
        payment.billing_period = 'yearly'
        payment.save()
        self.assertEqual(payment.get_subscription_duration_days(), 365)


class PaymentInvoiceModelTest(TestCase):
    """Tests for PaymentInvoice model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.payment = PremiumSubscriptionPayment.objects.create(
            user=self.user,
            billing_period='monthly',
            amount=15000000,
            track_id='test123'
        )
    
    def test_create_invoice(self):
        """Test creating an invoice"""
        invoice = PaymentInvoice.objects.create(
            payment=self.payment,
            subtotal=15000000,
            tax_amount=1350000,
            total_amount=16350000
        )
        
        self.assertEqual(invoice.payment, self.payment)
        self.assertIsNotNone(invoice.invoice_number)
        self.assertEqual(invoice.subtotal, 15000000)
    
    def test_auto_generate_invoice_number(self):
        """Test automatic invoice number generation"""
        invoice = PaymentInvoice.objects.create(
            payment=self.payment,
            subtotal=15000000,
            tax_amount=0,
            total_amount=15000000
        )
        
        self.assertTrue(invoice.invoice_number.startswith('INV-'))


class ZibalServiceTest(TestCase):
    """Tests for Zibal Service (mocked)"""
    
    def test_get_payment_url(self):
        """Test getting payment URL"""
        service = ZibalService()
        track_id = '12345'
        url = service.get_payment_url(track_id)
        
        self.assertEqual(url, f'https://gateway.zibal.ir/start/{track_id}')
    
    def test_get_result_message(self):
        """Test getting result message"""
        service = ZibalService()
        
        message = service.get_result_message(100)
        self.assertEqual(message, 'با موفقیت تایید شد')
        
        message = service.get_result_message(102)
        self.assertEqual(message, 'merchant یافت نشد')
    
    def test_is_successful_payment(self):
        """Test checking successful payment status"""
        service = ZibalService()
        
        self.assertTrue(service.is_successful_payment(1))
        self.assertTrue(service.is_successful_payment(2))
        self.assertFalse(service.is_successful_payment(3))
        self.assertFalse(service.is_successful_payment(-1))


# TODO: Add integration tests for API endpoints
# TODO: Add tests for payment callbacks
# TODO: Add tests for invoice generation
# TODO: Add tests for subscription activation


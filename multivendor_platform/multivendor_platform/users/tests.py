from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import UserProfile, BuyerProfile, VendorProfile, Supplier, SellerAd

User = get_user_model()


class UserModelTest(TestCase):
    """Test User model"""
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin.username, 'admin')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_user_str(self):
        """Test user string representation"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass'
        )
        self.assertEqual(str(user), 'testuser')


class UserProfileTest(TestCase):
    """Test UserProfile model"""
    
    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            role='buyer',
            phone='1234567890'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.role, 'buyer')
        self.assertEqual(profile.phone, '1234567890')
        self.assertFalse(profile.is_verified)
        self.assertFalse(profile.is_blocked)
    
    def test_user_profile_is_seller(self):
        """Test is_seller method"""
        profile = UserProfile.objects.create(user=self.user, role='seller')
        self.assertTrue(profile.is_seller())
        self.assertFalse(profile.is_buyer())
    
    def test_user_profile_is_buyer(self):
        """Test is_buyer method"""
        profile = UserProfile.objects.create(user=self.user, role='buyer')
        self.assertTrue(profile.is_buyer())
        self.assertFalse(profile.is_seller())
    
    def test_user_profile_both_roles(self):
        """Test user with both roles"""
        profile = UserProfile.objects.create(user=self.user, role='both')
        self.assertTrue(profile.is_seller())
        self.assertTrue(profile.is_buyer())
    
    def test_user_profile_str(self):
        """Test user profile string representation"""
        profile = UserProfile.objects.create(user=self.user, role='buyer')
        self.assertIn(self.user.username, str(profile))


class BuyerProfileTest(TestCase):
    """Test BuyerProfile model"""
    
    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='pass123'
        )
    
    def test_buyer_profile_creation(self):
        """Test creating a buyer profile"""
        buyer = BuyerProfile.objects.create(
            user=self.user,
            shipping_address='123 Main St',
            billing_address='123 Main St'
        )
        self.assertEqual(buyer.user, self.user)
        self.assertEqual(buyer.shipping_address, '123 Main St')
    
    def test_buyer_profile_str(self):
        """Test buyer profile string representation"""
        buyer = BuyerProfile.objects.create(user=self.user)
        self.assertIn('Buyer', str(buyer))
        self.assertIn(self.user.username, str(buyer))


class VendorProfileTest(TestCase):
    """Test VendorProfile model"""
    
    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username='vendor',
            email='vendor@example.com',
            password='pass123'
        )
    
    def test_vendor_profile_creation(self):
        """Test creating a vendor profile"""
        vendor = VendorProfile.objects.create(
            user=self.user,
            store_name='Test Store',
            description='A test store',
            contact_email='store@example.com'
        )
        self.assertEqual(vendor.user, self.user)
        self.assertEqual(vendor.store_name, 'Test Store')
        self.assertFalse(vendor.is_approved)
    
    def test_vendor_profile_str(self):
        """Test vendor profile string representation"""
        vendor = VendorProfile.objects.create(
            user=self.user,
            store_name='My Store'
        )
        self.assertEqual(str(vendor), 'My Store')
    
    def test_vendor_get_product_count(self):
        """Test getting vendor product count"""
        vendor = VendorProfile.objects.create(
            user=self.user,
            store_name='Test Store'
        )
        # Initially should be 0
        self.assertEqual(vendor.get_product_count(), 0)
    
    def test_vendor_approval(self):
        """Test vendor approval status"""
        vendor = VendorProfile.objects.create(
            user=self.user,
            store_name='Test Store',
            is_approved=False
        )
        self.assertFalse(vendor.is_approved)
        
        vendor.is_approved = True
        vendor.save()
        self.assertTrue(vendor.is_approved)


class SupplierTest(TestCase):
    """Test Supplier model"""
    
    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='pass123'
        )
    
    def test_supplier_creation(self):
        """Test creating a supplier"""
        supplier = Supplier.objects.create(
            vendor=self.user,
            name='ABC Company',
            website='https://abc.com',
            phone='555-1234',
            email='info@abc.com'
        )
        self.assertEqual(supplier.name, 'ABC Company')
        self.assertEqual(supplier.vendor, self.user)
        self.assertTrue(supplier.is_active)
    
    def test_supplier_str(self):
        """Test supplier string representation"""
        supplier = Supplier.objects.create(
            vendor=self.user,
            name='XYZ Corp'
        )
        self.assertEqual(str(supplier), 'XYZ Corp')
    
    def test_supplier_get_product_count(self):
        """Test getting supplier product count"""
        supplier = Supplier.objects.create(
            vendor=self.user,
            name='Test Supplier'
        )
        self.assertEqual(supplier.get_product_count(), 0)


class SellerAdTest(TestCase):
    """Test SellerAd model"""
    
    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
    
    def test_seller_ad_creation(self):
        """Test creating a seller advertisement"""
        ad = SellerAd.objects.create(
            seller=self.user,
            title='Special Offer',
            description='Limited time offer on products',
            contact_info='Call 555-1234'
        )
        self.assertEqual(ad.seller, self.user)
        self.assertEqual(ad.title, 'Special Offer')
        self.assertTrue(ad.is_active)
    
    def test_seller_ad_str(self):
        """Test seller ad string representation"""
        ad = SellerAd.objects.create(
            seller=self.user,
            title='New Products',
            description='Check out our new products',
            contact_info='email@example.com'
        )
        self.assertEqual(str(ad), 'New Products')


class AuthAPITest(TestCase):
    """Test Authentication API"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_register_endpoint_exists(self):
        """Test that register endpoint exists"""
        response = self.client.get('/api/auth/register/')
        # Should return 405 (Method Not Allowed) for GET or 200, meaning endpoint exists
        self.assertIn(response.status_code, [200, 405])
    
    def test_login_endpoint_exists(self):
        """Test that login endpoint exists"""
        response = self.client.post('/api/auth/login/', {})
        # Should return 400 or 401 (bad credentials) not 404
        self.assertNotEqual(response.status_code, 404)

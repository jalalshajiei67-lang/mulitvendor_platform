from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from products.models import Category
from .models import ReverseAuction, AuctionInvitation, Bid
from .services import AuctionService


class ReverseAuctionTestCase(TestCase):
    """Test cases for reverse auction functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.buyer = User.objects.create_user(
            username='buyer1',
            email='buyer1@test.com',
            password='testpass123'
        )
        self.supplier1 = User.objects.create_user(
            username='supplier1',
            email='supplier1@test.com',
            password='testpass123'
        )
        self.supplier2 = User.objects.create_user(
            username='supplier2',
            email='supplier2@test.com',
            password='testpass123'
        )
        
        # Create category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        # Create auction
        self.auction = ReverseAuction.objects.create(
            buyer=self.buyer,
            title='Test Auction',
            description='Test Description',
            category=self.category,
            starting_price=1000000,  # 1 million
            minimum_decrement=50000,  # 50k
            deadline=timezone.now() + timedelta(days=3),
            status='active'
        )
    
    def test_auction_creation(self):
        """Test auction creation"""
        self.assertEqual(self.auction.status, 'active')
        self.assertEqual(self.auction.buyer, self.buyer)
        self.assertTrue(self.auction.is_active())
    
    def test_auto_invite_suppliers(self):
        """Test automatic supplier invitation"""
        # This would require products to be created with the category
        # For now, just test the method exists
        invited = AuctionService.auto_invite_suppliers(self.auction)
        self.assertIsInstance(invited, list)
    
    def test_bid_validation(self):
        """Test bid validation"""
        # Create invitation
        invitation = AuctionInvitation.objects.create(
            auction=self.auction,
            supplier=self.supplier1
        )
        
        # Test valid bid
        is_valid, error = AuctionService.validate_bid(
            self.auction,
            self.supplier1,
            900000  # Less than starting price
        )
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        # Test invalid bid (too high)
        is_valid, error = AuctionService.validate_bid(
            self.auction,
            self.supplier1,
            1100000  # More than starting price
        )
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_bid_ranking(self):
        """Test bid ranking calculation"""
        # Create invitations
        AuctionInvitation.objects.create(
            auction=self.auction,
            supplier=self.supplier1
        )
        AuctionInvitation.objects.create(
            auction=self.auction,
            supplier=self.supplier2
        )
        
        # Create bids
        bid1 = Bid.objects.create(
            auction=self.auction,
            supplier=self.supplier1,
            amount=800000
        )
        bid2 = Bid.objects.create(
            auction=self.auction,
            supplier=self.supplier2,
            amount=750000
        )
        
        # Calculate ranks
        AuctionService.calculate_all_ranks(self.auction)
        
        # Refresh from DB
        bid1.refresh_from_db()
        bid2.refresh_from_db()
        
        # bid2 should be rank 1 (lowest)
        self.assertEqual(bid2.rank, 1)
        self.assertTrue(bid2.is_winning)
        # bid1 should be rank 2
        self.assertEqual(bid1.rank, 2)
        self.assertFalse(bid1.is_winning)
    
    def test_soft_close_extension(self):
        """Test soft close deadline extension"""
        # Set deadline to 4 minutes from now
        self.auction.deadline = timezone.now() + timedelta(minutes=4)
        self.auction.save()
        
        # Should extend
        self.assertTrue(self.auction.should_extend())
        
        # Extend deadline
        extended = self.auction.extend_deadline()
        self.assertTrue(extended)
        self.assertEqual(self.auction.extended_count, 1)
        
        # Should not extend more than 3 times
        self.auction.extended_count = 3
        self.auction.save()
        self.assertFalse(self.auction.should_extend())


from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone

from users.models import UserProfile, VendorProfile
from .models import Invitation, SupplierEngagement, PointsHistory
from .services import GamificationService


class InvitationModelTest(TestCase):
    """Test Invitation model"""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='09123456789',
            email='user1@test.com',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='09123456780',
            email='user2@test.com',
            first_name='User',
            last_name='Two'
        )
        self.profile1 = UserProfile.objects.create(
            user=self.user1,
            role='seller'
        )
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            role='seller'
        )
        self.vendor1 = VendorProfile.objects.get(user=self.user1)
        self.vendor2 = VendorProfile.objects.get(user=self.user2)

    def test_create_invitation(self):
        """Test creating an invitation"""
        invitation = Invitation.objects.create(
            inviter=self.vendor1,
            invite_code='TEST123',
            status='pending'
        )
        self.assertEqual(invitation.inviter, self.vendor1)
        self.assertEqual(invitation.invite_code, 'TEST123')
        self.assertEqual(invitation.status, 'pending')
        self.assertIsNone(invitation.invitee)

    def test_invitation_unique_code(self):
        """Test that invite codes must be unique"""
        Invitation.objects.create(
            inviter=self.vendor1,
            invite_code='UNIQUE123',
            status='pending'
        )
        # Try to create another with same code
        with self.assertRaises(Exception):
            Invitation.objects.create(
                inviter=self.vendor2,
                invite_code='UNIQUE123',
                status='pending'
            )


class InvitationAPITest(TestCase):
    """Test invitation API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='09123456789',
            email='user@test.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            role='seller'
        )
        self.vendor = VendorProfile.objects.get(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_generate_invite_code(self):
        """Test generating an invite code"""
        response = self.client.post('/api/gamification/invite/generate/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('invite_code', response.data)
        self.assertIn('invite_link', response.data)
        self.assertIsNotNone(response.data['invite_code'])
        self.assertIsNotNone(response.data['invite_link'])

        # Verify invitation was created
        invitation = Invitation.objects.get(invite_code=response.data['invite_code'])
        self.assertEqual(invitation.inviter, self.vendor)
        self.assertEqual(invitation.status, 'pending')

    def test_generate_invite_code_unique(self):
        """Test that generated codes are unique"""
        codes = set()
        for _ in range(10):
            response = self.client.post('/api/gamification/invite/generate/')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            code = response.data['invite_code']
            self.assertNotIn(code, codes, "Generated duplicate invite code")
            codes.add(code)

    def test_get_invitation_status(self):
        """Test getting invitation status"""
        # Create some invitations
        Invitation.objects.create(
            inviter=self.vendor,
            invite_code='CODE1',
            status='pending'
        )
        Invitation.objects.create(
            inviter=self.vendor,
            invite_code='CODE2',
            status='accepted',
            accepted_at=timezone.now()
        )

        response = self.client.get('/api/gamification/invite/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('invitations', response.data)
        self.assertEqual(len(response.data['invitations']), 2)
        self.assertEqual(response.data['total_invitations'], 2)
        self.assertEqual(response.data['accepted_count'], 1)
        self.assertEqual(response.data['pending_count'], 1)

    def test_invitation_status_requires_auth(self):
        """Test that invitation endpoints require authentication"""
        self.client.logout()
        response = self.client.post('/api/gamification/invite/generate/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get('/api/gamification/invite/status/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InvitationRegistrationTest(TestCase):
    """Test invitation handling during registration"""

    def setUp(self):
        self.client = APIClient()
        # Create inviter
        self.inviter_user = User.objects.create_user(
            username='09123456789',
            email='inviter@test.com',
            first_name='Inviter',
            last_name='User',
            password='testpass123'
        )
        self.inviter_profile = UserProfile.objects.create(
            user=self.inviter_user,
            role='seller'
        )
        self.inviter_vendor = VendorProfile.objects.get(user=self.inviter_user)
        # Create engagement for inviter
        SupplierEngagement.objects.create(
            vendor_profile=self.inviter_vendor,
            total_points=100
        )

    def test_registration_with_referral_code(self):
        """Test registration with valid referral code"""
        # Create invitation
        invitation = Invitation.objects.create(
            inviter=self.inviter_vendor,
            invite_code='REF123',
            status='pending'
        )

        # Register new user with referral code
        response = self.client.post('/api/users/register/', {
            'username': '09123456780',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'seller',
            'referral_code': 'REF123'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify invitation was accepted
        invitation.refresh_from_db()
        self.assertEqual(invitation.status, 'accepted')
        self.assertIsNotNone(invitation.accepted_at)

        # Verify points were awarded to inviter
        engagement = SupplierEngagement.objects.get(vendor_profile=self.inviter_vendor)
        self.assertEqual(engagement.total_points, 200)  # 100 initial + 100 from invitation

        # Verify points history was created
        points_history = PointsHistory.objects.filter(
            vendor_profile=self.inviter_vendor,
            reason='peer_invitation'
        ).first()
        self.assertIsNotNone(points_history)
        self.assertEqual(points_history.points, 100)

    def test_registration_with_invalid_referral_code(self):
        """Test registration with invalid referral code doesn't fail"""
        response = self.client.post('/api/users/register/', {
            'username': '09123456780',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'seller',
            'referral_code': 'INVALID123'
        })

        # Registration should still succeed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # No points should be awarded
        engagement = SupplierEngagement.objects.get(vendor_profile=self.inviter_vendor)
        self.assertEqual(engagement.total_points, 100)

    def test_registration_with_already_accepted_code(self):
        """Test that already accepted codes don't award points again"""
        # Create and accept invitation
        invitation = Invitation.objects.create(
            inviter=self.inviter_vendor,
            invite_code='REF456',
            status='accepted',
            accepted_at=timezone.now()
        )

        initial_points = SupplierEngagement.objects.get(
            vendor_profile=self.inviter_vendor
        ).total_points

        # Try to register with already accepted code
        response = self.client.post('/api/users/register/', {
            'username': '09123456780',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'seller',
            'referral_code': 'REF456'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Points should not be awarded again
        engagement = SupplierEngagement.objects.get(vendor_profile=self.inviter_vendor)
        self.assertEqual(engagement.total_points, initial_points)

    def test_registration_without_referral_code(self):
        """Test normal registration without referral code"""
        response = self.client.post('/api/users/register/', {
            'username': '09123456780',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'seller'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Should work fine without referral code
        self.assertIn('token', response.data)


class InvitationPointsTest(TestCase):
    """Test points awarding for invitations"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='09123456789',
            email='user@test.com',
            first_name='Test',
            last_name='User'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            role='seller'
        )
        self.vendor = VendorProfile.objects.get(user=self.user)
        self.engagement = SupplierEngagement.objects.create(
            vendor_profile=self.vendor,
            total_points=50
        )

    def test_points_awarded_on_invitation_acceptance(self):
        """Test that 100 points are awarded when invitation is accepted"""
        invitation = Invitation.objects.create(
            inviter=self.vendor,
            invite_code='TEST123',
            status='pending'
        )

        # Simulate invitation acceptance
        from gamification.services import GamificationService
        service = GamificationService(self.vendor)
        service.add_points('peer_invitation', 100, metadata={
            'invitation_id': invitation.id
        })

        # Verify points were added
        self.engagement.refresh_from_db()
        self.assertEqual(self.engagement.total_points, 150)

        # Verify points history
        history = PointsHistory.objects.filter(
            vendor_profile=self.vendor,
            reason='peer_invitation'
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.points, 100)
        self.assertEqual(history.metadata.get('invitation_id'), invitation.id)


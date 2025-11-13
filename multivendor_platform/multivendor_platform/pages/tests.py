from django.test import TestCase
from .models import AboutPage, ContactPage


class AboutPageTestCase(TestCase):
    """Test cases for About Us page"""
    
    def setUp(self):
        """Set up test data"""
        self.about_page = AboutPage.objects.create(
            title_fa='درباره ما',
            content_fa='<p>این متن درباره ما است</p>',
            title_en='About Us',
            content_en='<p>This is about us content</p>',
            meta_title_fa='درباره ما - سایت ما',
            meta_description_fa='صفحه درباره ما',
            meta_keywords_fa='درباره ما, تیم ما',
        )
    
    def test_about_page_creation(self):
        """Test that About Us page is created successfully"""
        self.assertEqual(AboutPage.objects.count(), 1)
        self.assertEqual(self.about_page.title_fa, 'درباره ما')
    
    def test_only_one_instance_allowed(self):
        """Test that only one About Us page instance can exist"""
        # Try to create a second instance
        new_page = AboutPage.objects.create(
            title_fa='درباره ما جدید',
            content_fa='<p>محتوای جدید</p>',
        )
        # Should update the existing instance
        self.assertEqual(AboutPage.objects.count(), 1)
        self.assertEqual(AboutPage.objects.first().title_fa, 'درباره ما جدید')


class ContactPageTestCase(TestCase):
    """Test cases for Contact Us page"""
    
    def setUp(self):
        """Set up test data"""
        self.contact_page = ContactPage.objects.create(
            title_fa='تماس با ما',
            content_fa='<p>این متن تماس با ما است</p>',
            address_fa='تهران، خیابان ولیعصر',
            phone='021-12345678',
            email='info@example.com',
            working_hours_fa='شنبه تا چهارشنبه 9 الی 17',
            title_en='Contact Us',
            content_en='<p>This is contact us content</p>',
            address_en='Tehran, Vali Asr Street',
            working_hours_en='Saturday to Wednesday 9 AM to 5 PM',
            meta_title_fa='تماس با ما - سایت ما',
            meta_description_fa='صفحه تماس با ما',
            meta_keywords_fa='تماس, آدرس',
        )
    
    def test_contact_page_creation(self):
        """Test that Contact Us page is created successfully"""
        self.assertEqual(ContactPage.objects.count(), 1)
        self.assertEqual(self.contact_page.title_fa, 'تماس با ما')
        self.assertEqual(self.contact_page.phone, '021-12345678')
    
    def test_only_one_instance_allowed(self):
        """Test that only one Contact Us page instance can exist"""
        # Try to create a second instance
        new_page = ContactPage.objects.create(
            title_fa='تماس با ما جدید',
            content_fa='<p>محتوای جدید</p>',
        )
        # Should update the existing instance
        self.assertEqual(ContactPage.objects.count(), 1)
        self.assertEqual(ContactPage.objects.first().title_fa, 'تماس با ما جدید')


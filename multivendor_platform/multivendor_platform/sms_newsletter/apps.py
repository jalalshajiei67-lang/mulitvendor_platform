from django.apps import AppConfig


class SmsNewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms_newsletter'
    verbose_name = 'خبرنامه پیامکی فروشندگان'

    def ready(self):
        """Import admin to ensure registration"""
        try:
            import sms_newsletter.admin  # noqa: F401
        except ImportError:
            pass


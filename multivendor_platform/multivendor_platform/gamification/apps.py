from django.apps import AppConfig


class GamificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gamification'
    verbose_name = 'Supplier Gamification'

    def ready(self):
        # Import signal handlers
        from . import signals  # noqa: F401

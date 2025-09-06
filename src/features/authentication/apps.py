# Authentication app configuration
# Decision: Follow Django app configuration pattern for feature modules

from django.apps import AppConfig
from django.conf import settings

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'features.authentication'
    verbose_name = 'Authentication'

    def ready(self):
        # Import signals when app is ready
        # Decision: Lazy import to avoid circular imports
        if self.is_enabled():
            from . import signals

    def is_enabled(self):
        """Check if authentication feature is enabled"""
        return settings.ENABLED_FEATURES.get('authentication', False)
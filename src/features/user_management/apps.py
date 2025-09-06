# User management app configuration

from django.apps import AppConfig
from django.conf import settings

class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'features.user_management'
    verbose_name = 'User Management'

    def is_enabled(self):
        """Check if user management feature is enabled"""
        return settings.ENABLED_FEATURES.get('user_management', False)
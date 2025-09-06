# Authentication signals
# Decision: Use Django signals for loose coupling between features

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create user profile when user is created
    
    Design Decision: Only create profile if profile_management feature is enabled
    """
    from django.conf import settings
    
    if created and settings.ENABLED_FEATURES.get('profile_management', False):
        try:
            from features.user_management.models import UserProfile
            UserProfile.objects.get_or_create(user=instance)
        except ImportError:
            # Profile feature not available
            pass
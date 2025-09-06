# User management models
# Decision: Keep user management models separate from auth models for modularity

from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    """
    Extended user profile information
    
    Design Decision: Separate profile model using OneToOne relationship
    - Keeps core User model lightweight
    - Allows for feature toggling
    - Easier to extend with additional fields
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    # Privacy settings
    is_public = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email}"

    class Meta:
        db_table = 'user_profiles'
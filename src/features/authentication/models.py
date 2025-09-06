# Authentication models for VLE User Management System
# Decision: Custom user model with email as username for better UX
# Following Django best practices for user authentication

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model with additional fields
    
    Design Decision: Use email as username instead of traditional username
    - Improves user experience (users remember emails better)
    - Aligns with modern authentication patterns
    - Reduces duplicate data entry
    """
    
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'
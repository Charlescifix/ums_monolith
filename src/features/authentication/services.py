# Authentication services for business logic
# Decision: Separate business logic from views for better testability and reusability

from typing import Optional
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .models import User

class AuthenticationService:
    """
    Authentication business logic service
    
    Design Decision: Service layer pattern
    - Encapsulates business rules
    - Makes logic reusable across different interfaces (API, web)
    - Easier to test in isolation
    """

    def register_user(self, email: str, password: str, **extra_fields) -> User:
        """
        Register a new user
        
        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            **extra_fields: Additional user data
            
        Returns:
            Created User instance
        """
        user = User.objects.create_user(
            email=email,
            username=email,  # Use email as username
            password=password,
            **extra_fields
        )
        
        # Send verification email
        self._send_verification_email(user)
        
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user credentials
        
        Args:
            email: User's email
            password: Plain text password
            
        Returns:
            User instance if credentials are valid, None otherwise
        """
        return authenticate(username=email, password=password)

    def send_password_reset(self, email: str) -> bool:
        """
        Send password reset email
        
        Args:
            email: User's email address
            
        Returns:
            True if email was sent successfully
        """
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            # Implementation depends on notification feature
            return True
        except User.DoesNotExist:
            return False

    def _send_verification_email(self, user: User):
        """Send email verification - placeholder for notification feature"""
        # Implementation depends on notification feature
        pass
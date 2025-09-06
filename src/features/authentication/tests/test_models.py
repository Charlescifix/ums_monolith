# Authentication model tests
# Decision: Test models separately for clear separation of concerns

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class UserModelTests(TestCase):
    """
    Test cases for custom User model
    
    Design Decision: Focus on business rules and edge cases
    - Test unique constraints
    - Test model methods
    - Test field validations
    """

    def test_create_user_with_email(self):
        """Test creating user with email as username"""
        user = User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_email_verified)

    def test_create_user_without_email_fails(self):
        """Test that creating user without email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                username='testuser',
                password='testpass123'
            )

    def test_email_uniqueness(self):
        """Test that email must be unique"""
        User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                username='test2@example.com',
                password='testpass123'
            )

    def test_user_string_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        # Should use email for string representation
        self.assertEqual(str(user), 'test@example.com')
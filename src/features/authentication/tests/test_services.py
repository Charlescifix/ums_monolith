# Authentication service tests
# Decision: Test business logic separately from API layer

from django.test import TestCase
from django.contrib.auth import get_user_model
from ..services import AuthenticationService

User = get_user_model()

class AuthenticationServiceTests(TestCase):
    """
    Test authentication business logic
    
    Design Decision: Test service layer in isolation
    - Mock external dependencies when needed
    - Focus on business rule validation
    - Test both success and failure scenarios
    """

    def setUp(self):
        self.service = AuthenticationService()

    def test_register_user_success(self):
        """Test successful user registration"""
        user = self.service.register_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testpass123'))

    def test_authenticate_valid_credentials(self):
        """Test authentication with valid credentials"""
        # Create user first
        User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        # Test authentication
        user = self.service.authenticate_user('test@example.com', 'testpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

    def test_authenticate_invalid_credentials(self):
        """Test authentication with invalid credentials"""
        # Create user first
        User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        # Test with wrong password
        user = self.service.authenticate_user('test@example.com', 'wrongpass')
        self.assertIsNone(user)
        
        # Test with non-existent user
        user = self.service.authenticate_user('nonexistent@example.com', 'testpass123')
        self.assertIsNone(user)

    def test_send_password_reset_existing_user(self):
        """Test password reset for existing user"""
        User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        result = self.service.send_password_reset('test@example.com')
        self.assertTrue(result)

    def test_send_password_reset_nonexistent_user(self):
        """Test password reset for non-existent user returns False"""
        result = self.service.send_password_reset('nonexistent@example.com')
        self.assertFalse(result)
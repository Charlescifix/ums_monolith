# Authentication API tests
# Decision: Test API endpoints with realistic scenarios

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationAPITests(TestCase):
    """
    Test authentication API endpoints
    
    Design Decision: Test complete request/response cycle
    - Test status codes
    - Test response structure
    - Test authentication flows
    """

    def setUp(self):
        self.client = APIClient()

    def test_user_registration_success(self):
        """Test successful user registration via API"""
        data = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = self.client.post('/api/v1/auth/register/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_user_registration_invalid_data(self):
        """Test registration with invalid data"""
        data = {
            'email': 'invalid-email',  # Invalid email format
            'password': '123'  # Too short password
        }
        
        response = self.client.post('/api/v1/auth/register/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_login_success(self):
        """Test successful login"""
        # Create user first
        user = User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/v1/auth/login/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['email'], 'test@example.com')

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        # Create user first
        User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post('/api/v1/auth/login/', data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_password_reset_request(self):
        """Test password reset request always returns success"""
        # Test with existing user
        User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123'
        )
        
        data = {'email': 'test@example.com'}
        response = self.client.post('/api/v1/auth/password-reset/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Test with non-existent user (should still return success for security)
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post('/api/v1/auth/password-reset/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
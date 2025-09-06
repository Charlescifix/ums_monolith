# User management API tests

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserManagementAPITests(TestCase):
    """
    Test user management API endpoints
    
    Design Decision: Test authenticated API access
    - Test authorization requirements
    - Test response formats
    - Test error handling
    """

    def setUp(self):
        self.client = APIClient()
        
        # Create test user for authentication
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin@example.com',
            password='adminpass123'
        )
        
        # Create regular test users
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        # Authenticate admin user
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_user_list_authenticated(self):
        """Test user list endpoint with authentication"""
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('pagination', response.data)
        self.assertEqual(len(response.data['users']), 2)  # admin + user1

    def test_user_list_unauthenticated(self):
        """Test user list endpoint without authentication"""
        client = APIClient()  # New client without credentials
        response = client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_with_search(self):
        """Test user list with search parameter"""
        response = self.client.get('/api/v1/users/?search=john')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 1)
        self.assertEqual(response.data['users'][0]['first_name'], 'John')

    def test_user_list_with_pagination(self):
        """Test user list with pagination parameters"""
        response = self.client.get('/api/v1/users/?page=1&page_size=1')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 1)
        self.assertGreater(response.data['pagination']['page_count'], 1)

    def test_user_detail_success(self):
        """Test user detail endpoint"""
        response = self.client.get(f'/api/v1/users/{self.user1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user1@example.com')
        self.assertEqual(response.data['first_name'], 'John')

    def test_user_detail_not_found(self):
        """Test user detail for non-existent user"""
        response = self.client.get('/api/v1/users/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_user_update_success(self):
        """Test successful user update"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.patch(f'/api/v1/users/{self.user1.id}/update/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'Name')

    def test_user_update_not_found(self):
        """Test updating non-existent user"""
        data = {'first_name': 'Test'}
        
        response = self.client.patch('/api/v1/users/99999/update/', data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_deactivate_success(self):
        """Test successful user deactivation"""
        response = self.client.delete(f'/api/v1/users/{self.user1.id}/deactivate/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify user is deactivated
        user = User.objects.get(id=self.user1.id)
        self.assertFalse(user.is_active)

    def test_user_deactivate_not_found(self):
        """Test deactivating non-existent user"""
        response = self.client.delete('/api/v1/users/99999/deactivate/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bulk_operations_success(self):
        """Test bulk operations endpoint"""
        data = {
            'user_ids': [self.user1.id],
            'operation': 'deactivate'
        }
        
        response = self.client.post('/api/v1/users/bulk/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['affected_users'], 1)

    def test_bulk_operations_invalid_data(self):
        """Test bulk operations with invalid data"""
        data = {
            'user_ids': [],  # Empty list
            'operation': 'invalid_operation'
        }
        
        response = self.client.post('/api/v1/users/bulk/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
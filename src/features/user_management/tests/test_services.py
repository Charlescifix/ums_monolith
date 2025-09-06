# User management service tests

from django.test import TestCase
from django.contrib.auth import get_user_model
from ..services import UserManagementService

User = get_user_model()

class UserManagementServiceTests(TestCase):
    """
    Test user management business logic
    
    Design Decision: Test service methods thoroughly
    - Test pagination logic
    - Test search functionality 
    - Test bulk operations
    """

    def setUp(self):
        self.service = UserManagementService()
        
        # Create test users
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            username='user1@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            username='user2@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith'
        )

    def test_get_user_list_basic(self):
        """Test basic user list retrieval"""
        result = self.service.get_user_list()
        
        self.assertEqual(result['total_count'], 2)
        self.assertEqual(len(result['users']), 2)
        self.assertEqual(result['current_page'], 1)

    def test_get_user_list_with_search(self):
        """Test user list with search functionality"""
        result = self.service.get_user_list(search='john')
        
        self.assertEqual(result['total_count'], 1)
        self.assertEqual(result['users'][0].first_name, 'John')

    def test_get_user_list_pagination(self):
        """Test user list pagination"""
        # Test first page
        result = self.service.get_user_list(page=1, page_size=1)
        
        self.assertEqual(len(result['users']), 1)
        self.assertEqual(result['page_count'], 2)
        self.assertTrue(result['has_next'])
        self.assertFalse(result['has_previous'])

    def test_get_user_by_id_exists(self):
        """Test getting user by existing ID"""
        user = self.service.get_user_by_id(self.user1.id)
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'user1@example.com')

    def test_get_user_by_id_not_exists(self):
        """Test getting user by non-existent ID"""
        user = self.service.get_user_by_id(99999)
        
        self.assertIsNone(user)

    def test_update_user_success(self):
        """Test successful user update"""
        updated_user = self.service.update_user(
            self.user1.id,
            first_name='Updated',
            last_name='Name'
        )
        
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')

    def test_update_user_not_exists(self):
        """Test updating non-existent user"""
        result = self.service.update_user(99999, first_name='Test')
        
        self.assertIsNone(result)

    def test_deactivate_user_success(self):
        """Test successful user deactivation"""
        result = self.service.deactivate_user(self.user1.id)
        
        self.assertTrue(result)
        
        # Verify user is deactivated
        user = User.objects.get(id=self.user1.id)
        self.assertFalse(user.is_active)

    def test_deactivate_user_not_exists(self):
        """Test deactivating non-existent user"""
        result = self.service.deactivate_user(99999)
        
        self.assertFalse(result)

    def test_bulk_deactivate(self):
        """Test bulk user deactivation"""
        result = self.service.bulk_operation(
            user_ids=[self.user1.id, self.user2.id],
            operation='deactivate'
        )
        
        self.assertEqual(result['success_count'], 2)
        self.assertEqual(result['total_requested'], 2)
        
        # Verify both users are deactivated
        user1 = User.objects.get(id=self.user1.id)
        user2 = User.objects.get(id=self.user2.id)
        self.assertFalse(user1.is_active)
        self.assertFalse(user2.is_active)

    def test_bulk_activate(self):
        """Test bulk user activation"""
        # First deactivate users
        self.user1.is_active = False
        self.user1.save()
        
        result = self.service.bulk_operation(
            user_ids=[self.user1.id],
            operation='activate'
        )
        
        self.assertEqual(result['success_count'], 1)
        
        # Verify user is activated
        user = User.objects.get(id=self.user1.id)
        self.assertTrue(user.is_active)
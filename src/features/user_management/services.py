# User management services
# Decision: Service layer for user CRUD operations and business logic

from typing import List, Optional
from django.core.paginator import Paginator
from django.db.models import Q
from features.authentication.models import User
from .models import UserProfile

class UserManagementService:
    """
    User management business logic service
    
    Design Decision: Centralize user management operations
    - Consistent business rules across different interfaces
    - Easy to modify behavior without changing multiple views
    - Better testability
    """

    def get_user_list(self, search: str = None, page: int = 1, page_size: int = 20) -> dict:
        """
        Get paginated list of users with optional search
        
        Args:
            search: Search term for email, first_name, last_name
            page: Page number
            page_size: Items per page
            
        Returns:
            Dictionary with users and pagination info
        """
        queryset = User.objects.select_related('profile').order_by('-date_joined')
        
        # Apply search filter
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        # Paginate results
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        return {
            'users': list(page_obj),
            'total_count': paginator.count,
            'page_count': paginator.num_pages,
            'current_page': page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID with profile"""
        try:
            return User.objects.select_related('profile').get(id=user_id)
        except User.DoesNotExist:
            return None

    def update_user(self, user_id: int, **update_data) -> Optional[User]:
        """
        Update user information
        
        Args:
            user_id: User ID to update
            **update_data: Fields to update
            
        Returns:
            Updated user instance or None if not found
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Update allowed fields
        allowed_fields = ['first_name', 'last_name', 'email', 'is_active']
        for field, value in update_data.items():
            if field in allowed_fields and hasattr(user, field):
                setattr(user, field, value)
        
        user.save()
        return user

    def deactivate_user(self, user_id: int) -> bool:
        """
        Soft delete user by deactivating
        
        Design Decision: Soft delete instead of hard delete
        - Preserves data integrity
        - Allows for account recovery
        - Maintains audit trail
        """
        user = self.get_user_by_id(user_id)
        if user and user.is_active:
            user.is_active = False
            user.save()
            return True
        return False

    def bulk_operation(self, user_ids: List[int], operation: str) -> dict:
        """
        Perform bulk operations on users
        
        Args:
            user_ids: List of user IDs
            operation: Operation type ('deactivate', 'activate')
            
        Returns:
            Dictionary with operation results
        """
        users = User.objects.filter(id__in=user_ids)
        success_count = 0
        
        if operation == 'deactivate':
            success_count = users.update(is_active=False)
        elif operation == 'activate':
            success_count = users.update(is_active=True)
        
        return {
            'success_count': success_count,
            'total_requested': len(user_ids)
        }
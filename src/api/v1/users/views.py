# User management API views

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from features.user_management.services import UserManagementService
from .serializers import (
    UserListSerializer, UserDetailSerializer, 
    UserUpdateSerializer, BulkOperationSerializer
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    """
    Get paginated list of users with search functionality
    
    Design Decision: Function-based view for simple list operation
    - Clear and concise
    - Easy to add custom logic
    """
    service = UserManagementService()
    
    # Get query parameters
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    
    # Get users from service
    result = service.get_user_list(search=search, page=page, page_size=page_size)
    
    # Serialize users
    serializer = UserListSerializer(result['users'], many=True)
    
    return Response({
        'users': serializer.data,
        'pagination': {
            'total_count': result['total_count'],
            'page_count': result['page_count'],
            'current_page': result['current_page'],
            'has_next': result['has_next'],
            'has_previous': result['has_previous']
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    """Get detailed user information"""
    service = UserManagementService()
    user = service.get_user_by_id(user_id)
    
    if not user:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = UserDetailSerializer(user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_update(request, user_id):
    """
    Update user information
    
    Design Decision: Support both PUT and PATCH
    - PUT for complete updates
    - PATCH for partial updates
    """
    service = UserManagementService()
    user = service.get_user_by_id(user_id)
    
    if not user:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        updated_user = service.update_user(user_id, **serializer.validated_data)
        return Response(UserDetailSerializer(updated_user).data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_deactivate(request, user_id):
    """
    Deactivate user (soft delete)
    
    Design Decision: Use soft delete for data preservation
    """
    service = UserManagementService()
    
    if service.deactivate_user(user_id):
        return Response({'message': 'User deactivated successfully'})
    else:
        return Response(
            {'error': 'User not found or already inactive'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_operations(request):
    """
    Perform bulk operations on users
    
    Design Decision: Single endpoint for multiple bulk operations
    - Consistent API pattern
    - Easy to extend with new operations
    """
    serializer = BulkOperationSerializer(data=request.data)
    if serializer.is_valid():
        service = UserManagementService()
        result = service.bulk_operation(
            user_ids=serializer.validated_data['user_ids'],
            operation=serializer.validated_data['operation']
        )
        
        return Response({
            'message': f'Operation completed successfully',
            'affected_users': result['success_count'],
            'total_requested': result['total_requested']
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
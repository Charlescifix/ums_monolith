# User management API serializers

from rest_framework import serializers
from features.authentication.models import User
from features.user_management.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    
    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'date_of_birth', 'location', 'website', 'is_public', 'show_email')

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed user serializer with profile information
    
    Design Decision: Include profile data in user serialization
    - Reduces API calls for common use case
    - Clean nested structure
    """
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 
            'is_active', 'is_email_verified', 'date_joined',
            'last_login', 'profile'
        )
        read_only_fields = ('id', 'date_joined', 'last_login', 'is_email_verified')

class UserListSerializer(serializers.ModelSerializer):
    """Simplified user serializer for list views"""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')

class UserUpdateSerializer(serializers.ModelSerializer):
    """User update serializer with validation"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')
        
    def validate_email(self, value):
        """Ensure email uniqueness"""
        if User.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

class BulkOperationSerializer(serializers.Serializer):
    """Bulk operations serializer"""
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    operation = serializers.ChoiceField(choices=['activate', 'deactivate'])
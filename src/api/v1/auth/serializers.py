# Authentication API serializers
# Decision: Use DRF serializers for clean data validation and transformation

from rest_framework import serializers
from features.authentication.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    User registration serializer
    
    Design Decision: Separate registration from user model serializer
    - Different validation rules for registration
    - Hides sensitive fields from API response
    """
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone')
        extra_kwargs = {
            'email': {'required': True},
        }

    def create(self, validated_data):
        # Use service layer for business logic
        from features.authentication.services import AuthenticationService
        service = AuthenticationService()
        return service.register_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    """
    Login credentials serializer
    
    Design Decision: Use separate serializer for login
    - Clean separation of concerns
    - Easy to add additional login fields (2FA, etc.)
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    """Basic user information serializer"""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_email_verified', 'date_joined')
        read_only_fields = ('id', 'is_email_verified', 'date_joined')
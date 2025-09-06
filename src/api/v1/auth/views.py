# Authentication API views
# Decision: Use DRF class-based views for consistency and built-in functionality

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from features.authentication.services import AuthenticationService
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    User registration endpoint
    
    Design Decision: Function-based view for simple operations
    - Cleaner code for single-purpose endpoints
    - Easy to understand and test
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login endpoint
    
    Returns JWT tokens on successful authentication
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        service = AuthenticationService()
        user = service.authenticate_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    """
    Password reset request endpoint
    
    Design Decision: Always return success to prevent email enumeration
    """
    email = request.data.get('email')
    if email:
        service = AuthenticationService()
        service.send_password_reset(email)
    
    return Response(
        {'message': 'If the email exists, a reset link has been sent.'},
        status=status.HTTP_200_OK
    )
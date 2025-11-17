from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .serializers import (
    UserSerializer, LoginSerializer, LogoutSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer)
from .service.passwordResetService import PasswordResetService
from .service.userService import UserService
from backend.utils.token_utils import get_tokens_for_user, blacklist_token, refresh_token_for_user
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserRegistrationView(GenericAPIView):
    """
    API view for user registration
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.register_user(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            password=serializer.validated_data['password']
        )
        tokens = get_tokens_for_user(user)
        return Response({
            "success": True,
            "message": "User registered successfully.",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)

class UserLoginView(GenericAPIView):
    """
    API view for user login
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.login_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response({
                "success": False,
                "message": "Invalid email or password."
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        tokens = get_tokens_for_user(user)
        return Response({
            "success": True,
            "message": "User logged in successfully.",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            "tokens": tokens
        }, status=status.HTTP_200_OK)

class LogoutView(GenericAPIView):
    """
    API view for user logout
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            blacklist_token(refresh_token)
            return Response({
                "success": True,
                "message": "User logged out successfully."
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({
                "success": False,
                "message": "An error occurred during logout."
            }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(GenericAPIView):
    """
    API view to request a password reset
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        success = PasswordResetService.request_password_reset(email)
        if success:
            return Response({
                "success": True,
                "message": "Password reset email sent if user exists."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "User with this email does not exist."
            }, status=status.HTTP_404_NOT_FOUND)


class ResendPasswordResetCodeView(GenericAPIView):
    """
    API view to resend password reset code
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        success, error_message = PasswordResetService.resend_password_reset_code(email)
        
        if success:
            return Response({
                "success": True,
                "message": "New password reset code has been sent."
            }, status=status.HTTP_200_OK)
        else:
            # If there's a specific error message (like wait time), use it
            message = error_message if error_message else "Failed to resend reset code."
            return Response({
                "success": False,
                "message": message
            }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(GenericAPIView):
    """
    API view to reset password using a reset code
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        try:
            success = PasswordResetService.reset_password(code, email, new_password)
            if success:
                return Response({
                    "success": True,
                    "message": "Password has been reset successfully."
                }, status=status.HTTP_200_OK)
        except ValidationError as ve:
            return Response({
                "success": False,
                "message": str(ve)
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
def RefreshTokenView(GenericAPIView):
    """
    API view to refresh JWT tokens
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                "success": False,
                "message": "Refresh token is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        new_tokens = refresh_token_for_user(refresh_token)
        if new_tokens:
            return Response({
                "success": True,
                "message": "Token refreshed successfully.",
                "tokens": new_tokens
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "message": "Invalid or expired refresh token."
            }, status=status.HTTP_400_BAD_REQUEST)
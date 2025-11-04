from rest_framework import serializers
from rest_framework.validators import ValidationError

class UserSerializer(serializers.Serializer):
    """
    Serializer for user registration
    """
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    confirm_password = serializers.CharField(max_length=100, write_only=True)
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords do not match.")
        if len(data['password']) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in data['password']):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in data['password']):
            raise ValidationError("Password must contain at least one letter.")
        return data
    
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)

class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout
    """
    refresh = serializers.CharField()
    
class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset code
    """
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for resetting password"""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100, write_only=True)
    confirm_new_password = serializers.CharField(max_length=100, write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise ValidationError("New passwords do not match.")
        if len(data['new_password']) < 8:
            raise ValidationError("New password must be at least 8 characters long.")
        if not any(char.isdigit() for char in data['new_password']):
            raise ValidationError("New password must contain at least one digit.")
        if not any(char.isalpha() for char in data['new_password']):
            raise ValidationError("New password must contain at least one letter.")
        return data
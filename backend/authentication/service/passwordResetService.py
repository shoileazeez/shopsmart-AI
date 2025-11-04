from django.core.exceptions import ValidationError
from ..repositories.userRepository import UserRepository
from ..repositories.resetCodeRepository import ResetCodeRepository

class PasswordResetService:
    """
    Handle business logic for password reset operations
    """

    @staticmethod
    def request_password_reset(email: str) -> bool:
        """
        Request a password reset for a user
        
        Args:
            email: The email address of the user requesting password reset
            
        Returns:
            bool: True if request was successful, False if user not found
        """
        user = UserRepository.get_user_by_email(email)
        if not user:
            return False
            
        # Create new reset token - signal will handle email sending
        reset_token = ResetCodeRepository.create_reset_token(user)
        return reset_token is not None

    @staticmethod
    def reset_password(code: str, email: str, new_password: str) -> bool:
        """
        Reset a user's password using a reset token
        
        Args:
            code: The reset code
            email: The user's email
            new_password: The new password to set
            
        Returns:
            bool: True if password was reset successfully
            
        Raises:
            ValidationError: If token is invalid or expired
        """
        user = UserRepository.get_user_by_email(email)
        if not user:
            raise ValidationError("User not found.")
            
        reset_token = ResetCodeRepository.validate_reset_token(user, code)
        if not reset_token:
            raise ValidationError("Invalid or expired reset code.")
        
        # Update password through UserRepository
        try:
            user.set_password(new_password)
            user.save()
            reset_token.delete()  # Delete used token
            return True
        except Exception as e:
            raise ValidationError(f"Failed to update password: {str(e)}")

    @staticmethod
    def resend_password_reset_code(email: str) -> tuple[bool, str | None]:
        """
        Resend a password reset code to the user
        
        Args:
            email: The email address of the user
            
        Returns:
            tuple: (success: bool, error_message: str | None)
        """
        user = UserRepository.get_user_by_email(email)
        if not user:
            return False, "User not found"
            
        # Check if user can request a new token
        can_resend, error_message = ResetCodeRepository.can_resend_token(user)
        if not can_resend:
            return False, error_message
            
        # Create new reset token - signal will handle email sending
        reset_token = ResetCodeRepository.create_reset_token(user)
        if reset_token:
            return True, None
        return False, "Failed to create reset token"
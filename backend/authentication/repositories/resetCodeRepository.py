from typing import Tuple, Optional
from ..models import PasswordResetToken
import random
from django.utils import timezone
from datetime import timedelta

def generate_code():
    return str(random.randint(100000, 999999))

class ResetCodeRepository:
    """
    Handle database operations related to password reset codes.
    """
    
    @staticmethod
    def cleanup_expired_tokens(user) -> None:
        """
        Delete any expired tokens for a user
        """
        PasswordResetToken.objects.filter(
            user=user,
            expires_at__lt=timezone.now()
        ).delete()
    
    @staticmethod
    def create_reset_token(user) -> PasswordResetToken:
        """
        Create a new reset token, cleaning up any existing ones
        """
        if not user:
            return None
            
        # Clean up any expired tokens first
        ResetCodeRepository.cleanup_expired_tokens(user)
        
        # Delete any existing valid tokens
        PasswordResetToken.objects.filter(user=user).delete()
        
        code = generate_code()
        expires_at = timezone.now() + timedelta(minutes=30)  # 30 minutes expiry
        return PasswordResetToken.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )

    @staticmethod
    def validate_reset_token(user, code) -> Optional[PasswordResetToken]:
        """
        Validate a reset token and clean up if expired
        """
        if not user:
            return None
            
        try:
            token = PasswordResetToken.objects.get(user=user, code=code)
            if token.expires_at < timezone.now():
                token.delete()
                return None
            return token
        except PasswordResetToken.DoesNotExist:
            return None
    
    @staticmethod
    def can_resend_token(user) -> Tuple[bool, Optional[str]]:
        """
        Check if a user can request a new token
        Returns (can_resend, error_message)
        """
        if not user:
            return False, "User not found"
            
        # Clean up any expired tokens first
        ResetCodeRepository.cleanup_expired_tokens(user)
        
        # Check for existing valid token
        existing_token = PasswordResetToken.objects.filter(user=user).first()
        if existing_token:
            # Check if the last token was created less than 2 minutes ago
            time_since_last_token = timezone.now() - existing_token.created_at
            if time_since_last_token < timedelta(minutes=2):
                seconds_remaining = int((timedelta(minutes=2) - time_since_last_token).total_seconds())
                return False, f"Please wait {seconds_remaining} seconds before requesting a new code"
                
        return True, None
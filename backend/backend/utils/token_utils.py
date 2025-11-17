from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    Generate JWT tokens for a user
    
    Args:
        user: The user object to generate tokens for
        
    Returns:
        dict: Dictionary containing access and refresh tokens
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def blacklist_token(refresh_token):
    """
    Blacklist a refresh token
    
    Args:
        refresh_token: The refresh token to blacklist
        
    Returns:
        bool: True if successful
    """
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return True
    except Exception:
        return False
    
def refresh_token_for_user(refresh_token):
    """
    Refresh access token using a refresh token
    
    Args:
        refresh_token: The refresh token to use for refreshing
        
    Returns:
        dict: Dictionary containing new access and refresh tokens
    """
    try:
        token = RefreshToken(refresh_token)
        new_access_token = str(token.access_token)
        new_refresh_token = str(token)
        return {
            'refresh': new_refresh_token,
            'access': new_access_token,
        }
    except Exception:
        return None
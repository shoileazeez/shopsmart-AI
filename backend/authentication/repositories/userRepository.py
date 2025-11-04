from ..models import User

class UserRepository:
    """
      Handle database access for user model
    """
    
    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def validate_email_for_register(email: str) -> bool:
        return not User.objects.filter(email=email).exists()
    
    @staticmethod
    def register_new_user(email: str, password: str, first_name: str, last_name: str) -> User:
        if not UserRepository.validate_email_for_register(email):
            raise ValueError("Email already in use")
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_staff=False,
        )
        return user
    
    @staticmethod
    def delete_user_by_email_and_id(email: str, id:int) -> str | None:
        try:
            user = User.objects.get(email=email, id=id)
            user.delete()
            return "User deleted successfully"
        except User.DoesNotExist:
            return None
        
    @staticmethod
    def login_user(email: str,  password: str) -> User | None:
        user = UserRepository.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None
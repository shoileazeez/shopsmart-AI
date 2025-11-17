from ..repositories.userRepository import UserRepository

class UserService:
    """
    Handle business logic for user operations
    """
    
    @staticmethod
    def register_user(email: str, password: str, first_name: str, last_name: str):
        return UserRepository.register_new_user(email, password, first_name, last_name)
    
    @staticmethod
    def login_user(email: str, password: str):
        return UserRepository.login_user(email, password)
    
    @staticmethod
    def delete_user(email: str, id: int):
        return UserRepository.delete_user_by_email_and_id(email, id)
    
    @staticmethod
    def get_user_by_id(id: int):
        return UserRepository.get_user_by_id(id)
from backend .utils.get_user_id import get_user_id_from_request

def fetch_user_id(request) -> str | None:
    """
    Utility function to fetch user ID from request
    """
    return get_user_id_from_request(request)
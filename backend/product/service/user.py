# from authentication.service.userService import UserService
from backend.utils.get_user_id import get_user_first_name_from_request
from typing import Optional


def get_user_first_name(user_id: Optional[int] = None, request=None) -> Optional[str]:
    """
    Return user's first name.

    Preferred order:
    - If ``request`` is provided and contains an authenticated user, extract first name from it.
    - Else, if ``user_id`` is provided, query via UserService.get_user_by_id.
    - Otherwise return None.
    """
    # Try to get first name directly from request if provided
    if request is not None:
        first_name = get_user_first_name_from_request(request)
        if first_name:
            return first_name

    # Fallback to DB lookup using user_id
    # if user_id is not None:
    #     user = UserService.get_user_by_id(user_id)
    #     if user:
    #         return getattr(user, "first_name", None)

    return None
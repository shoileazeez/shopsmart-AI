from typing import Optional, Dict, Any


def get_user_info_from_request(request) -> Optional[Dict[str, Any]]:
    """
    Extract current user's id and first name from a Django/DRF request.

    Returns a dict with keys: 'id' and 'first_name' when the user is authenticated.
    Returns None when there is no authenticated user.

    The function is defensive: it supports both Django's HttpRequest and DRF's Request
    (which wraps the Django request).
    """
    if request is None:
        return None

    # DRF Request wraps the django request and provides .user
    user = getattr(request, "user", None)

    if not user:
        # Some callers may pass the underlying django request as `request._request`
        inner = getattr(request, "_request", None)
        user = getattr(inner, "user", None) if inner is not None else None

    if user and getattr(user, "is_authenticated", False):
        return {"id": getattr(user, "id", None), "first_name": getattr(user, "first_name", None)}

    return None


def get_user_id_from_request(request) -> Optional[int]:
    info = get_user_info_from_request(request)
    if info:
        return info.get("id")
    return None


def get_user_first_name_from_request(request) -> Optional[str]:
    info = get_user_info_from_request(request)
    if info:
        return info.get("first_name")
    return None

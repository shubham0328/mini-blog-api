from .in_memory import USERS


#It verifies the request token and returns the matching user if valid, or None if not authenticated.
def get_user_from_token(request): #checks the incoming requests
    """
    Extract user from Authorization header.
    Expected header: Authorization: Token <token>
    - The "Token" prefix check is case-insensitive.
    Returns user dict on success or None on failure.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    parts = auth_header.split()
    # Accept "Token <token>" (case-insensitive) or a single bare token (less preferred).
    if len(parts) == 2 and parts[0].lower() == "token":
        token = parts[1]
    else:
        # Do not accept malformed headers (strict)
        return None

    for user in USERS:
        if user.get("token") == token:
            return user
    return None

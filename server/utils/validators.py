def validate_username(username):
    if not isinstance(username, str) or len(username.strip()) < 3:
        return False, "Username must be at least 3 characters long."
    return True, ""

def registration_data(payload):
    payload = payload or {}
    username = payload.get("username")
    password = payload.get("password")
    confirmation = payload.get("password_confirmation")
    if not isinstance(username, str) or not username.strip():
        return None, "Username is required."
    if not isinstance(password, str) or not password:
        return None, "Password is required."
    if password != confirmation:
        return None, "Passwords do not match."
    return {
        "username": username.strip(),
        "email": payload.get("email") or f"{username.strip()}@local.invalid",
        "password": password,
    }, None


def task_data(payload, partial=False):
    payload = payload or {}
    allowed = {"title", "description", "completed"}
    data = {key: payload[key] for key in allowed if key in payload}
    if not partial and not data.get("title"):
        return None, "Title is required."
    if partial and not data:
        return None, "At least one task field is required."
    if "title" in data and (not isinstance(data["title"], str) or not data["title"].strip()):
        return None, "Title must be a non-empty string."
    if "completed" in data and not isinstance(data["completed"], bool):
        return None, "Completed must be a boolean."
    if "title" in data:
        data["title"] = data["title"].strip()
    return data, None


from server.schemas.user_schema import user_schema, users_schema
from server.schemas.task_schema import task_schema, tasks_schema

__all__ = [
    "registration_data",
    "task_data",
    "user_schema",
    "users_schema",
    "task_schema",
    "tasks_schema",
]
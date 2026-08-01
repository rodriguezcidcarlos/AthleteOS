from werkzeug.security import check_password_hash

from auth.users import USERS


def authenticate(username, password):

    user = USERS.get(username)

    if user is None:
        return None

    if not check_password_hash(
        user["password"],
        password
    ):
        return None

    return {
        "authenticated": True,
        "username": username,
        "role": user["role"]
    }
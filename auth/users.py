from werkzeug.security import generate_password_hash


USERS = {
    "admin": {
        "password": generate_password_hash(
            "AthleteOS2026"
        ),
        "role": "admin"
    }
}
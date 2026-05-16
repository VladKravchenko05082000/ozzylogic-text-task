import bcrypt

from configs.general_constants import BCRYPT_ROUNDS
from configs.regex import PASSWORD_RE

def validate_password(password: str):
    if not isinstance(password, str):
        raise ValueError("password must be a string")
    if not PASSWORD_RE.match(password):
        raise ValueError(
            "password must be 8-20 chars and contain letters and digits"
        )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=BCRYPT_ROUNDS),
    ).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False
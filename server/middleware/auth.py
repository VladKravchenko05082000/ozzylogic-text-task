from functools import wraps

from models.user_models import find_user_by_id

from lib.jwt_helpers import decode_token
from lib.helpers import get_file_logger

from configs.error_logs_files_name import AUTH_FLOW_ERROR_FILE_NAME

logger = get_file_logger(AUTH_FLOW_ERROR_FILE_NAME)


class AuthError(Exception):
    """Authentication error — maps to 401."""

def _extract_bearer(headers: dict) -> str:
    auth_header = headers.get("authorization")
    if not auth_header:
        raise ValueError("missing authorization header")
    parts = auth_header.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("invalid authorization header")
    return parts[1].strip()


def _authenticate(access_token: str) -> dict:
    claims = decode_token(access_token, expected_type="access")
    user = find_user_by_id(claims["user_id"])
    if not user:
        raise ValueError("user not found")
    return {
        "id": user["id"],
        "email": user["email"],
        "newsletter_enabled": bool(user["newsletter_enabled"]),
        "created_at": user.get("created_at"),
    }


def require_auth(handler):
    @wraps(handler)
    def wrapped(*, headers, **kwargs):
        try:
            token = _extract_bearer(headers)
            user = _authenticate(token)
        except ValueError as e:
            logger.error("require_auth error: %s", e)
            return {"status": 401, "response": {"error": str(e)}}
        return handler(current_user=user, headers=headers, **kwargs)

    return wrapped

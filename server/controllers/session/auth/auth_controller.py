from models.user_models import (find_user_by_email, create_user, find_user_by_id)
from models.session_tokens_models import (store_refresh_token)

from lib.password_helpers import (hash_password, validate_password, verify_password)
from lib.jwt_helpers import (get_token_pair, serialize_tokens)
from lib.helpers import (get_file_logger, validate_email)

from configs.error_logs_files_name import AUTH_FLOW_ERROR_FILE_NAME

from configs.types import TokenPair
from middleware.auth import AuthError

logger = get_file_logger(AUTH_FLOW_ERROR_FILE_NAME)

def _user_login_user(email: str, password: str) -> tuple[dict, TokenPair]:
    email = validate_email(email)
    user = find_user_by_email(email)

    if not user or not verify_password(password, user["password_hash"]):
        raise AuthError("invalid credentials")

    tokens = get_token_pair(user.get("id"))
    store_refresh_token(
        tokens.get("refresh_jwt_id", ""), user.get("id"), tokens.get("refresh_expires_at", "")
    )

    return {
        "id": user.get("id"),
        "email": user.get("email"),
        "newsletter_enabled": bool(user.get("newsletter_enabled", 0)),
        "created_at": user.get("created_at"),
    }, tokens



def user_register(*, body, **_):
    try:
        email = validate_email(body.get("email", ""))
        password = body.get("password", "")
        validate_password(password)

        if find_user_by_email(email):
            return {"status": 409, "response": {"error": "email already user_registered"}}

        user_id = create_user(
            email=email,
            password_hash=hash_password(password),
        )

        user, tokens = _user_login_user(email, password)
        return {"status": 201, "response": {"user": user, "tokens": serialize_tokens(tokens)}}

    except ValueError as e:
        logger.error("user_register validation error: %s", e)
        return {"status": 400, "response": {"error": str(e)}}

def user_login(*, body, **_):
    try:
        user, tokens = _user_login_user(body.get("email", ""), body.get("password", ""))
        return {"status": 200, "response": {"user": user, "tokens": serialize_tokens(tokens)}}
    except ValueError as e:
        logger.error("user_login validation error: %s", e)
        return {"status": 400, "response": {"error": str(e)}}
    except AuthError as e:
        logger.error("user_login auth error: %s", e)
        return {"status": 401, "response": {"error": str(e)}}
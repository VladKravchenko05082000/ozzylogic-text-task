from models.session_tokens_models import (is_refresh_token_active, revoke_refresh_token, store_refresh_token)
from models.user_models import (find_user_by_id)

from lib.jwt_helpers import (decode_token, get_token_pair, serialize_tokens)
from lib.helpers import get_file_logger

from configs.error_logs_files_name import AUTH_FLOW_ERROR_FILE_NAME

from configs.types import TokenPair
from middleware.auth import AuthError

logger = get_file_logger(AUTH_FLOW_ERROR_FILE_NAME)


def _refresh_tokens(refresh_token: str) -> TokenPair:
    claims = decode_token(refresh_token, expected_type="refresh")

    if not is_refresh_token_active(claims.get("jwt_id")):
        raise AuthError("refresh token revoked or unknown")

    user = find_user_by_id(claims.get("user_id"))
    if not user:
        raise AuthError("user not found")

    revoke_refresh_token(claims.get("jwt_id"))
    new_pair = get_token_pair(user.get("id"))
    store_refresh_token(
        new_pair.get("refresh_jwt_id"), user.get("id"), new_pair.get("refresh_expires_at")
    )
    return new_pair


def _logout(refresh_token: str) -> None:
    try:
        claims = decode_token(refresh_token, expected_type="refresh")
        revoke_refresh_token(claims.get("jwt_id"))
    except ValueError:
        pass


def refresh(*, body, **_):
    refresh_token = body.get("refresh_token")
    if not refresh_token:
        return {"status": 400, "response": {"error": "refresh_token is required"}}
    try:
        pair = _refresh_tokens(refresh_token)
    except (AuthError, ValueError) as e:
        logger.error("refresh error: %s", e)
        return {"status": 401, "response": {"error": str(e)}}
    return {"status": 200, "response": {"tokens": serialize_tokens(pair)}}


def logout_from_session(*, body, **_):
    _logout(body.get("refresh_token"))
    return {"status": 200, "response": {"ok": True}}

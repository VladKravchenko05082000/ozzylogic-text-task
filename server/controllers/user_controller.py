from models.user_models import (find_user_by_email, update_user, find_user_by_id)
from models.session_tokens_models import (revoke_all_user_tokens)

from middleware.auth import require_auth
from lib.helpers import validate_email, get_file_logger
from lib.password_helpers import (verify_password, validate_password, hash_password)

from configs.error_logs_files_name import USER_ERROR_FILE_NAME

from typing import Optional
from middleware.auth import AuthError

logger = get_file_logger(USER_ERROR_FILE_NAME)


def _update_profile(
    user_id: int,
    email: Optional[str] = None,
    newsletter_enabled: bool = False
) -> dict:
    fields: dict = {}

    if email is not None:
        new_email = validate_email(email)
        existing = find_user_by_email(new_email)
        if existing and existing.get("id") != user_id:
            raise ValueError("email already in use")
        fields["email"] = new_email
    
    fields["newsletter_enabled"] = newsletter_enabled

    updated = update_user(user_id, fields)
    if not updated:
        raise AuthError("user not found")

    return updated


def _change_password(user_id: int, current_password: str, new_password: str) -> None:
    user = find_user_by_id(user_id)
    if not user:
        raise AuthError("user not found")

    if not verify_password(current_password, user["password_hash"]):
        raise AuthError("current password is incorrect")

    validate_password(new_password)
    update_user(
        user_id, {"password_hash": hash_password(new_password)}
    )

    revoke_all_user_tokens(user_id)

@require_auth
def get_me(*, current_user, **_):
    return {"status": 200, "response": {"user": current_user}}

@require_auth
def update_user_profile(*, current_user, body, **_):
    try:
        updated = _update_profile(
            current_user.get("id"),
            email=body.get("email"),
            newsletter_enabled=body.get("newsletter_enabled", False)
        )
    except ValueError as e:
        logger.error("update_user_profile validation error: %s", e)
        return {"status": 400, "response": {"error": str(e)}}
    except AuthError as e:
        logger.error("update_user_profile auth error: %s", e)
        return {"status": 401, "response": {"error": str(e)}}
    return {"status": 200, "response": {"user": updated}}


@require_auth
def change_password(*, current_user, body, **_):
    try:
        _change_password(
            current_user["id"],
            body.get("current_password", ""),
            body.get("new_password", ""),
        )
    except ValueError as e:
        logger.error("change_password validation error: %s", e)
        return {"status": 400, "response": {"error": str(e)}}
    except AuthError as e:
        logger.error("change_password auth error: %s", e)
        return {"status": 401, "response": {"error": str(e)}}
    return {"status": 200, "response": {"ok": True, "message": "password updated, please login again"}}

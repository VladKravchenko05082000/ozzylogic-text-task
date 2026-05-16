from datetime import datetime

from db import (get_conn, get_file_logger)

from lib.helpers import validate_type

from configs.error_logs_files_name import AUTH_FLOW_ERROR_FILE_NAME

logger = get_file_logger(AUTH_FLOW_ERROR_FILE_NAME)


def store_refresh_token(jwt_id: str, user_id: int, expires_at: datetime) -> None:
    if not validate_type(jwt_id, str, "jwt_id", logger):
        return
    if not validate_type(user_id, int, "user_id", logger):
        return
    if not validate_type(expires_at, datetime, "expires_at", logger):
        return

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO refresh_tokens (jwt_id, user_id, expires_at)
            VALUES (?, ?, ?)
            """,
            (jwt_id, user_id, expires_at.isoformat()),
        )


def is_refresh_token_active(jwt_id: str) -> bool:
    if not validate_type(jwt_id, str, "jwt_id", logger):
        return False

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT revoked FROM refresh_tokens WHERE jwt_id = ?",
            (jwt_id,),
        )
        row = cursor.fetchone()

    if not row:
        return False
    return not row["revoked"]


def revoke_refresh_token(jwt_id: str) -> None:
    if not validate_type(jwt_id, str, "jwt_id", logger):
        return

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE refresh_tokens SET revoked = 1 WHERE jwt_id = ?",
            (jwt_id,),
        )


def revoke_all_user_tokens(user_id: int) -> None:
    if not validate_type(user_id, int, "user_id", logger):
        return

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE refresh_tokens SET revoked = 1 WHERE user_id = ?",
            (user_id,),
        )

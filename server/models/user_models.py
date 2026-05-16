from typing import Optional

from db import get_conn, get_file_logger

from lib.helpers import validate_type

from configs.error_logs_files_name import USER_ERROR_FILE_NAME

logger = get_file_logger(USER_ERROR_FILE_NAME)

_ALLOWED_UPDATE_FIELDS = {"email", "password_hash", "newsletter_enabled"}

def create_user(
    email: str,
    password_hash: str,
    newsletter_enabled: bool = False,
) -> Optional[int]:
    if not validate_type(email, str, "email", logger):
        return None
    if not validate_type(password_hash, str, "password_hash", logger):
        return None

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, newsletter_enabled)
            VALUES (?, ?, ?)
            """,
            (email.lower(), password_hash, int(newsletter_enabled)),
        )
        return cursor.lastrowid


def find_user_by_email(email: str) -> Optional[dict]:
    if not validate_type(email, str, "email", logger):
        return None

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.lower(),),
        )
        row = cursor.fetchone()

    return dict(row) if row else None


def find_user_by_id(user_id: int) -> Optional[dict]:
    if not validate_type(user_id, int, "user_id", logger):
        return None

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()

    return dict(row) if row else None


def update_user(user_id: int, fields: dict) -> Optional[dict]:
    if not validate_type(user_id, int, "user_id", logger):
        return None
    if not fields:
        return find_user_by_id(user_id)

    invalid = set(fields) - _ALLOWED_UPDATE_FIELDS
    if invalid:
        logger.error("update_user: unknown fields %s", invalid)
        return None

    columns = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [user_id]

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE users SET {columns}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            values,
        )

    return find_user_by_id(user_id)

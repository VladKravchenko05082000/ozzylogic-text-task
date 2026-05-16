import uuid
from datetime import datetime, timedelta, timezone
import jwt as pyjwt

from lib.helpers import get_file_logger

from configs.general_constants import (
    JWT_SECRET, JWT_ALGORITHM,
    ACCESS_TOKEN_TTL_MIN, REFRESH_TOKEN_TTL_DAYS,
)
from configs.error_logs_files_name import AUTH_FLOW_ERROR_FILE_NAME

from configs.types import TokenPair

logger = get_file_logger(AUTH_FLOW_ERROR_FILE_NAME)


def _encode(user_id: int, token_type: str, ttl: timedelta) -> tuple[str, str, datetime]:
    now = datetime.now(timezone.utc)
    expires_at = now + ttl
    jwt_id = str(uuid.uuid4())

    token = pyjwt.encode({
        "sub": str(user_id),
        "type": token_type,
        "jwt_id": jwt_id,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token, jwt_id, expires_at

def serialize_tokens(pair: TokenPair) -> TokenPair:
    return {
        "access_token": pair.get("access_token", ""),
        "refresh_token": pair.get("refresh_token", ""),
        "access_expires_at": pair.get("access_expires_at").isoformat(),
        "refresh_expires_at": pair.get("refresh_expires_at").isoformat(),
        "token_type": "Bearer",
    }

def get_token_pair(user_id: int) -> TokenPair:
    access, _, access_exp = _encode(user_id, "access", timedelta(minutes=ACCESS_TOKEN_TTL_MIN))
    refresh, refresh_jwt_id, refresh_exp = _encode(user_id, "refresh", timedelta(days=REFRESH_TOKEN_TTL_DAYS))

    return {
        "access_token": access,
        "refresh_token": refresh,
        "access_expires_at": access_exp,
        "refresh_expires_at": refresh_exp,
        "refresh_jwt_id": refresh_jwt_id,
    }


def decode_token(token: str, expected_type: str) -> dict:
    try:
        payload = pyjwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except pyjwt.ExpiredSignatureError:
        logger.error("Token expired")
        raise ValueError("token expired")
    except pyjwt.InvalidTokenError:
        logger.error("Invalid token")
        raise ValueError("invalid token")

    if payload.get("type") != expected_type:
        logger.error("Token type mismatch: expected %s, got %s", expected_type, payload.get("type"))
        raise ValueError(f"expected {expected_type} token")

    return {
        "user_id": int(payload.get("sub")),
        "jwt_id": payload.get("jwt_id"),
        "expires_at": datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc),
    }
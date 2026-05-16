from typing import  Literal, TypedDict
from datetime import datetime

TimeUnit = Literal["second", "minute", "hour"]

class TokenPair(TypedDict):
    access_token: str
    refresh_token: str
    access_expires_at: datetime
    refresh_expires_at: datetime
    refresh_jwt_id: str
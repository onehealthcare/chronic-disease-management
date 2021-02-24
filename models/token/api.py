import time
from typing import Any, Dict, Optional, Tuple

import jwt
from config import JWT_SECRET
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
)
from models.token.exceptions import InvalidTokenError


def get_jwt(user_id: int, user_name: str) -> Tuple[bytes, bytes]:
    iat = int(time.time())
    data: Dict[str, Any[str, int]] = {
        'exp': iat + 3 * 24 * 3600,  # (expiration time)：过期时间
        'iat': iat,  # (Issued At)：签发时间
        'user_id': user_id,
        'user_name': user_name,
    }

    refresh_data: Dict[str, Any[str, int]] = {
        'exp': iat + 15 * 24 * 3600,  # (expiration time)：过期时间
        'iat': iat,  # (Issued At)：签发时间
        'user_id': user_id,
        'user_name': user_name,
    }

    access_token = jwt.encode(data, JWT_SECRET, algorithm="HS256")
    refresh_token = jwt.encode(refresh_data, JWT_SECRET, algorithm="HS256")

    return access_token, refresh_token


def decode_jwt(token: str) -> Dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except (DecodeError, InvalidSignatureError, ExpiredSignatureError):
        raise InvalidTokenError


def is_token_valid(token: str, user_id: Optional[int] = None) -> bool:
    if not token:
        return False

    try:
        data = decode_jwt(token)
    except InvalidTokenError:
        return False

    if user_id is not None and data.get('user_id', '') != user_id:
        return False

    return True

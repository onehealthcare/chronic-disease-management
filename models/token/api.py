import time
from typing import Any, Dict, Tuple

import jwt
from config import JWT_SECRET
from jwt.exceptions import DecodeError, InvalidSignatureError


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
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])


def is_token_valid(token: str, user_id: int) -> bool:
    try:
        data = decode_jwt(token)
    except DecodeError:
        return False
    except InvalidSignatureError:
        return False

    if data.get('user_id', '') != user_id:
        return False

    now = int(time.time())
    if data.get('exp', 0) < now:
        return False

    return True

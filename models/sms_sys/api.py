import random
from typing import List

from config import DEBUG
from models.redis import (
    delete_sms_auth_code,
    get_sms_auth_code,
    save_sms_auth_code,
)


def generate_and_send_auth_code(phone: str, length: int = 4) -> str:
    _auth_code: str = get_sms_auth_code(phone=phone)
    if _auth_code:
        return _auth_code

    seeds: str = "0123456789"
    codes: List[str] = []

    for i in range(length):
        codes.append(random.choice(seeds))

    auth_code: str = ''.join(codes)
    save_sms_auth_code(phone=phone, auth_code=auth_code)

    return auth_code


def verify_auth_code(phone: str, auth_code: str) -> bool:
    if DEBUG and auth_code == '0000':
        return True

    _auth_code: str = get_sms_auth_code(phone=phone)

    result = auth_code == _auth_code
    if result:
        delete_sms_auth_code(phone=phone)

    return result

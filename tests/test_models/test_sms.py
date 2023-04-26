import config
from models.redis.api import get_sms_auth_code
from models.sms_sys import generate_auth_code, verify_auth_code


def test_sms():
    phone: str = '11111111111'
    length: int = 4
    auth_code: str = generate_auth_code(phone=phone)
    assert len(auth_code) == length

    assert verify_auth_code(phone=phone, auth_code=auth_code)

    assert '' == get_sms_auth_code(phone=phone)

    config.DEBUG = True
    assert verify_auth_code(phone=phone, auth_code='0000')
    config.DEBUG = False

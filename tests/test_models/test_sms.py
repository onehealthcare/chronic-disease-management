import config
from models.redis.api import get_sms_auth_code, send_code_freq_limit
from models.sms_sys import generate_auth_code, verify_auth_code


def test_sms():
    phone: str = '11111111111'
    length: int = 4
    auth_code: str = generate_auth_code(phone=phone)
    assert len(auth_code) == length

    auth_code1: str = generate_auth_code(phone=phone)
    assert auth_code == auth_code1

    assert verify_auth_code(phone=phone, auth_code=auth_code)

    assert '' == get_sms_auth_code(phone=phone)

    config.DEBUG = True
    assert verify_auth_code(phone=phone, auth_code='0000')
    config.DEBUG = False


def test_send_code_freq_limit():
    phone = "123456"
    ret: int = send_code_freq_limit(phone)
    assert not bool(ret)

    ret = send_code_freq_limit(phone)
    assert bool(ret)

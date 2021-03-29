from models.init_db import redis_conn


class RedisKeys(object):
    auth_code_key = "auth_code:{phone}"


def save_sms_auth_code(phone: str, auth_code: str):
    key = RedisKeys.auth_code_key.format(phone=phone)
    redis_conn.set(key, auth_code)
    redis_conn.expire(key, 600)


def get_sms_auth_code(phone: str) -> str:
    key = RedisKeys.auth_code_key.format(phone=phone)
    return redis_conn.get(key) or ''


def delete_sms_auth_code(phone: str):
    key = RedisKeys.auth_code_key.format(phone=phone)
    return redis_conn.delete(key)

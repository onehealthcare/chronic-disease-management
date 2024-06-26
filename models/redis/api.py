from models.init_db import redis_conn


class RedisKeys:
    auth_code_key = "auth_code:{phone}"
    send_code_freq_limit = "send_code_freq_limit:{phone}"


def save_sms_auth_code(phone: str, auth_code: str):
    key = RedisKeys.auth_code_key.format(phone=phone)
    redis_conn.set(key, auth_code)
    redis_conn.expire(key, 300)


def get_sms_auth_code(phone: str) -> str:
    key = RedisKeys.auth_code_key.format(phone=phone)
    return redis_conn.get(key) or ''


def delete_sms_auth_code(phone: str):
    key = RedisKeys.auth_code_key.format(phone=phone)
    return redis_conn.delete(key)


def send_code_freq_limit(phone: str) -> int:
    key = RedisKeys.send_code_freq_limit.format(phone=phone)
    _value = redis_conn.get(key)
    if _value:
        redis_conn.incr(key)
        value = int(_value)
        redis_conn.expire(key, 60 * value)
        return value

    redis_conn.incr(key)
    redis_conn.expire(key, 60)
    return 0

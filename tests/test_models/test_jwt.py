import time

import jwt
import pytest
from models.jwt import decode_jwt, get_jwt, is_token_valid


def test_jwt():
    user_id = 100
    user_name = 'tonghs'

    access_token, refresh_token = get_jwt(user_id=user_id, user_name=user_name)
    assert is_token_valid(access_token, user_id)
    assert is_token_valid(refresh_token, user_id)

    data = decode_jwt(access_token)
    assert data.get('user_id') == user_id
    assert data.get('user_name') == user_name
    assert data.get('exp') > int(time.time()) + 24 * 3600

    data = decode_jwt(refresh_token)
    assert data.get('user_id') == user_id
    assert data.get('user_name') == user_name
    assert data.get('exp') > int(time.time()) + 24 * 3600 * 10

    assert not is_token_valid(access_token, user_id=200)
    assert not is_token_valid(refresh_token, user_id=200)

    assert not is_token_valid('aaa', user_id)

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTQxNDQwMDQsImlhdCI6MTYxMzg4NDgwNCwidXNlcl9pZCI6MTAwLCJ1c2VyX25hbWUiOiJ0b25naHMifQ.Z1JSEJssGWW7_ohEtS1CwzqegWHu38S9RTy-aBhMqH0'
    assert not is_token_valid(token, user_id)
    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        decode_jwt(token)

import pytest
from models.init_db import wxapp_client
from models.wxapp import InvalidAuthCodeError, code_to_session


@pytest.fixture()
def wxapp_client_monkey_patch():
    def _code_to_session(code: str):
        return {
            "openid": "ozRbY5DiATBfayZpZjAC-udvyFfI",
            "session_key": "FVHdBFc0O59/uoAQfgCMjw=="
        }

    setattr(wxapp_client, 'code_to_session', _code_to_session)


def test_code_to_session_exception():
    with pytest.raises(InvalidAuthCodeError):
        code_to_session('aaa')


def test_code_to_session(wxapp_client_monkey_patch):
    code = 'test_code'
    data = code_to_session(code)

    assert data['openid'] == 'ozRbY5DiATBfayZpZjAC-udvyFfI'
    assert data['session_key'] == 'FVHdBFc0O59/uoAQfgCMjw=='

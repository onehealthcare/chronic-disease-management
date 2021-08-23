import pytest
from libs.qcloud import QCloudCOSGetCredentialError
from models.init_db import qcloud_cos_client
from models.qcloud import get_cos_temp_credential


@pytest.fixture
def get_cos_temp_credential_patch():
    def _get_cos_temp_credential():
        return {
            "expiredTime": 1614528057,
            "expiration": "2021-02-28T16:00:57Z",
            "credentials": {
                "sessionToken": "6HVH855hKfUBOg5M21u6GiNyJ14qcvuae8336fc0d755203c754aad7d0052fd08kYrybk4P971aJdFTpKD8YMXb7LNAkWCObFt4z3-qH4TncD5FxN2ww3RQSHi6s9HHzooKxLhg2d_vdU5nRqWP8DbXvlJfr9DrsWjQHxP1BwdkQvKd1iUsUNqBlXWExwWurzXrKuje1XD_M0wlNJjJQtPZsRdzdsB4svijSSmV7c8i6aTnmCI8Y6ayITQ3jGPc_aygY9h1svKTI6-di37AiTI_Af9wAIeVAr5bscQl26V_RhjRmngXiIiBlKUwrVVDXt59aaHbV2IrlNtVXqXzpKr4xH1lJc0qVhKiEnhploXruZsNeMpmrnHXTtLrxvpSu6vBUnHKeH6GHRU36j9TjxmykNPTlUTaUL906sx96SY1QRSzWCitoUd05tJbosOgsX2XzoUPJvft0S8TH1UFH9Cb6O3JYu6U6QWsXo9vxMK2_fQJ2NGeO15xvnzf6JZ5XeVaa5ba3qZS_BXTt6j974is4mrv3CR3w4dEt6hm7nxUMunG77eiWMJjDya6n-xIuDibPgK_IOlqrbvJNxiyM_Joo-vUVOsWe69wFSlhtHF_7D9imAbElDkvfiFx-QU2n-XinzDEONhc4WZtyPTT2Q",
                "tmpSecretId": "AKIDHcylfnJro3i3p4Zsja_NwL-cUnXmJC1HKlFgNKrEe3KsdTMqwQbKUOabro9BGM1Y",
                "tmpSecretKey": "cydqH1xZHCrnuojsOaTDC4zgj4oT+0qNpJAUc1urG8Y="
            },
            "requestId": "714215aa-2c1b-44dd-b78d-2fbdd66aefe6",
            "startTime": 1614526257
        }

    setattr(qcloud_cos_client, 'get_temp_credential', _get_cos_temp_credential)


@pytest.mark.usefixtures("get_cos_temp_credential_patch")
def test_get_credential():
    ret = get_cos_temp_credential()

    assert 'expired_time' in ret
    assert 'start_time' in ret
    assert 'token' in ret
    assert 'secret_id' in ret
    assert 'secret_key' in ret


@pytest.fixture
def get_cos_temp_credential_patch1():
    def _get_cos_temp_credential():
        raise QCloudCOSGetCredentialError()

    setattr(qcloud_cos_client, 'get_temp_credential', _get_cos_temp_credential)


def test_get_credential_exception(get_cos_temp_credential_patch1):
    with pytest.raises(QCloudCOSGetCredentialError):
        get_cos_temp_credential()

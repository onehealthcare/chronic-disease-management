import datetime
from typing import Dict

import simplejson

from models.tower_sys import api as tower_api
from models.user_sys import api as user_api
from models.user_sys import UserAuthProvider


def save_access_token(auth_code: str, user_id: int) -> str:
    data: Dict = tower_api.get_access_token_by_auth_code(auth_code=auth_code, user_id=user_id)
    access_token: str = data.get("access_token")
    refresh_token: str = data.get("refresh_token")
    expires_in: int = int(data.get("expires_in"))

    user_api.create_user_auth(
        user_id=user_id, third_party_id=user_id, provider=UserAuthProvider.TOWER,
        access_token=access_token, refresh_token=refresh_token,
        expires_date=datetime.datetime.now() + datetime.timedelta(seconds=expires_in),
        detail_json=simplejson.dumps({"txt": "tower notion sync"})
    )

    return access_token


def refresh_access_token():
    pass


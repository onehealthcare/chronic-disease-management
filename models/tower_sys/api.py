from typing import Dict
from models.init_db import tower_client
from config import HOST


def get_access_token_by_auth_code(auth_code: str, user_id: int) -> Dict:
    """
    获取 tower access token
    :param auth_code:
    :return:
        {
            "access_token": "d4e949df783404f22e882430158f3b0440b608709d833f9b981e9a96b850f05c",
            "token_type": "bearer",
            "expires_in": 7199,
            "refresh_token": "c426d5ab6a211310df088c77b36b38592f6752d5238f291b79174d93f7dc2ed5",
            "created_at": 1523420694,
            "email": "tower@tower.im"
        }
    """
    redirect_uri = f"{HOST}/tower/oauth_callback?user_id={user_id}"
    return tower_client.get_access_token_by_auth_code(auth_code=auth_code, redirect_uri=redirect_uri)


def refresh_access_token(access_token: str, refresh_token: str, user_id: int):
    """
    刷新 access_token
    :param access_token:
    :param refresh_token:
    :param user_id:
    :return:
    """
    redirect_uri = f"{HOST}/tower/oauth_callback?user_id={user_id}"
    return tower_client.refresh_access_token(
        access_token=access_token, refresh_token=refresh_token,
        redirect_uri=redirect_uri
    )


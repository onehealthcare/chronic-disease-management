from typing import Dict

from models.user_sys import UserDTO


def dump_account(user: UserDTO, access_token: str, refresh_token: str) -> Dict[str, str]:
    return {
        'user_id': str(user.id),
        'user_name': user.name,
        'access_token': access_token,
        'refresh_token': refresh_token
    }

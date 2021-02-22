from typing import Dict, List

from models.user_sys import UserDTO


def dump_users(users: List[UserDTO]) -> List[Dict[str, str]]:
    return [dump_user(user) for user in users]


def dump_user(user: UserDTO) -> Dict[str, str]:
    return {
        'user_id': str(user.id),
        'user_name': user.name,
        'is_admin': user.is_admin()
    }

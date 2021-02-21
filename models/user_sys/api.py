import string

from models.const import CommonStatus
from models.init_db import db
from models.user_sys.dao.user import UserDAO
from models.user_sys.dao.user_auth import UserAuthDAO
from models.user_sys.dto.user import UserDTO
from models.user_sys.dto.user_auth import UserAuthDTO
from models.user_sys.exceptions import (
    UserAuthNotFoundException,
    UserNotFoundException,
)
from utils.str_utils import random_str


def get_user_by_id(user_id: int) -> UserDTO:
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException

    return UserDTO.from_dao(user)


def find_avaliable_name(original_name):
    name = original_name
    while True:
        randstr = random_str(4)

        for i in [''] + list(string.ascii_lowercase):
            if not UserDAO.get_by_name(name=name):
                return name
            name = '%s_%s%s' % (original_name, randstr, i)


def create_user(name: str, ident: str = "") -> UserDTO:
    name = find_avaliable_name(name)
    user: UserDAO = UserDAO.create(name=name, ident=ident)
    return UserDTO.from_dao(user)


def update_status_by_user_id(user_id: int, status: int):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException

    user.update_status(status)


def delete_user(user_id: int):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException

    user.update_status(status=CommonStatus.DELETED)


def create_user_auth(user_id: int, third_party_id: str,
                     provider: int, detail_json: str) -> UserAuthDTO:
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException

    return UserAuthDTO.from_dao(UserAuthDAO.create(user_id=user_id,
                                                   third_party_id=third_party_id,
                                                   provider=provider,
                                                   detail_json=detail_json))


def get_user_by_third_party_id(third_party_id: str, provider: int) -> UserDTO:
    dao = UserAuthDAO.get_by_third_party_id_and_provider(
        third_party_id=third_party_id,
        provider=provider
    )

    if not dao or dao.status != CommonStatus.NORMAL:
        raise UserNotFoundException
    else:
        return get_user_by_id(dao.user_id)


@db.atomic()
def create_oauth_user(name: str, ident: str, third_party_id: str,
                      provider: int, detail_json: str) -> UserDTO:

    user = create_user(name=name, ident=ident)
    UserAuthDAO.create(user_id=user.id,
                       third_party_id=third_party_id,
                       provider=provider,
                       detail_json=detail_json)

    return user


def delete_user_auth_by_user_id(user_id: int, provider: int):
    dao = UserAuthDAO.get_by_user_id_and_provider(user_id=user_id, provider=provider)
    if not dao:
        raise UserAuthNotFoundException

    dao.update_status(status=CommonStatus.DELETED)

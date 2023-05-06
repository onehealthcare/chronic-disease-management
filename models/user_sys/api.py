import datetime
import string

import peewee
from models.const import CommonStatus
from models.init_db import db
from models.user_sys.dao.user import UserDAO
from models.user_sys.dao.user_auth import UserAuthDAO
from models.user_sys.dao.user_phone import UserPhoneDAO
from models.user_sys.dto.user import UserDTO
from models.user_sys.dto.user_auth import UserAuthDTO
from models.user_sys.exceptions import (
    DuplicatedUserNameError,
    DuplicatedUserPhoneError,
    EmptyUserNameError,
    UserAuthNotFoundException,
    UserNotFoundException,
)
from utils.str_utils import random_str


def get_user_by_id(user_id: int) -> UserDTO:
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException()

    return UserDTO.from_dao(user)


def find_available_name(original_name):
    name = original_name
    if not UserDAO.get_by_name(name=name):
        return name

    while True:
        randstr = random_str(4)

        for i in [''] + list(string.ascii_lowercase):
            name = f'{name}_{randstr}{i}'
            if not UserDAO.get_by_name(name=name):
                return name


def create_user(name: str, ident: str = "") -> UserDTO:
    if not name:
        raise EmptyUserNameError()
    name = find_available_name(name)
    try:
        user: UserDAO = UserDAO.create(name=name, ident=ident)
    except peewee.IntegrityError:
        raise DuplicatedUserNameError()
    return UserDTO.from_dao(user)


def update_status_by_user_id(user_id: int, status: int):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException()

    user.update_status(status)


def delete_user(user_id: int):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException()

    user.update_status(status=CommonStatus.DELETED)


def create_user_auth(user_id: int, third_party_id: str,
                     provider: int, access_token: str,
                     refresh_token: str, expires_date: datetime.datetime,
                     detail_json: str) -> UserAuthDTO:
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException()

    dao = UserAuthDAO.get_by_user_id_and_provider(user_id=user_id, provider=provider)
    if not dao:
        dao = UserAuthDAO.create(user_id=user_id,
                                 third_party_id=third_party_id,
                                 provider=provider,
                                 access_token=access_token,
                                 refresh_token=refresh_token,
                                 expires_date=expires_date,
                                 detail_json=detail_json)
    else:
        dao.access_token = access_token
        dao.refresh_token = refresh_token
        dao.expires_date = expires_date
        dao.save()

    return UserAuthDTO.from_dao(dao)


def get_user_by_third_party_id(third_party_id: str, provider: int) -> UserDTO:
    dao = UserAuthDAO.get_by_third_party_id_and_provider(
        third_party_id=third_party_id,
        provider=provider
    )

    if not dao or dao.status != CommonStatus.NORMAL:
        raise UserNotFoundException()
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
        raise UserAuthNotFoundException()

    dao.update_status(status=CommonStatus.DELETED)


def set_user_admin(user_id: int):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException()
    user.set_role_admin()


def clear_user_admin(user_id: int):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException()
    user.clear_role_admin()


def paged_get_user_list(cursor: int, size: int = 20):
    daos = UserDAO.paged_get_list(cursor=cursor, size=size)
    return [UserDTO.from_dao(dao) for dao in daos]


def rename_user(user_id: int, user_name: str):
    if not user_name:
        return

    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException()

    try:
        user.rename(user_name=user_name)
    except peewee.IntegrityError:
        raise DuplicatedUserNameError()


def update_user_ident(user_id: int, user_ident: str):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException()

    user.ident = user_ident
    user.save()


def get_user_by_phone(phone: str) -> UserDTO:
    dao = UserPhoneDAO.get_by_phone(phone=phone)

    if not dao or dao.status != CommonStatus.NORMAL:
        raise UserNotFoundException()

    user = get_user_by_id(user_id=dao.user_id)

    return UserDTO.from_dao(user)


@db.atomic()
def create_user_by_phone(phone: str) -> UserDTO:
    dao = UserPhoneDAO.get_by_phone(phone=phone)
    if dao:
        raise DuplicatedUserPhoneError()

    user = create_user(name=f"手机用户{phone[-4:]}")
    UserPhoneDAO.create(user_id=user.id, phone=phone)

    return UserDTO.from_dao(user)


def bind_phone(user_id: int, phone: str):
    dao = UserPhoneDAO.get_by_phone(phone=phone)
    if dao:
        raise DuplicatedUserPhoneError()

    UserPhoneDAO.create(user_id=user_id, phone=phone)


def get_user_auth_by_user_id_and_provider(user_id: int, provider: int):
    dao = UserAuthDAO.get_by_user_id_and_provider(user_id=user_id, provider=provider)
    if not dao:
        raise UserAuthNotFoundException()

    return UserAuthDTO.from_dao(dao)


def update_user_auth_by_user_id_and_provider(user_id: int, provider: int, access_token: str,
                                             refresh_token: str, expires_date: datetime.datetime):
    dao = UserAuthDAO.get_by_user_id_and_provider(user_id=user_id, provider=provider)
    if not dao:
        raise UserAuthNotFoundException()

    dao.update_token(access_token=access_token, refresh_token=refresh_token, expires_date=expires_date)

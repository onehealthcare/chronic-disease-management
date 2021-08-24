import datetime

import pytest
import simplejson
from models.const import CommonStatus
from models.user_sys import (
    DuplicatedUserPhoneError,
    UserAuthNotFoundException,
    UserAuthProvider,
    UserNotFoundException,
    clear_user_admin,
    create_oauth_user,
    create_user,
    create_user_auth,
    create_user_by_phone,
    delete_user,
    delete_user_auth_by_user_id,
    get_user_by_id,
    get_user_by_phone,
    get_user_by_third_party_id,
    paged_get_user_list,
    rename_user,
    set_user_admin,
    update_status_by_user_id,
)
from models.user_sys.dao.user import UserDAO
from models.user_sys.dao.user_auth import UserAuthDAO
from models.user_sys.dao.user_phone import UserPhoneDAO
from models.user_sys.dto.user_phone import UserPhoneDTO
from utils.cursor import get_next_cursor


def test_user():
    user_id = 1
    user_name = 'tonghs'
    ident = 'xxx'

    with pytest.raises(UserNotFoundException):
        get_user_by_id(user_id)

    user = create_user(name=user_name, ident=ident)
    assert user.name == user_name
    assert user.ident == ident
    assert user.id is not None
    assert user.created_at is not None

    now = datetime.datetime.now()
    assert (now - user.created_at).seconds < 300

    update_status_by_user_id(user.id, CommonStatus.INIT)

    user = get_user_by_id(user.id)
    assert user.status == CommonStatus.INIT

    delete_user(user.id)
    user = get_user_by_id(user.id)
    assert user.status == CommonStatus.DELETED

    with pytest.raises(UserNotFoundException):
        delete_user(4)

    with pytest.raises(UserNotFoundException):
        update_status_by_user_id(4, CommonStatus.INIT)

    # 创建一样 user_name 的用户
    user = create_user(name=user_name, ident=ident)
    assert user_name in user.name
    assert len(user.name) >= len(user_name) + 5

    # user role
    with pytest.raises(UserNotFoundException):
        set_user_admin(10000)

    user = UserDAO.get_by_id(user.id)
    assert not user.is_admin()

    set_user_admin(user.id)
    user = get_user_by_id(user.id)
    assert user.is_admin()

    with pytest.raises(UserNotFoundException):
        clear_user_admin(10000)

    clear_user_admin(user.id)
    user = get_user_by_id(user.id)
    assert not user.is_admin()

    user = UserDAO.get_by_id(user.id)
    user.set_role_admin()
    user.set_role_clear()
    assert user.bits == 0

    # empty user name
    user = create_user(name='', ident=ident)
    assert '用户' in user.name

    # rename user
    new_user_name = 'tttt'
    rename_user(user.id, new_user_name)
    user = get_user_by_id(user.id)
    assert user.name == new_user_name

    rename_user(user.id, "")
    user = get_user_by_id(user.id)
    assert user.name == new_user_name

    with pytest.raises(UserNotFoundException):
        rename_user(20000, "tonghs")


def test_user_auth():
    user_id = 100
    user_name = 'tonghs1'
    third_party_id = 'open_id'
    unique_id = "xxx"
    detail = {"unique_id": unique_id}
    provider = UserAuthProvider.WXAPP

    with pytest.raises(UserNotFoundException):
        create_user_auth(user_id=user_id,
                         third_party_id=third_party_id,
                         provider=provider,
                         access_token="",
                         refresh_token="",
                         expires_date=datetime.datetime.now(),
                         detail_json=simplejson.dumps(detail))

    with pytest.raises(UserAuthNotFoundException):
        delete_user_auth_by_user_id(user_id=user_id, provider=provider)

    with pytest.raises(UserAuthNotFoundException):
        delete_user_auth_by_user_id(user_id=2, provider=provider)

    with pytest.raises(UserNotFoundException):
        get_user_by_third_party_id(third_party_id=100, provider=provider)
        get_user_by_third_party_id(third_party_id=third_party_id,
                                   provider=UserAuthProvider.WEIBO)

    _user = create_oauth_user(name=user_name, ident="",
                              third_party_id=third_party_id,
                              provider=provider,
                              detail_json=simplejson.dumps(detail))

    user = get_user_by_id(_user.id)
    assert user.name == user_name

    user_dto = get_user_by_third_party_id(third_party_id=third_party_id, provider=provider)
    assert user_dto.id == user.id

    user_auth = UserAuthDAO.get_by_third_party_id_and_provider(
        third_party_id=third_party_id,
        provider=provider
    )
    assert user_auth.user_id == user.id
    assert user_auth.status == CommonStatus.NORMAL
    assert simplejson.loads(user_auth.detail_json).get('unique_id') == unique_id

    with pytest.raises(UserAuthNotFoundException):
        delete_user_auth_by_user_id(user_id=user_id, provider=UserAuthProvider.WEIBO)

    delete_user_auth_by_user_id(user_id=user.id, provider=provider)
    with pytest.raises(UserNotFoundException):
        get_user_by_third_party_id(third_party_id=third_party_id, provider=provider)

    user_auth = UserAuthDAO.get_by_third_party_id_and_provider(third_party_id=third_party_id, provider=provider)
    assert user_auth.status == CommonStatus.DELETED

    user_auth.delete()

    user_auth_dto = create_user_auth(user_id=user.id,
                                     third_party_id=third_party_id,
                                     provider=provider,
                                     detail_json=simplejson.dumps(detail))
    assert user_auth_dto.user_id == user.id
    assert user_auth_dto.status == CommonStatus.NORMAL
    assert user_auth_dto.detail_json.get('unique_id') == unique_id


@pytest.mark.parametrize('size,result', [
    (100, True),
    (1, False),
])
def test_paged_users(size, result):
    users = paged_get_user_list(cursor=0, size=size)
    assert len(users) > 0

    new_users, next_cursor = get_next_cursor(users, size)
    assert (len(new_users) == len(users)) == result
    assert (next_cursor == '') == result


def test_user_phone():
    phone: str = '11111111111'

    with pytest.raises(UserNotFoundException):
        get_user_by_phone(phone)

    user1 = create_user_by_phone(phone=phone)
    user2 = get_user_by_phone(phone)

    assert user1.id == user2.id
    assert user1.name == user2.name

    dao = UserPhoneDAO.get_by_phone(phone=phone)
    dto = UserPhoneDTO.from_dao(dao)
    assert dao.id == dto.id

    with pytest.raises(DuplicatedUserPhoneError):
        create_user_by_phone(phone=phone)

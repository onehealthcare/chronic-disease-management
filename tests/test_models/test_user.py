import datetime

import pytest
import simplejson
from models.const import CommonStatus
from models.user_sys import (
    UserAuthNotFoundException,
    UserAuthProvider,
    UserNotFoundException,
    create_oauth_user,
    create_user,
    create_user_auth,
    delete_user,
    delete_user_auth_by_user_id,
    get_user_by_id,
    get_user_by_third_party_id,
    update_status_by_user_id,
)
from models.user_sys.dao.user_auth import UserAuthDAO


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
    assert len(user.name) == len(user_name) + 5


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

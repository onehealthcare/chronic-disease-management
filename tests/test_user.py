from models.const import CommonStatus
from models.user_sys import (
    UserNotFoundException,
    create_user,
    delete_user,
    get_user_by_id,
    update_status_by_user_id,
)


def test_user():
    user_id = 1
    user_name = 'tonghs'
    ident = 'xxx'

    try:
        get_user_by_id(user_id)
    except UserNotFoundException:
        pass
    else:
        raise

    user = create_user(name=user_name, ident=ident)
    assert user.name == user_name
    assert user.ident == ident
    assert user.id is not None
    assert user.created_at is not None

    update_status_by_user_id(user.id, CommonStatus.INIT)

    user = get_user_by_id(user.id)
    assert user.status == CommonStatus.INIT

    delete_user(user.id)
    user = get_user_by_id(user.id)
    assert user.status == CommonStatus.DELETED

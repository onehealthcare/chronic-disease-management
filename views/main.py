from typing import List

import simplejson
from flask import Blueprint, g, request
from models.init_db import db
from models.user_sys import (
    DuplicatedUserNameError,
    UserDTO,
    UserNotFoundException,
    create_user,
    delete_user,
    get_user_by_id,
    paged_get_user_list,
    rename_user,
    update_user_ident,
)
from utils.cursor import get_next_cursor
from utils.logging import file_logger as _logger
from views.common import ApiError
from views.dumps.dump_user import dump_user, dump_users
from views.middleware.auth import need_admin, need_login
from views.render import error, ok


app = Blueprint('main_app', __name__)
logger = _logger('views.main')


@app.route('/')
def hello_world():
    return ok('hello world')


@app.route('/users/')
@need_admin
def paged_users():
    pager = g.pager
    users: List[UserDTO] = paged_get_user_list(pager.cursor, pager.size)

    next_cursor: str = ''
    users, next_cursor = get_next_cursor(users, pager.size)
    return ok({'users': dump_users(users), 'next_cursor': next_cursor})


def _get_user():
    try:
        user_id = int(request.args.get('user_id'))
    except ValueError:
        return ok('用户 ID 格式错误')

    if not user_id:
        return ok('用户ID不应该为空')

    try:
        user: UserDTO = get_user_by_id(user_id)
    except UserNotFoundException as e:
        msg: str = f'{e.message}: {user_id}'
        logger.error(msg)
        return error(msg)

    return ok(dump_user(user))


@need_login
def _new_user():
    data = request.get_json()
    logger.info(f"create_user,request,{simplejson.dumps(data)}")
    name: str = data.get('name', '')
    if not name:
        return error("name is required")

    ident: str = data.get('ident', '')
    try:
        user = create_user(name=name, ident=ident)
    except DuplicatedUserNameError as e:
        logger.warn(f"create_user,duplicated_user_name,{simplejson.dumps(data)}")
        return error(e.message, 500)

    logger.info(f"create_user,ok,{simplejson.dumps(data)}")
    return ok(dump_user(user))


@need_login
def _update_user():
    data = request.get_json()
    logger.info(f"update_user,request,{simplejson.dumps(data)}")
    data = request.get_json()
    try:
        user_id: int = int(data.get('user_id', '0'))
    except ValueError:
        return error('用户 ID 格式错误')

    if user_id != g.me.id and not g.me.is_admin():
        logger.warn(f"update_user,access_denied,{simplejson.dumps(data)}")
        return error(ApiError.access_denied, 403)

    user_name: str = data.get('user_name', '')

    if not user_id:
        return error("user_id is required")

    if not user_name:
        return error("name is required")

    with db.atomic() as transaction:
        try:
            rename_user(user_id=user_id, user_name=user_name)
        except DuplicatedUserNameError as e:
            logger.warn(f"update_user,dumplicated_user_name,{simplejson.dumps(data)}")
            return error(e.message)
        except UserNotFoundException as e:
            logger.warn(f"update_user,user_not_found,{simplejson.dumps(data)}")
            return error(e.message)

        user_ident: str = data.get('user_ident', '')
        if user_ident:
            try:
                update_user_ident(user_id=user_id, user_ident=user_ident)
            except UserNotFoundException as e:
                logger.warn(f"update_user,user_not_found,{simplejson.dumps(data)}")
                transaction.rollback()
                return error(e.message)

    logger.info(f"update_user,ok,{simplejson.dumps(data)}")
    user = get_user_by_id(user_id=user_id)
    return ok(dump_user(user))


@need_admin
def _delete_user():
    data = request.get_json()
    logger.info(f"delete_user,requeset,{simplejson.dumps(data)}")
    data = request.get_json()
    try:
        user_id: int = int(data.get('user_id', '0'))
    except ValueError:
        return error('用户 ID 格式错误')

    if not g.me.is_admin() or g.me.id == user_id:
        logger.warn(f"delete_user,access_denied,{simplejson.dumps(data)}")
        return error(ApiError.access_denied, 403)

    if not user_id:
        return error("user_id is required")

    try:
        delete_user(user_id=user_id)
    except UserNotFoundException as e:
        logger.warn(f"delete_user,user_not_found,{simplejson.dumps(data)}")
        return error(e.message)

    logger.info(f"update_user,ok,{simplejson.dumps(data)}")
    return ok()


@app.route('/user/', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def _user():
    if request.method == "GET":
        return _get_user()

    elif request.method == "POST":
        return _new_user()

    elif request.method == "PATCH":
        return _update_user()

    elif request.method == "DELETE":
        return _delete_user()


@app.route('/update_user/', methods=['POST'])
def update_user():
    return _update_user()


@app.route('/ping')
def ping():
    return 'ok'

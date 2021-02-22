import os
from typing import List

import peewee
import simplejson
from flask import Blueprint, g, request
from models.user_sys import (
    UserDTO,
    UserNotFoundException,
    create_user,
    get_user_by_id,
    paged_get_user_list,
)
from utils.cursor import get_next_cursor
from utils.logging import logger as _logger
from views.dumps.dump_user import dump_users
from views.middleware.auth import need_admin, need_login
from views.render import error, ok


app = Blueprint('main_app', __name__)
logger = _logger('views.main')


@app.route('/')
@need_login
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


@app.route('/user/<int:user_id>/')
@need_admin
def query_user(user_id):
    msg: str = ""

    if not user_id:
        return ok('hello world')

    try:
        user: UserDTO = get_user_by_id(user_id)
    except UserNotFoundException:
        msg = f'user not found: user_id: {user_id}'
        logger.error(msg)
        return error(msg)

    logger.info(f"query_user,ok,{user.json()}")
    return ok(f'Hello World!{os.getpid()}: {user.name}')


@app.route('/user/', methods=['POST'])
def _create_user():
    data = request.get_json()
    logger.info(f"create_user,requeset,{simplejson.dumps(data)}")
    name: str = data.get('name', '')
    if not name:
        return error("name is required")

    ident: str = data.get('ident', '')
    try:
        user = create_user(name=name, ident=ident)
    except peewee.IntegrityError:
        return error('存在同名用户', 500)
    return ok(content=user.dict())


@app.route('/ping')
def ping():
    return 'ok'

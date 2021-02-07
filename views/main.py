import os

from flask import Blueprint, request
from models.user_sys import UserDTO, UserNotFoundException, get_user_by_id
from utils import logger
from views.render import error, ok


app = Blueprint('main_app', __name__)
logger = logger('views.main')


@app.route('/')
def hello_world():
    _user_id: str = request.args.get('user_id', '')
    if not _user_id:
        return ok('hello world')

    try:
        user_id: int = int(_user_id)
    except (ValueError, TypeError):
        logger.error('user_id is not valid')
        return error("user_id is not valid")

    try:
        user: UserDTO = get_user_by_id(user_id)
    except UserNotFoundException:
        logger.error('user not found: user_id: {user_id}')
        return error(f'user not found: user_id: {user_id}')

    logger.info(f"home page,ok,{user.json()}")
    return ok(f'Hello World!{os.getpid()}: {user.name}')


@app.route('/ping')
def ping():
    return 'ok'

import os

from flask import Blueprint
from models.user_sys import UserDTO, UserNotFoundException, get_user_by_id
from views.render import error, ok


app = Blueprint('main_app', __name__)


@app.route('/')
def hello_world():
    try:
        user_id = 1
        user: UserDTO = get_user_by_id(user_id)
    except UserNotFoundException:
        return error(f'user not found: user_id: {user_id}')
    return ok(f'Hello World!{os.getpid()}: {user.name}')


@app.route('/ping')
def ping():
    return 'ok'

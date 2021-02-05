import os
from flask import Flask
from models.user_sys import get_user_by_id, UserDTO, UserNotFoundException

app = Flask(__name__)


@app.route('/')
def hello_world():
    try:
        user: UserDTO = get_user_by_id(1)
    except UserNotFoundException:
        return 'user not found 1'
    return f'Hello World!{os.getpid()}: {user.name}'


@app.route('/ping')
def ping():
    return 'ok'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)

from flask import Blueprint, request
from models.init_db import wxapp
from utils import logger as _logger
from views.render import error, ok


app = Blueprint('account', __name__, url_prefix="/account")
logger = _logger('views.account')


@app.route('/login_via_wxapp/', methods=['POST'])
def login_via_wxapp():
    code: str = request.get_json().get('code', '')

    if not code:
        return error('code invalid')

    data = wxapp.code_to_session(code)

    return ok(data)

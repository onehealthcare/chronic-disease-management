from flask import Blueprint, request
from models.init_db import wxapp_client
from utils import logger as _logger
from views.common import ApiError
from views.render import error, ok


app = Blueprint('account', __name__, url_prefix="/account")
logger = _logger('views.account')


@app.route('/wxapp/login/', methods=['POST'])
def login_via_wxapp():
    code: str = request.get_json().get('code', '')

    if not code:
        return error(ApiError.invalid_wxapp_cod)

    data = wxapp_client.code_to_session(code)

    return ok(data)

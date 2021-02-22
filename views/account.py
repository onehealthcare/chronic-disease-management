from typing import Dict

import simplejson
from flask import Blueprint, request
from metaclass.wxapp.session import Code2SessionData
from models.token import decode_jwt, get_jwt, is_token_valid
from models.user_sys import (
    UserAuthProvider,
    UserDTO,
    UserNotFoundException,
    create_oauth_user,
    get_user_by_id,
    get_user_by_third_party_id,
)
from models.wxapp import InvalidAuthCodeError, code_to_session
from utils import logger as _logger
from views.common import ApiError
from views.dumps.dump_account import dump_account
from views.render import error, ok


app = Blueprint('account', __name__, url_prefix="/account")
logger = _logger('views.account')


@app.route('/wxapp/login/', methods=['POST'])
def login_via_wxapp():
    code: str = request.get_json().get('code', '')
    user_name: str = request.get_json().get('user_name', '')

    if not code:
        return error(ApiError.invalid_wxapp_code)

    try:
        data: Code2SessionData = code_to_session(code)
    except InvalidAuthCodeError:
        return error(ApiError.invalid_wxapp_code)

    third_party_id: str = data.get('open_id', '')
    user: UserDTO
    try:
        user = get_user_by_third_party_id(third_party_id=third_party_id,
                                          provider=UserAuthProvider.WXAPP)
    except UserNotFoundException:
        detail: Dict[str, str] = {'session_key': data.get('session_key', '')}
        user = create_oauth_user(name=user_name, ident='',
                                 third_party_id=third_party_id,
                                 provider=UserAuthProvider.WXAPP,
                                 detail_json=simplejson.dumps(detail))

    access_token, refresh_token = get_jwt(user_id=user.id, user_name=user.name)

    return ok(dump_account(user, access_token, refresh_token))


@app.route('/refresh_token/', methods=['POST'])
def refresh_token():
    refresh_token: str = request.get_json().get('refresh_token', '')
    if not refresh_token:
        return error(ApiError.invalid_token)

    if not is_token_valid(refresh_token):
        return error(ApiError.invalid_token)

    data = decode_jwt(refresh_token)
    user_id = data.get('user_id')
    try:
        user = get_user_by_id(user_id)
    except UserNotFoundException:
        return error(ApiError.invalid_token)

    access_token, refresh_token = get_jwt(user_id=user.id, user_name=user.name)
    return ok(dump_account(user, access_token, refresh_token))
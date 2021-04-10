import base64

import sentry_sdk
from config import DEBUG, SENTRY_DSN
from flask import Flask, g, request, url_for
from metaclass.cursor import Pager
from models.init_db import db
from models.token import InvalidTokenError, decode_jwt
from models.user_sys import get_user_by_id
from sentry_sdk.integrations.flask import FlaskIntegration
from utils.crypto import hmac_sha1_encode
from views.account import app as account_app
from views.auth import app as auth_app
from views.chronic_condition import app as chronic_condition_app
from views.common import ApiError
from views.main import app as main_app
from views.render import error


sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)


@app.errorhandler(500)
def handle_500(e):
    original = str(getattr(e, "original_exception", e))
    return error(error=original, status_code=500)


@app.errorhandler(404)
def handle_404(e):
    return error(error='Not Found', status_code=404)


@app.before_request
def before_request():
    # api sign
    if request.method == 'GET':
        data = request.args
    else:
        data = request.json

    if not DEBUG:
        if request.path != url_for('main_app.ping'):
            if 'sign' not in data or hmac_sha1_encode(data) != data.get('sign'):
                return error(ApiError.invalid_api_sign)

    # db conn
    if db.is_closed():
        db.connect()

    # set g.me
    g.me = None

    access_token = request.headers.get('Auth', '')
    if access_token:
        try:
            jwt_data = decode_jwt(access_token)
            user_id: int = jwt_data.get('user_id', 0)
            if user_id:
                g.me = get_user_by_id(user_id)

        except InvalidTokenError:
            pass

    # pager
    if request.method == 'GET':
        size: int = 20
        cursor: int = 0

        _cursor: str = data.get('cursor', '')
        try:
            cursor = int(base64.b64decode(_cursor))
        except ValueError:
            pass
        except TypeError:
            return error(ApiError.invalid_cursor)

        try:
            size = int(request.args.get('size', 20))
        except (ValueError, TypeError):
            pass

        g.pager = Pager(cursor=cursor, size=size)


@app.teardown_request
def close(e):
    if not db.is_closed():
        db.close()


app.register_blueprint(main_app)
app.register_blueprint(account_app)
app.register_blueprint(auth_app)
app.register_blueprint(chronic_condition_app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8079, debug=DEBUG)

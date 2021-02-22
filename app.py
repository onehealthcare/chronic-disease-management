import sentry_sdk
from config import DEBUG, SENTRY_DSN
from flask import Flask, g, request
from models.init_db import db
from models.token import InvalidTokenError, decode_jwt
from models.user_sys import get_user_by_id
from sentry_sdk.integrations.flask import FlaskIntegration
from views.account import app as account_app
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
    # db conn
    if db.is_closed():
        db.connect()

    # set g.me
    g.me = None

    access_token = request.headers.get('Auth', '')
    if access_token:
        try:
            data = decode_jwt(access_token)
        except InvalidTokenError:
            pass

        user_id: int = data.get('user_id', 0)
        if user_id:
            g.me = get_user_by_id(user_id)


@app.teardown_request
def close(e):
    if not db.is_closed():
        db.close()


app.register_blueprint(main_app)
app.register_blueprint(account_app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8079, debug=DEBUG)

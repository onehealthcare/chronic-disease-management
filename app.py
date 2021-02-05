import sentry_sdk
from config import DEBUG, SENTRY_DSN
from flask import Flask
from models.init_db import db
from sentry_sdk.integrations.flask import FlaskIntegration
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
def conn():
    if db.is_closed():
        db.connect()


@app.teardown_request
def close(e):
    if not db.is_closed():
        db.close()


app.register_blueprint(main_app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=DEBUG)

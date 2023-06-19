from flask import Blueprint
from router.auth.oauth import app as oauth_app
from router.main import app as main_app


app = Blueprint('router', __name__)
app.register_blueprint(main_app)  # type: ignore
app.register_blueprint(oauth_app)  # type: ignore

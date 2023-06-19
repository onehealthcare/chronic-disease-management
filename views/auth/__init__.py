from flask import Blueprint
from views.auth.account import app as account_app
from views.auth.auth import app as auth_app
from views.auth.oauth import app as oauth_app
from views.auth.user import app as user_app


app = Blueprint("auth", __name__)
app.register_blueprint(account_app)  # type: ignore
app.register_blueprint(auth_app)  # type: ignore
app.register_blueprint(oauth_app)  # type: ignore
app.register_blueprint(user_app)  # type: ignore

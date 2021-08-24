from flask import Blueprint, request
from utils import logger as _logger
from broker.tower_sys import save_access_token

app = Blueprint("tower", __name__, url_prefix="/tower")

logger = _logger("views.tower")


@app.route("/oauth_callback")
def tower_oauth_callback():
    logger.info(request.args.to_dict())
    auth_code: str = request.args.get("code")
    user_id: int = int(request.args.get("user_id"))
    access_token: str = save_access_token(auth_code=auth_code, user_id=user_id)
    return f"ok, auth_code: {auth_code}, access_token: {access_token}"

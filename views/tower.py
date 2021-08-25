from broker.tower_sys import save_access_token
from flask import Blueprint, request
from models.tower_sys import TodoPayloadModel
from pydantic import ValidationError
from utils import logger as _logger


app = Blueprint("tower", __name__, url_prefix="/tower")

logger = _logger("views.tower")


@app.route("/oauth_callback")
def tower_oauth_callback():
    logger.info(request.args.to_dict())
    auth_code: str = request.args.get("code")
    user_id: int = int(request.args.get("user_id"))
    access_token: str = save_access_token(auth_code=auth_code, user_id=user_id)
    return f"ok, auth_code: {auth_code}, access_token: {access_token}"


@app.route("/user/<user_id>/webhook", methods=["POST"])
def tower_webhook_handler(user_id):
    if request.is_json:
        data = request.json
        logger.info(f"tower_webhook,request,{user_id} - {data}")
        try:
            model: TodoPayloadModel = TodoPayloadModel.parse_obj(data)
            todo_id: str = model.data.todo.guid
            todo_id
        except ValidationError:
            logger.error(f"tower_webhook,invalid payload,{user_id} - {data}")

    return "ok"

import simplejson
from broker.notion_sys import update_notion_task_by_tower_todo_id
from broker.tower_sys import save_access_token
from flask import Blueprint, redirect, request
from models.tower_sys import TodoPayloadModel, get_auth_url
from pydantic import ValidationError
from utils import logger as _logger


app = Blueprint("tower", __name__, url_prefix="/tower")

logger = _logger("views.tower")


@app.route("/user/<user_id>/login")
def tower_login(user_id):
    return redirect(location=get_auth_url(user_id=user_id))


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
            if model.action != "deleted":
                todo_id: str = model.data.todo.guid
                update_notion_task_by_tower_todo_id(todo_id=todo_id, user_id=int(user_id))
            else:
                logger.info(f"tower_webhook,request,{user_id} - ignore delete action - {data}")
        except ValidationError as e:
            error_data = {'error': str(e)}
            logger.error(f"tower_webhook,invalid payload,{user_id} - {data} - {simplejson.dumps(error_data)}")

    return "ok"

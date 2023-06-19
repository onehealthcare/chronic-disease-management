import datetime

from flask import Blueprint, request
from libs.strava import StatusError as StravaStatusError, TokenResp
from models.init_db import db, strava_client
from models.user_sys import (
    UserAuthNotFoundException,
    UserAuthProvider,
    UserDTO,
    get_or_create_oauth_user,
    update_user_auth_by_user_id_and_provider,
)
from views.render import ok


app = Blueprint('oauth', __name__, url_prefix="/oauth")


@app.route('/strava/exchange_token')
def oauth_strava_exchange_token():
    code: str = request.args.get("code", "")
    if not code:
        return "code is empty"
    try:
        resp: TokenResp = strava_client.get_token_by_code(code=code)
    except StravaStatusError as e:
        return e.message

    with db.atomic() as txn:
        provider = UserAuthProvider.STRAVA
        user: UserDTO = get_or_create_oauth_user(
            name=f"{resp.athlete.firstname} {resp.athlete.lastname}",
            ident="", third_party_id=str(resp.athlete.id),
            provider=provider, detail_json=resp.athlete.json()
        )
        try:
            update_user_auth_by_user_id_and_provider(
                user_id=user.id, provider=provider,
                access_token=resp.access_token,
                refresh_token=resp.refresh_token,
                expires_date=datetime.datetime.now() + datetime.timedelta(seconds=resp.expires_at)
            )
        except UserAuthNotFoundException:
            txn.rollback()

    return ok({"code": code, "user_id": user.id})

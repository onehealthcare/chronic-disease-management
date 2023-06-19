from config import HOST
from flask import Blueprint, redirect, url_for
from models.init_db import strava_client


app = Blueprint("router_main", __name__)


@app.route('/oauth/strava/')
def oauth_strava():
    redirect_url = f"{HOST}{url_for('auth.oauth.oauth_strava_exchange_token')}"
    url = strava_client.get_oauth_url(redirect_url=redirect_url)
    return redirect(url)

import requests
from libs.strava.dto import StatusError, TokenResp
from utils.logging import logger


log = logger('lib.strava')


class StravaClient:
    def __init__(self, client_id: int, client_secret: str):
        self.host = "https://www.strava.com"
        self.oauth_uri = "/oauth/authorize"
        self.client_id = client_id
        self.client_secret = client_secret

    def get_oauth_url(self, redirect_url: str) -> str:
        return f"{self.host}{self.oauth_uri}?client_id={self.client_id}&response_type=code&redirect_uri={redirect_url}&approval_prompt=force&scope=activity:read"

    def _post(self, url, data) -> dict:
        resp = requests.post(url, data=data)
        if resp.status_code == requests.codes['ok']:
            return resp.json()
        else:
            body: str = resp.text
            log.error(f"post,status_error,{resp.status_code},{body}")
            raise StatusError(resp.status_code, body)

    def get_token_by_code(self, code: str) -> TokenResp:
        url = f"{self.host}/oauth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
        }
        resp = self._post(url, data=data)
        return TokenResp.parse_obj(resp)

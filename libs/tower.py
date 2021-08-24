import requests
from typing import Dict


class TowerClient:
    def __init__(self, client_id: str, secret_key: str):
        self.client_id = client_id
        self.secret_key = secret_key
        self.api_host = "https://tower.im/api/v1/"
        self.auth_host = "https://tower.im/oauth/token"
        self._session = None

    @property
    def connection(self):
        if not self._session:
            self._session = requests.Session()

        return self._session

    def get(self, url: str, headers: Dict):
        pass

    def post(self, url: str, data: Dict, headers: Dict={}):
        r = self.connection.post(url=url, data=data, headers=headers)
        if r.status_code != requests.codes.ok:
            return None

        return r

    def get_access_token_by_auth_code(self, auth_code: str, redirect_uri: str):
        data: Dict = {
            "client_id": self.client_id,
            "client_secret": self.secret_key,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        r = self.post(url=self.auth_host, data=data)
        if not r:
            return {}

        return r.json()

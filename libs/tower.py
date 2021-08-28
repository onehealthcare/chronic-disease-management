from typing import Dict

import requests


class TowerClient:
    def __init__(self, client_id: str, secret_key: str):
        self.client_id = client_id
        self.secret_key = secret_key
        self.api_host = "https://tower.im"
        self.api_url = f"{self.api_host}/api/v1/"
        self.auth_url = f"{self.api_host}/oauth/token"
        self.auth_code_url = f"{self.api_host}/oauth/authorize"
        self._session = None

    @property
    def connection(self):
        if not self._session:
            self._session = requests.Session()

        return self._session

    def get(self, url: str, headers: Dict):
        r = self.connection.get(url=url, headers=headers)
        if r.status_code != requests.codes.ok:
            return None

        return r

    def post(self, url: str, data: Dict, headers: Dict = {}):
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
        r = self.post(url=self.auth_url, data=data)
        if not r:
            return {}

        return r.json()

    def refresh_access_token(self, access_token: str, refresh_token: str, redirect_uri: str):
        data: Dict = {
            "client_id": self.client_id,
            "client_secret": self.secret_key,
            "grant_type": "refresh_token",
            "redirect_uri": redirect_uri,
            "refresh_token": refresh_token
        }
        headers: Dict[str, str] = {"Authorization": f"Bearer {access_token}"}
        r = self.post(url=self.auth_url, data=data, headers=headers)
        if not r:
            return {}

        return r.json()

    def get_todo(self, todo_id: str, access_token: str):
        headers: Dict[str, str] = {"Authorization": f"Bearer {access_token}"}
        url: str = f"{self.api_url}/todos/{todo_id}"
        r = self.get(url=url, headers=headers)
        if not r:
            return {}

        return r.json()

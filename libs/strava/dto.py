import datetime
from typing import Optional

from pydantic import BaseModel


class Athlete(BaseModel):
    """
    {
        "id": 11258832,
        "username": null,
        "resource_state": 2,
        "firstname": "tonghs",
        "lastname": "t",
        "bio": "",
        "city": "Beijing",
        "state": "Beijing",
        "country": "中国",
        "sex": "M",
        "premium": true,
        "summit": true,
        "created_at": "2015-09-09T00:15:59Z",
        "updated_at": "2023-06-02T04:52:29Z",
        "badge_type_id": 1,
        "weight": 82.4,
        "profile_medium": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/11258832/3434458/3/medium.jpg",
        "profile": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/11258832/3434458/3/large.jpg",
        "friend": null,
        "follower": null
    }
    """
    id: int
    username: Optional[str]
    resource_state: int
    firstname: str
    lastname: str
    bio: str
    city: str
    state: str
    country: str
    sex: str
    premium: bool
    summit: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    badge_type_id: int
    weight: float
    profile_medium: str
    profile: str


class TokenResp(BaseModel):
    """
    {
        "token_type": "Bearer",
        "expires_at": 1686843689,
        "expires_in": 21600,
        "refresh_token": "428c8edfcb284850e4b0c18b059175e826366ba0",
        "access_token": "d3378d7fa5e06d95252140e94d2b70f634bb315a",
        "athlete": {
            "id": 11258832,
            "username": null,
            "resource_state": 2,
            "firstname": "tonghs",
            "lastname": "t",
            "bio": "",
            "city": "Beijing",
            "state": "Beijing",
            "country": "中国",
            "sex": "M",
            "premium": true,
            "summit": true,
            "created_at": "2015-09-09T00:15:59Z",
            "updated_at": "2023-06-02T04:52:29Z",
            "badge_type_id": 1,
            "weight": 82.4,
            "profile_medium": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/11258832/3434458/3/medium.jpg",
            "profile": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/11258832/3434458/3/large.jpg",
            "friend": null,
            "follower": null
        }
    }
    """

    token_type: str
    expires_at: int
    expires_in: int
    refresh_token: str
    access_token: str
    athlete: Athlete


class StatusError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"StatusError: {self.status_code} {self.message}"

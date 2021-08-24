import datetime
from typing import Dict

import simplejson
from pydantic import BaseModel
from utils.datetime_utils import _datetime


class UserAuthDTO(BaseModel):
    id: int
    user_id: int
    third_party_id: str
    provider: int
    access_token: str
    refresh_token: str
    expires_date: datetime.datetime
    detail_json: Dict
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao):
        return UserAuthDTO(
            id=dao.id,
            user_id=dao.user_id,
            third_party_id=dao.third_party_id,
            provider=dao.provider,
            access_token=dao.access_token,
            refresh_token=dao.refresh_token,
            expires_date=dao.expires_date,
            detail_json=simplejson.loads(dao.detail_json),
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )

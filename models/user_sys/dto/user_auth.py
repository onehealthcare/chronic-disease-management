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
            detail_json=simplejson.loads(dao.detail_json),
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )

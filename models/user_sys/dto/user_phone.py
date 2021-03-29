import datetime

from pydantic import BaseModel
from utils.datetime_utils import _datetime


class UserPhoneDTO(BaseModel):
    id: int
    user_id: int
    phone: str
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao):
        return UserPhoneDTO(
            id=dao.id,
            user_id=dao.user_id,
            phone=dao.phone,
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )

import datetime

from pydantic import BaseModel
from utils.datetime_utils import _datetime


class MetricDTO(BaseModel):
    id: int
    name: str
    text: str
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao) -> 'MetricDTO':
        return MetricDTO(
            id=dao.id,
            name=dao.name,
            text=dao.text,
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )


class UserMetricDTO(BaseModel):
    id: int
    user_id: int
    metric_id: int
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao) -> 'UserMetricDTO':
        return UserMetricDTO(
            id=dao.id,
            user_id=dao.user_id,
            metric_id=dao.metric_id,
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )

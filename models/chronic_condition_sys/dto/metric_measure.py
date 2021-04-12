import datetime

from pydantic import BaseModel
from utils.datetime_utils import _datetime


class MetricMeasureDTO(BaseModel):
    id: int
    user_id: int
    metric_id: int
    metric_label: str
    value: float
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao) -> 'MetricMeasureDTO':
        return cls(
            id=dao.id,
            user_id=dao.user_id,
            metric_id=dao.metric_id,
            metric_label=dao.metric_label,
            value=dao.value,
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )

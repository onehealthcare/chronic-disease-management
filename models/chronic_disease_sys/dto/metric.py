import datetime
from typing import Optional

from pydantic import BaseModel
from utils.datetime_utils import _datetime


class MetricDTO(BaseModel):
    id: int
    name: str
    text: str
    unit: str
    ref_value: Optional[float]
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao) -> 'MetricDTO':
        return MetricDTO(
            id=dao.id,
            name=dao.name,
            text=dao.text,
            unit=dao.unit,
            ref_value=dao.ref_value,
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )


class UserMetricDTO(BaseModel):
    id: int
    user_id: int
    metric_id: int
    metric: MetricDTO
    chart_type: str
    ref_value: Optional[float]
    default_selected: int
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao) -> 'UserMetricDTO':
        return UserMetricDTO(
            id=dao.id,
            user_id=dao.user_id,
            metric_id=dao.metric_id,
            chart_type=dao.chart_type,
            ref_value=dao.ref_value,
            default_selected=dao.default_selected,
            metric=MetricDTO.from_dao(dao.metric),
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )


class MetricLabelDTO(BaseModel):
    id: int
    metric_id: int
    order: int
    name: str
    text: str
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao) -> 'MetricLabelDTO':
        return MetricLabelDTO(
            id=dao.id,
            metric_id=dao.metric_id,
            order=dao.order,
            name=dao.name,
            text=dao.text,
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )

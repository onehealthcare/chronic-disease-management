import datetime
from typing import List

from models.base import Base
from models.const import CommonStatus
from peewee import CharField, DateTimeField, FloatField, IntegerField


class MetricMeasureDAO(Base):
    """
    测量值
    """
    user_id = IntegerField(index=True)
    metric_id = IntegerField(index=True)
    metric_label = CharField(index=True)
    value = FloatField()
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "chronic_condition_metric_measure"

    @classmethod
    def query_recent_by_metric(cls, user_id: int, metric_id: int, limit: int) -> List['MetricMeasureDAO']:
        q = cls.select().where(
            cls.user_id == user_id,
            cls.metric_id == metric_id,
            cls.status == CommonStatus.NORMAL
        ).order_by(cls.created_at.desc()).limit(limit)

        return list(sorted([o for o in q], key=lambda dao: dao.created_at, reverse=True))

    @classmethod
    def query_recent_by_metric_and_time(cls, user_id: int, metric_id: int, time: datetime.datetime) -> List['MetricMeasureDAO']:
        return cls.select().where(
            cls.user_id == user_id,
            cls.metric_id == metric_id,
            cls.status == CommonStatus.NORMAL,
            cls.created_at >= time
        )

    @classmethod
    def get_by_id(cls, measure_id: int) -> 'MetricMeasureDAO':
        return cls.get(cls.id == measure_id)

    def update_status(self, status: int):
        self.status = status
        self.save()

    def delete(self):
        self.update_status(status=CommonStatus.DELETED)

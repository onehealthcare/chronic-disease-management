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
    metric_label = CharField(index=True, default="")
    value = FloatField()
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "chronic_disease_metric_measure"

    @classmethod
    def query_recent_by_metric(cls, user_id: int, metric_id: int, size: int) -> List['MetricMeasureDAO']:
        q = cls.select().where(
            cls.user_id == user_id,
            cls.metric_id == metric_id,
            cls.status == CommonStatus.NORMAL
        ).order_by(cls.created_at.desc()).limit(size)

        return list(q)

    @classmethod
    def paged_by_metric(cls, user_id: int, metric_id: int, cursor: int, size: int) -> List['MetricMeasureDAO']:
        q = cls.select().where(
            cls.user_id == user_id,
            cls.metric_id == metric_id,
            cls.status == CommonStatus.NORMAL,
            cls.id >= cursor
        ).order_by(cls.id.desc()).limit(size)

        return list(q)

    @classmethod
    def get_by_id(cls, measure_id: int) -> 'MetricMeasureDAO':
        return cls.get(cls.id == measure_id)

    def update_status(self, status: int):
        self.status = status
        self.save()

    def delete(self):
        self.update_status(status=CommonStatus.DELETED)

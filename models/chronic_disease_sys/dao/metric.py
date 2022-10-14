import datetime
from typing import List

from models.base import Base
from models.const import CommonStatus
from peewee import CharField, DateTimeField, IntegerField


class MetricDAO(Base):
    """
    度量，比如血压/血糖/心率
    """
    name = CharField(index=True)
    text = CharField()
    unit = CharField()
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "chronic_disease_metric"

    @classmethod
    def get_by_id(cls, metric_id: int) -> 'MetricDAO':
        return cls.get(cls.id == metric_id)

    @classmethod
    def get_by_name(cls, name: str) -> 'MetricDAO':
        return cls.get(cls.name == name, cls.status == CommonStatus.NORMAL)

    def update_status(self, status: int):
        self.status = status
        self.save()

    def delete(self):
        self.update_status(status=CommonStatus.DELETED)


class UserMetricDAO(Base):
    """
    用户选择的度量
    """
    user_id = IntegerField(index=True)
    metric_id = IntegerField(index=True)
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "chronic_disease_user_metric"

    @classmethod
    def get_by_id(cls, metric_id: int) -> 'UserMetricDAO':
        return cls.get(cls.id == metric_id)

    @classmethod
    def query_by_user_id(cls, user_id: int) -> List['UserMetricDAO']:
        return cls.select().where(cls.user_id == user_id, cls.status == CommonStatus.NORMAL)

    @classmethod
    def query_by_metric_id(cls, metric_id: int) -> List['UserMetricDAO']:
        return cls.select().where(cls.metric_id == metric_id, cls.status == CommonStatus.NORMAL)

    @property
    def metric(self):
        metric_id: int = self.id
        return MetricDAO.get_by_id(metric_id=metric_id)

    def update_status(self, status: int):
        self.status = status
        self.save()

    def delete(self):
        self.update_status(status=CommonStatus.DELETED)


class MetricLabelDAO(Base):
    """
    度量标签，比如血压有舒张压和收缩压，血糖有餐前餐后等
    """
    name = CharField(index=True)
    text = CharField()
    metric_id = IntegerField(index=True)
    order = IntegerField(index=True)
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "chronic_disease_metric_label"

    @classmethod
    def get_by_id(cls, metric_label_id: int) -> 'MetricLabelDAO':
        return cls.get(cls.id == metric_label_id)

    @classmethod
    def get_by_name(cls, metric_id: int, name: str) -> 'MetricLabelDAO':
        return cls.get(cls.name == name, cls.status == CommonStatus.NORMAL)

    @classmethod
    def query_by_metric_id(cls, metric_id: int) -> List['MetricLabelDAO']:
        return cls.select().where(cls.metric_id == metric_id, cls.status == CommonStatus.NORMAL).order_by(cls.order.asc())

    def update_status(self, status: int):
        self.status = status
        self.save()

    def delete(self):
        self.update_status(status=CommonStatus.DELETED)

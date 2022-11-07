import datetime
from typing import List, Optional

from models.base import Base
from models.chronic_disease_sys.const import ChartType
from models.const import CommonStatus
from models.init_db import db
from peewee import CharField, DateTimeField, FloatField, IntegerField


class MetricDAO(Base):
    """
    度量，比如血压/血糖/心率
    """
    name = CharField(index=True)
    text = CharField()
    unit = CharField()
    ref_value = FloatField()  # 推荐的参考值
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

    @classmethod
    def get_all(cls):
        return cls.select().where(cls.status == CommonStatus.NORMAL)

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
    chart_type = CharField(default=ChartType.COLUMN.value)
    ref_value = FloatField()  # 用户自定义的参考值
    default_selected = IntegerField(default=0)  # 是否默认选中
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "chronic_disease_user_metric"

    @classmethod
    def create(cls, user_id: int, metric_id: int, ref_value: Optional[float] = None) -> 'UserMetricDAO':
        dao = cls.get(cls.user_id == user_id, cls.metric_id == metric_id)
        if not dao:
            dao = cls(user_id=user_id, metric_id=metric_id, ref_value=ref_value)
            dao.save()
        elif dao.status != CommonStatus.NORMAL:
            dao.update_status(status=CommonStatus.NORMAL)

        return dao

    @classmethod
    def get_by_id(cls, metric_id: int) -> 'UserMetricDAO':
        return cls.get(cls.id == metric_id)

    @classmethod
    @db.atomic()
    def set_default_selected(cls, user_id: int, metric_id: int):
        cls.update(default_selected=0).where(cls.user_id == user_id, cls.default_selected == 1).execute()
        cls.update(default_selected=1).where(cls.user_id == user_id, cls.metric_id == metric_id, cls.status == CommonStatus.NORMAL).execute()

    @classmethod
    def get_by_user_id_metric_id(cls, user_id: int, metric_id: int) -> "UserMetricDAO":
        return cls.get(cls.user_id == user_id, cls.metric_id == metric_id, cls.status == CommonStatus.NORMAL)

    @classmethod
    def set_ref_value(cls, user_id: int, metric_id: int, ref_value: float):
        dao = cls.get_by_user_id_metric_id(user_id=user_id, metric_id=metric_id)
        if dao:
            dao.ref_value = ref_value
            dao.save()

    @classmethod
    def query_by_user_id(cls, user_id: int) -> List['UserMetricDAO']:
        return cls.select().where(cls.user_id == user_id, cls.status == CommonStatus.NORMAL)

    @classmethod
    def query_by_metric_id(cls, metric_id: int) -> List['UserMetricDAO']:
        return cls.select().where(cls.metric_id == metric_id, cls.status == CommonStatus.NORMAL)

    @property
    def metric(self):
        metric_id: int = self.metric_id
        return MetricDAO.get_by_id(metric_id=metric_id)

    def update_status(self, status: int):
        self.status = status
        self.save()

    def delete(self):
        self.update_status(status=CommonStatus.DELETED)

    @classmethod
    def set_chart_type(cls, user_id: int, metric_id: int, chart_type: str):
        dao = cls.get(cls.user_id == user_id, cls.metric_id == metric_id)
        if dao:
            dao.chart_type = chart_type
            dao.save()


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

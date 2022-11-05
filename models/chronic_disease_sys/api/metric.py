from typing import Dict, List, Optional

from models.chronic_disease_sys.const import ChartType
from models.chronic_disease_sys.dao.metric import (
    MetricDAO,
    MetricLabelDAO,
    UserMetricDAO,
)
from models.chronic_disease_sys.dto.metric import (
    MetricDTO,
    MetricLabelDTO,
    UserMetricDTO,
)
from models.chronic_disease_sys.exceptions import (
    DuplicatedMetricException,
    MetricLabelNotFoundException,
    MetricNotFoundException,
)
from models.const import CommonStatus
from models.init_db import db


def create_metric(name: str, text: str, unit: str, ref_value: Optional[float] = None) -> MetricDTO:
    dao = MetricDAO.get_by_name(name=name)
    if dao:
        raise DuplicatedMetricException()
    dao = MetricDAO.create(name=name, text=text, unit=unit, ref_value=ref_value)
    return MetricDTO.from_dao(dao)


def get_metric(metric_id: int) -> MetricDTO:
    dao = MetricDAO.get_by_id(metric_id=metric_id)
    if not dao or dao.status == CommonStatus.DELETED:
        raise MetricNotFoundException()

    return MetricDTO.from_dao(dao)


def get_all_metrics() -> List[MetricDTO]:
    daos = MetricDAO.get_all()
    return [MetricDTO.from_dao(dao) for dao in daos]


def get_metric_by_name(name: str) -> MetricDTO:
    dao = MetricDAO.get_by_name(name=name)
    if not dao:
        raise MetricNotFoundException()

    return MetricDTO.from_dao(dao)


@db.atomic()
def delete_metric(metric_id: int):
    dao = MetricDAO.get_by_id(metric_id=metric_id)
    if not dao:
        raise MetricNotFoundException()

    dao.delete()

    for um_dao in UserMetricDAO.query_by_metric_id(metric_id=metric_id):
        um_dao.delete()

    for ml_dao in MetricLabelDAO.query_by_metric_id(metric_id=metric_id):
        ml_dao.delete()


def create_user_metric(user_id: int, metric_id: int) -> UserMetricDTO:
    metric: MetricDTO = get_metric(metric_id=metric_id)
    dao = UserMetricDAO.create_one(user_id=user_id, metric_id=metric_id, ref_value=metric.ref_value)
    return UserMetricDTO.from_dao(dao)


def remove_user_metric(user_id: int, metric_id: int):
    dao = UserMetricDAO.get(
        UserMetricDAO.user_id == user_id,
        UserMetricDAO.metric_id == metric_id,
        UserMetricDAO.status == CommonStatus.NORMAL
    )
    if dao:
        dao.delete()


def set_default_user_metric(user_id: int, metric_id: int):
    """
    设置用户的主要用的指标
    """
    UserMetricDAO.set_default_selected(user_id=user_id, metric_id=metric_id)


def set_user_metric_ref_value(user_id: int, metric_id: int, ref_value: float):
    UserMetricDAO.set_ref_value(user_id=user_id, metric_id=metric_id, ref_value=ref_value)


def query_user_metric_by_user_id(user_id: int) -> List[UserMetricDTO]:
    daos = UserMetricDAO.query_by_user_id(user_id=user_id)
    return [UserMetricDTO.from_dao(dao) for dao in daos]


def set_user_metric_chart_type(user_id: int, metric_id: int, chart_type: str):
    UserMetricDAO.set_chart_type(user_id=user_id, metric_id=metric_id, chart_type=chart_type)


def get_user_metric(user_id: int, metric_id: int) -> Optional[UserMetricDTO]:
    dao = UserMetricDAO.get_by_user_id_metric_id(user_id=user_id, metric_id=metric_id)
    if not dao:
        return None
    return UserMetricDTO.from_dao(dao)


def create_metric_label(metric_id: int, name: str, text: str, order: int = 0) -> MetricLabelDTO:
    dao = get_metric(metric_id=metric_id)
    dao = MetricLabelDAO.create(metric_id=dao.id, name=name, text=text, order=order)
    return MetricLabelDTO.from_dao(dao)


def get_metric_label(metric_id: int, label_name: str) -> MetricLabelDTO:
    dao = MetricLabelDAO.get_by_name(metric_id=metric_id, name=label_name)
    if not dao:
        raise MetricLabelNotFoundException()

    return MetricLabelDTO.from_dao(dao)


def delete_metric_label(metric_label_id: int):
    dao = MetricLabelDAO.get_by_id(metric_label_id=metric_label_id)
    if not dao:
        raise MetricLabelNotFoundException()
    dao.delete()


def query_metric_label_by_metric_id(metric_id: int) -> List[MetricLabelDTO]:
    daos = MetricLabelDAO.query_by_metric_id(metric_id=metric_id)
    return [MetricLabelDTO.from_dao(dao) for dao in daos]


def get_metric_chart_types() -> List[Dict[ChartType, str]]:
    return ChartType.get_all()

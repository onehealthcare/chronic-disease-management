from typing import Dict, List, Optional

from models.chronic_condition_sys import (
    MetricDTO,
    MetricLabelDTO,
    UserMetricDTO,
)


def dump_user_metric(dto: UserMetricDTO) -> Optional[Dict]:
    if not dto:
        return None

    return {
        "user_id": dto.user_id,
        "metric_id": dto.metric_id,
        "metric_name": dto.metric.name,
        "metric_unit": dto.metric.unit,
        "metric_text": dto.metric.text
    }


def dump_user_metrics(dtos: List[UserMetricDTO]) -> List[Dict]:
    if not dtos:
        return []
    return list(filter(None, [dump_user_metric(dto) for dto in dtos]))


def dump_metric(dto: MetricDTO) -> Optional[Dict]:
    if not dto:
        return None

    return {
        "id": dto.id,
        "name": dto.name,
        "text": dto.text
    }


def dump_metric_label(dto: MetricLabelDTO) -> Optional[Dict]:
    if not dto:
        return None

    return {
        "id": dto.id,
        "metric_id": dto.metric_id,
        "name": dto.name,
        "text": dto.text,
        "order": dto.order
    }

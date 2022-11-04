from typing import Dict, List, Optional, Union

from models.chronic_disease_sys import MetricDTO, MetricLabelDTO, UserMetricDTO


def dump_user_metric(dto: UserMetricDTO) -> Optional[Dict]:
    if not dto:
        return None

    return {
        "user_id": dto.user_id,
        "metric_id": dto.metric_id,
        "metric_name": dto.metric.name,
        "metric_unit": dto.metric.unit,
        "metric_text": dto.metric.text,
        "ref_value": dto.ref_value,
        "chart_type": dto.chart_type,
        "default_selected": dto.default_selected
    }


def dump_user_metrics(dtos: List[UserMetricDTO]) -> List[Dict]:
    if not dtos:
        return []
    return list(filter(None, [dump_user_metric(dto) for dto in dtos]))


def dump_metric(dto: MetricDTO) -> Optional[Dict[str, Union[int, str, bool]]]:
    if not dto:
        return None

    return {
        "id": dto.id,
        "name": dto.name,
        "text": dto.text,
        "is_activated": False,
    }


def dump_metrics(dtos: List[MetricDTO], user_metrics: List[UserMetricDTO] = []) -> List[Dict]:
    if not dtos:
        return []

    result = []
    user_metric_ids = [um.metric_id for um in user_metrics]
    for dto in dtos:
        data = dump_metric(dto)
        if not data:
            continue

        if dto.id in user_metric_ids:
            data["is_activated"] = True

        result.append(data)
    return result


def dump_metric_labels(dtos: List[MetricLabelDTO]) -> List[Dict]:
    if not dtos:
        return []

    return list(filter(None, [dump_metric_label(dto) for dto in dtos]))


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

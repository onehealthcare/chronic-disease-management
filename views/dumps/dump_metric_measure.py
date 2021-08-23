from typing import Dict, List, Optional

from models.chronic_condition_sys import MetricMeasureDTO


def dump_metric_measure(dto: MetricMeasureDTO) -> Optional[Dict]:
    if not dto:
        return None

    return {
        "id": dto.id,
        "value": dto.value,
        "created_at": dto.created_at,
        "metric_id": dto.metric_id,
        "metric_label": dto.metric_label
    }


def dump_metric_measures(dtos: List[MetricMeasureDTO]) -> List[Dict]:
    if not dtos:
        return []

    return list(filter(None, [dump_metric_measure(dto) for dto in dtos]))

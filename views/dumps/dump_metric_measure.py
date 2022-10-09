from typing import Dict, List, Optional, Tuple

from models.chronic_disease_sys import MetricMeasureDTO


def _get_color(value: float, ref_value: float) -> str:
    """
    获取指标的颜色
    :param value:
    :param ref_value: 参考值
    :return:
    """
    return "#EE6666" if value > ref_value else "#91CB74"


def dump_metric_measure(dto: MetricMeasureDTO, ref_value: float) -> Optional[Dict]:
    if not dto:
        return None

    return {
        "id": dto.id,
        "value": dto.value,
        "color": _get_color(dto.value, ref_value),
        "created_at": dto.created_at.strftime("%m/%d %H:%M"),
        "metric_id": dto.metric_id,
        "metric_label": dto.metric_label
    }


def dump_metric_measures(dtos: List[MetricMeasureDTO], ref_value: float) -> List[Dict]:
    if not dtos:
        return []

    dtos.sort(key=lambda x: x.created_at)
    return list(filter(None, [dump_metric_measure(dto, ref_value=ref_value) for dto in dtos]))


def dump_avg_metric_measures(dtos: List[MetricMeasureDTO]) -> Tuple[float, float, float]:
    if not dtos:
        return 0, 0, 0

    dtos.sort(key=lambda x: x.created_at)
    return (
        round(sum([o.value for o in dtos[: 15]]) / len(dtos[: 15]), 2),
        round(sum([o.value for o in dtos[: 7]]) / len(dtos[: 7]), 2),
        round(dtos[-1].value, 2),
    )

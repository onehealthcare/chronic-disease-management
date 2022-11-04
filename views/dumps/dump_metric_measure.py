from typing import Dict, List, Optional, Tuple

from models.chronic_disease_sys import MetricMeasureDTO, get_metric_label
from models.const import ColorEnum


def _get_color(value: float, ref_value: float) -> str:
    """
    获取指标的颜色
    :param value:
    :param ref_value: 参考值
    :return:
    """
    if not ref_value:
        return ColorEnum.BLUE
    return ColorEnum.WARN if value > ref_value else ColorEnum.NORMAL


def dump_metric_measure(dto: MetricMeasureDTO, ref_value: float) -> Optional[Dict]:
    if not dto:
        return None

    return {
        "id": dto.id,
        "value": dto.value,
        "color": _get_color(dto.value, ref_value),
        "created_at": dto.created_at.strftime("%m/%d %H:%M"),
        "_created_at": dto.created_at.strftime("%Y-%m-%d %H:%M"),
        "metric_id": dto.metric_id,
        "metric_label": get_metric_label(metric_id=dto.metric_id, label_name=dto.metric_label).text
    }


def dump_metric_measures(dtos: List[MetricMeasureDTO], ref_value: float) -> List[Dict]:
    if not dtos:
        return []

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

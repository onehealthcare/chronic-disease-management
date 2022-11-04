import datetime
from typing import List

from flask import g, request
from metaclass.cursor import Pager
from models.chronic_disease_sys import (
    MetricDTO,
    MetricLabelNotFoundException,
    MetricMeasureDTO,
    MetricMeasureNotFoundException,
    MetricNotFoundException,
    UserMetricDTO,
    create_metric_measure,
    delete_metric_measure,
    get_metric,
    get_recent_metric_measure,
    get_user_metric,
    paged_metric_measure,
)
from models.exceptions import AccessDeniedError
from utils.cursor import get_next_cursor
from utils.datetime_utils import _datetime
from views.chronic_disease import app
from views.dumps.dump_metric_measure import (
    dump_avg_metric_measures,
    dump_metric_measures,
)
from views.middleware.auth import need_login
from views.render import error, ok


@app.route("/metric_measure/", methods=["POST"])
@need_login
def measure_view():
    data = request.get_json()
    _metric_id: str = data.get('metric_id', '')
    metric_label: str = data.get('metric_label', '')
    _value: str = data.get('value', "")
    _created_at: str = data.get('created_at', "")

    if not _metric_id or not _value:
        return error('all field required')

    try:
        metric_id: int = int(_metric_id)
        value: float = float(_value)
        created_at: datetime.datetime = _datetime(_created_at)
    except (ValueError, TypeError):
        return error('invalid data')

    try:
        create_metric_measure(
            user_id=g.me.id, metric_id=metric_id,
            metric_label=metric_label,
            value=value, created_at=created_at
        )
    except (MetricLabelNotFoundException, MetricNotFoundException) as e:
        return error(e.message)

    return ok()


@app.route("/metric_measure/<int:metric_measure_id>", methods=["DELETE"])
@need_login
def delete_measure_view(metric_measure_id):
    try:
        delete_metric_measure(metric_measure_id=metric_measure_id, user_id=g.me.id)
    except (MetricMeasureNotFoundException, AccessDeniedError) as e:
        return error(e.message)

    return ok()


@app.route("/metric_measures/recent", methods=["GET"])
@need_login
def recent_measures_view():
    data = request.args

    _metric_id: str = data.get('metric_id', '')
    pager: Pager = g.pager

    if not _metric_id:
        return error('all field required')

    try:
        metric_id: int = int(_metric_id)
    except (ValueError, TypeError):
        return error('invalid data')

    try:
        dtos: List[MetricMeasureDTO] = get_recent_metric_measure(
            user_id=g.me.id, metric_id=metric_id, size=pager.size
        )
        metric: MetricDTO = get_metric(metric_id)
    except MetricNotFoundException as e:
        return error(e.message)

    avg15, avg7, v = dump_avg_metric_measures(dtos)

    # 获取用户 metric 设置
    user_metric: UserMetricDTO = get_user_metric(user_id=g.me.id, metric_id=metric_id)

    return ok({
        "datas": dump_metric_measures(dtos, ref_value=user_metric.ref_value),
        "avg_data": {
            "avg15": avg15,
            "avg7": avg7,
            "v": v
        },
        "chart_type": user_metric.chart_type,
        "ref_value": user_metric.ref_value,
        "metric_text": metric.text,
        "metric_unit": metric.unit
    })


@app.route("/metric_measures/", methods=["GET"])
@need_login
def measures_view():
    data = request.args

    _metric_id: str = data.get('metric_id', '')
    pager: Pager = g.pager

    if not _metric_id:
        return error('all field required')

    try:
        metric_id: int = int(_metric_id)
    except (ValueError, TypeError):
        return error('invalid data')

    try:
        dtos: List[MetricMeasureDTO] = paged_metric_measure(
            user_id=g.me.id, metric_id=metric_id, cursor=pager.cursor, size=pager.size
        )
        dtos, next_cursor = get_next_cursor(dtos, pager.size)
        metric: MetricDTO = get_metric(metric_id)
    except MetricNotFoundException as e:
        return error(e.message)

    # 获取用户 metric 设置
    user_metric: UserMetricDTO = get_user_metric(user_id=g.me.id, metric_id=metric_id)
    return ok({
        "datas": dump_metric_measures(dtos, ref_value=user_metric.ref_value),
        "next_cursor": next_cursor,
        "ref_value": user_metric.ref_value,
        "metric_text": metric.text,
        "metric_unit": metric.unit,
        "chart_type": user_metric.chart_type
    })

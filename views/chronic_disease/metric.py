from typing import List, Optional

import simplejson
from flask import g, request
from models.chronic_disease_sys import (
    DuplicatedMetricException,
    MetricDTO,
    MetricLabelNotFoundException,
    MetricNotFoundException,
    UserMetricDTO,
    create_metric,
    create_metric_label,
    create_user_metric,
    delete_metric,
    delete_metric_label,
    get_all_metrics,
    get_metric_chart_types,
    get_user_metric,
    query_metric_label_by_metric_id,
    query_user_metric_by_user_id,
    remove_user_metric,
    set_user_metric_chart_type,
)
from utils.logging import logger as _logger
from views.chronic_disease import app
from views.dumps.dump_metric import (
    dump_metric,
    dump_metric_label,
    dump_metric_labels,
    dump_metrics,
    dump_user_metric,
    dump_user_metrics,
)
from views.middleware.auth import need_login
from views.render import error, ok


logger = _logger('views.chronic_condition.metric')


@app.route("/metrics/", methods=['GET'])
@need_login
def get_metric_view():
    user_id = g.me.id
    metric: List[MetricDTO] = get_all_metrics()
    user_metrics_data: List[UserMetricDTO] = query_user_metric_by_user_id(user_id)

    return ok({
        "metrics": dump_metrics(dtos=metric, user_metrics=user_metrics_data),
    })


@app.route("/metric/", methods=['POST', 'DELETE'])
@need_login
def metric_view():
    data = request.get_json()

    if request.method == 'POST':
        logger.info(f"metric,create_metric,{simplejson.dumps(data)}")
        name: str = data.get('name', '')
        text: str = data.get('text', '')
        unit: str = data.get('unit', '')
        _ref_value: str = data.get('ref_value')
        ref_value: Optional[float] = float(_ref_value) if _ref_value else None

        if not name or not text or not unit:
            logger.info(f"create_metric,field_required,{simplejson.dumps(data)}")
            return error('all field required')

        try:
            dto = create_metric(name=name, text=text, unit=unit, ref_value=ref_value)
        except DuplicatedMetricException as e:
            return error(e.message)

        return ok(dump_metric(dto))

    if request.method == 'DELETE':
        logger.info(f"metric,delete_metric,{simplejson.dumps(data)}")
        try:
            id: int = int(data.get('id', 0))
        except (ValueError, TypeError):
            return error('格式错误')

        delete_metric(id)
        return ok()


@app.route('/user_metrics/', methods=['GET'])
@need_login
def user_metrics():
    user_id: int = g.me.id
    dtos: List[UserMetricDTO] = query_user_metric_by_user_id(user_id)

    return ok({
        'user_metrics': dump_user_metrics(dtos)
    })


@app.route('/user_metric/<int:metric_id>/', methods=['GET'])
@need_login
def get_user_metric_view(metric_id: int):
    user_id: int = g.me.id
    dto: Optional[UserMetricDTO] = get_user_metric(user_id=user_id, metric_id=metric_id)

    return ok({
        'user_metric': dump_user_metric(dto) if dto else {}
    })


@app.route('/user_metric/<int:metric_id>/deafult_selected', methods=['POST', 'DELETE'])
@need_login
def user_metric_default_selected(metric_id: int):
    pass


@app.route('/user_metric/<int:metric_id>/', methods=['POST', 'DELETE'])
@need_login
def user_metric(metric_id: int):
    user_id: int = g.me.id

    if request.method == "POST":
        try:
            create_user_metric(user_id=user_id, metric_id=metric_id)
        except MetricNotFoundException as e:
            logger.info(f"user_metric,create_user_metric,metric_not_found:{metric_id}")
            return error(f"metric not found:{e.message}")
        logger.info(f"user_metric,create_user_metric,{user_id}-{metric_id}")
        return ok()

    if request.method == "DELETE":
        remove_user_metric(user_id=user_id, metric_id=metric_id)
        logger.info(f"user_metric,remove_user_metric,{user_id}-{metric_id}")
        return ok()


# @app.route('/user_metrics/', methods=['POST'])
# @need_login
# def user_metric():
#     user_id: int = g.me.id
#     data = request.get_json()
#     logger.info(f"user_metric,create_user_metric,{user_id}-{simplejson.dumps(data)}")
#
#     _metric_id: str = data.get('metric_id')
#     try:
#         metric_id: int = int(_metric_id)
#     except(ValueError, TabError):
#         logger.info(f"user_metric,create_user_metric,invalid_metric_id:{_metric_id}")
#         return error("metric id 格式错误")
#
#     try:
#         create_user_metric(user_id=user_id, metric_id=metric_id)
#     except MetricNotFoundException as e:
#         logger.info(f"user_metric,create_user_metric,metric_not_found:{_metric_id}")
#         return error(f"metric not found:{e.message}")
#     return ok()


@app.route("/metric/<int:metric_id>/labels/", methods=['GET'])
@need_login
def metric_labels_view(metric_id):
    if not metric_id:
        return error("all field required")

    dtos = query_metric_label_by_metric_id(metric_id=metric_id)

    return ok({"metric_labels": dump_metric_labels(dtos)})


@app.route("/metric_label/", methods=['POST', 'DELETE'])
@need_login
def metric_label_view():
    data = request.get_json()
    if request.method == 'POST':
        logger.info(f"create_metric_label,create_create_metric,{simplejson.dumps(data)}")
        name: str = data.get('name', '')
        text: str = data.get('text', '')
        _order: str = data.get('order', '0')
        _metric_id: str = data.get('metric_id', '')

        if not name or not text or not _metric_id:
            logger.info(f"create_metric_label,field_required,{simplejson.dumps(data)}")
            return error('all field required')

        try:
            metric_id: int = int(_metric_id)
            order: int = int(_order)
        except (ValueError, TabError):
            logger.info(f"create_metric_label,invalid_metric_id,{simplejson.dumps(data)}")
            return error('格式错误')

        try:
            dto = create_metric_label(metric_id=metric_id, name=name, text=text, order=order)
        except MetricNotFoundException as e:
            logger.info(f"create_metric_label,metric_not_found,{simplejson.dumps(data)}")
            return error(e.message)

        return ok(dump_metric_label(dto))

    elif request.method == 'DELETE':
        logger.info(f"metric_label,delete_metric_label,{simplejson.dumps(data)}")
        try:
            id: int = int(data.get('id', 0))
        except (ValueError, TypeError):
            logger.info(f"delete_metric_label,invalid_metric_label_id,{simplejson.dumps(data)}")
            return error('格式错误')

        try:
            delete_metric_label(metric_label_id=id)
        except MetricLabelNotFoundException as e:
            logger.info(f"delete_metric_label,metric_label_not_found,{simplejson.dumps(data)}")
            return error(e.message)
        return ok()


@app.route("/metric/<int:metric_id>/chart_types/", methods=['GET', 'POST'])
@need_login
def metric_chart_types_view(metric_id: int):
    if not metric_id:
        return error("all field required")

    if request.method == 'GET':
        all_chart_types = get_metric_chart_types()
        # 获取用户 metric 设置
        user_metric_dto: Optional[UserMetricDTO] = get_user_metric(user_id=g.me.id, metric_id=metric_id)
        return ok({"chart_types": all_chart_types, "selected": user_metric_dto.chart_type if user_metric_dto else None})
    elif request.method == 'POST':
        data = request.get_json()
        chart_type: str = data.get('chart_type', '')
        if not chart_type:
            return error("all field required")

        set_user_metric_chart_type(user_id=g.me.id, metric_id=metric_id, chart_type=chart_type)
        return ok()

    return ok()

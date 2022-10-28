import simplejson
from flask import g, request
from models.chronic_disease_sys import (
    DuplicatedMetricException,
    MetricLabelNotFoundException,
    MetricNotFoundException,
    UserMetricDTO,
    create_metric,
    create_metric_label,
    create_user_metric,
    delete_metric,
    delete_metric_label,
    query_metric_label_by_metric_id,
    query_user_metric_by_user_id,
)
from utils.logging import logger as _logger
from views.chronic_disease import app
from views.dumps.dump_metric import (
    dump_metric,
    dump_metric_label,
    dump_metric_labels,
    dump_user_metrics,
)
from views.middleware.auth import need_admin, need_login
from views.render import error, ok


logger = _logger('views.chronic_condition.metric')


@app.route("/metric/", methods=['POST', 'DELETE'])
@need_admin
def metric_view():
    data = request.get_json()

    if request.method == 'POST':
        logger.info(f"metric,create_metric,{simplejson.dumps(data)}")
        name: str = data.get('name', '')
        text: str = data.get('text', '')
        unit: str = data.get('unit', '')

        if not name or not text or not unit:
            logger.info(f"create_metric,field_required,{simplejson.dumps(data)}")
            return error('all field required')

        try:
            dto = create_metric(name=name, text=text, unit=unit)
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
    dtos: UserMetricDTO = query_user_metric_by_user_id(user_id)

    return ok({
        'user_metrics': dump_user_metrics(dtos)
    })


@app.route('/user_metrics/', methods=['POST'])
@need_login
def user_metric():
    user_id: int = g.me.id
    data = request.get_json()
    logger.info(f"user_metric,create_user_metric,{user_id}-{simplejson.dumps(data)}")

    _metric_id: str = data.get('metric_id')
    try:
        metric_id: int = int(_metric_id)
    except(ValueError, TabError):
        logger.info(f"user_metric,create_user_metric,invalid_metric_id:{_metric_id}")
        return error("metric id 格式错误")

    try:
        create_user_metric(user_id=user_id, metric_id=metric_id)
    except MetricNotFoundException as e:
        logger.info(f"user_metric,create_user_metric,metric_not_found:{_metric_id}")
        return error(f"metric not found:{e.message}")
    return ok()


# @app.route("/metric_labels/", methods=['GET'])
# @need_admin
# def metric_labels_view():
#     data = request.args
#     try:
#         metric_id = data.get("metric_id", "0")
#     except (ValueError, TypeError):
#         return error("invalid metric id")
#
#     if not metric_id:
#         return error("all field required")
#
#     dtos = query_metric_label_by_metric_id(metric_id=metric_id)
#
#     return ok({"metric_labels": dump_metric_labels(dtos)})


@app.route("/metric/<int:metric_id>/labels/", methods=['GET'])
@need_login
def metric_labels_view(metric_id):
    if not metric_id:
        return error("all field required")

    dtos = query_metric_label_by_metric_id(metric_id=metric_id)

    return ok({"metric_labels": dump_metric_labels(dtos)})


@app.route("/metric_label/", methods=['POST', 'DELETE'])
@need_admin
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

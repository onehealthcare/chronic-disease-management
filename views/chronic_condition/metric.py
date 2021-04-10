import simplejson
from flask import g, request
from models.chronic_condition_sys import (
    DuplicatedMetricException,
    MetricNotFoundException,
    UserMetricDTO,
    create_metric,
    create_user_metric,
    query_user_metric_by_user_id,
)
from utils.logging import logger as _logger
from views.chronic_condition import app
from views.dumps.dump_metric import dump_metric, dump_user_metrics
from views.middleware.auth import need_admin, need_login
from views.render import error, ok


logger = _logger('views.chronic_condition.metric')


@app.route("/metric/", methods=['POST'])
@need_admin
def create_metric_view():
    data = request.get_json()
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

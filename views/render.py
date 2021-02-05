import datetime
import decimal

import simplejson
from flask import Response


def default(obj):
    if obj is None:
        return ''
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return str(obj)
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if callable(obj):
        return obj()
    json_func = getattr(obj, 'for_json', None)
    if json_func:
        return json_func()
    raise TypeError(repr(obj) + "is not JSON serializable")


def jsonify(data, status_code=200):
    return Response(simplejson.dumps(data, default=default),
                    mimetype='application/json', status=status_code)


def ok(content=''):
    msg = {
        'status': 'ok',
        'content': content,
    }

    resp = jsonify(msg)
    return resp


def error(error='', status_code=400):
    if callable(error):
        error = error()

    if isinstance(error, (tuple, list)):
        msg = {
            'status': 'error',
            'code': error[0],
            'msg': error[1],
        }
    else:
        msg = {
            'status': 'error',
            'msg': error,
        }

    resp = jsonify(msg, status_code=status_code)
    return resp

from functools import wraps

from flask import g
from views.common import ApiError
from views.render import error


def need_login(func):
    @wraps(func)
    def _(*args, **kwargs):
        me = g.me
        if me:
            return func(*args, **kwargs)

        return error(ApiError.login_needed, status_code=403)

    return _


def need_admin(func):
    @wraps(func)
    def _(*args, **kwargs):
        me = g.me
        if me:
            if me.is_admin():
                return func(*args, **kwargs)
            return error(ApiError.admin_needed, status_code=403)

        return error(ApiError.login_needed, status_code=403)

    return _

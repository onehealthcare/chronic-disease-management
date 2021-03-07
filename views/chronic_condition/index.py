from typing import List

import simplejson
from flask import g, request
from models.chronic_condition_sys import create_doc_package
from utils.logging import logger as _logger
from views.chronic_condition import app
from views.middleware.auth import need_login
from views.render import error, ok


logger = _logger('views.chronic_condition.index')


@app.route('/doc_package/', methods=['POST'])
@need_login
def upload_docs():
    user_id: int = g.me.id
    data = request.get_json()
    logger.info(f"upload_docs,requeset,{user_id}-{simplejson.dumps(data)}")

    idents: List[str] = data.get('idents', [])
    if not idents:
        return error('未上传任何文件')

    desc = data.get('desc', '')

    create_doc_package(user_id=user_id, idents=idents, desc=desc)

    return ok()

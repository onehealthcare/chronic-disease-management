from typing import List

import simplejson
from flask import g, request
from models.chronic_condition_sys import (
    DocPackageDTO,
    DocPackageNotFoundException,
    create_doc_package,
    delete_doc_package_by_user_id_and_package_id,
    paged_doc_package_by_user_id,
)
from models.exceptions import AccessDeniedError
from utils.cursor import get_next_cursor
from utils.logging import logger as _logger
from views.chronic_condition import app
from views.dumps.dump_doc_package import dump_doc_packages
from views.middleware.auth import need_login
from views.render import error, ok


logger = _logger('views.chronic_condition.index')


@app.route('/doc_package/', methods=['POST', 'GET', 'DELETE'])
@need_login
def upload_docs():
    user_id: int = g.me.id
    if request.method == 'POST':
        data = request.get_json()
        logger.info(f"upload_docs,requeset,{user_id}-{simplejson.dumps(data)}")

        idents: List[str] = data.get('idents', [])
        if not idents:
            return error('未上传任何文件')

        desc = data.get('desc', '')

        create_doc_package(user_id=user_id, idents=idents, desc=desc)

        return ok()
    elif request.method == 'GET':
        pager = g.pager
        doc_packages: List[DocPackageDTO] = paged_doc_package_by_user_id(user_id=user_id, cursor=pager.cursor, size=pager.size)

        next_cursor: str = ''
        doc_packages, next_cursor = get_next_cursor(doc_packages, pager.size)

        return ok({
            'doc_packages': dump_doc_packages(doc_packages),
            'next_cursor': next_cursor
        })
    elif request.method == 'DELETE':
        data = request.get_json()
        logger.info(f"delete_doc_package,requeset,{user_id}-{simplejson.dumps(data)}")
        try:
            package_id: int = int(data.get('package_id', '0'))
        except (ValueError, TypeError):
            return error('ID 格式错误')

        try:
            delete_doc_package_by_user_id_and_package_id(user_id=user_id, package_id=package_id)
        except (DocPackageNotFoundException, AccessDeniedError) as e:
            logger.error(f"delete_doc_package,fail,{e.message}-{user_id}-{simplejson.dumps(data)}")
            return error(e.message)

        return ok()

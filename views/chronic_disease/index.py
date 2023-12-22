from typing import List

import simplejson
from flask import g, request
from models.chronic_disease_sys import (
    DocPackageDTO,
    DocPackageIdentNotFoundException,
    DocPackageNotFoundException,
    create_doc_package,
    delete_doc_package_by_user_id_and_package_id,
    get_doc_package_by_id,
    paged_doc_package_by_user_id,
    paged_search_doc_package_by_user_id,
    update_doc_package_by_user_id_and_package_id,
)
from models.exceptions import AccessDeniedError
from utils.cursor import get_next_cursor
from utils.logging import file_logger as _logger
from views.chronic_disease import app
from views.dumps.dump_doc_package import dump_doc_package, dump_doc_packages
from views.middleware.auth import need_login
from views.render import error, ok


logger = _logger('views.chronic_disease.index')


@app.route('/doc_packages/', methods=['GET'])
@need_login
def doc_packages_view():
    user_id: int = g.me.id
    pager = g.pager
    doc_packages: List[DocPackageDTO] = paged_doc_package_by_user_id(user_id=user_id, cursor=pager.cursor, size=pager.size + 1)
    doc_packages, next_cursor = get_next_cursor(doc_packages, pager.size)

    return ok({
        'doc_packages': dump_doc_packages(doc_packages),
        'next_cursor': next_cursor
    })


@app.route('/doc_packages/search/', methods=['GET'])
@need_login
def search_doc_packages():
    user_id: int = g.me.id
    keyword: str = request.args.get('q', '')
    if not keyword:
        return ok({
            'doc_packages': [],
            'next_cursor': ''
        })

    pager = g.pager
    doc_packages: List[DocPackageDTO] = paged_search_doc_package_by_user_id(user_id=user_id, keyword=keyword, cursor=pager.cursor, size=pager.size)

    next_cursor: str = ''
    doc_packages, next_cursor = get_next_cursor(doc_packages, pager.size)

    return ok({
        'doc_packages': dump_doc_packages(doc_packages),
        'next_cursor': next_cursor
    })


@app.route('/doc_package/', methods=['POST', 'GET', 'DELETE'])
@need_login
def doc_package():
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
        try:
            package_id: int = request.args.get('package_id', '0')
        except (ValueError, TypeError):
            return error('ID 格式错误')

        doc_package: DocPackageDTO = get_doc_package_by_id(package_id=package_id)

        return ok({'doc_package': dump_doc_package(doc_package)})
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


@app.route('/update_doc_package/', methods=['POST'])
@need_login
def update_doc_package():
    user_id: int = g.me.id
    data = request.get_json()
    logger.info(f"update_doc_package,requeset,{user_id}-{simplejson.dumps(data)}")

    try:
        update_doc_package_by_user_id_and_package_id(user_id, data.get('id', 0), data)
    except (DocPackageNotFoundException, AccessDeniedError, DocPackageIdentNotFoundException) as e:
        logger.error(f"update_doc_package,fail,{e.message}-{user_id}-{simplejson.dumps(data)}")
        return error(e.message)

    return ok()

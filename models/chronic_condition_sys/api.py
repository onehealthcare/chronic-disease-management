from typing import Dict, List, Optional

from models.chronic_condition_sys.dao.doc_package import (
    DocPackageDAO,
    DocPackageIdentDAO,
)
from models.chronic_condition_sys.dto.doc_package import DocPackageDTO
from models.chronic_condition_sys.exceptions import (
    DocPackageIdentNotFoundException,
    DocPackageNotFoundException,
)
from models.exceptions import AccessDeniedError
from models.init_db import db


def get_doc_package_by_id(package_id: int) -> DocPackageDTO:
    dao = DocPackageDAO.get_by_id(package_id)
    if not dao:
        DocPackageNotFoundException()

    return DocPackageDTO.from_dao(dao)


@db.atomic()
def create_doc_package(user_id: int, idents: List[str], desc: str) -> DocPackageDTO:
    dpa: DocPackageDAO = DocPackageDAO.create(user_id=user_id, desc=desc)
    for ident in idents:
        DocPackageIdentDAO.create(package_id=dpa.id, ident=ident)

    return get_doc_package_by_id(dpa.id)


def paged_doc_package_by_user_id(user_id: int, cursor: int, size: int = 0) -> List[DocPackageDTO]:
    daos = DocPackageDAO.paged_by_user_id(user_id=user_id, cursor=cursor, size=size)

    return [DocPackageDTO.from_dao(dao) for dao in daos]


def paged_search_doc_package_by_user_id(user_id: int, keyword: str, cursor: int, size: int = 0) -> List[DocPackageDTO]:
    if not keyword:
        return []

    daos = DocPackageDAO.search_by_keyword(user_id=user_id, keyword=keyword, cursor=cursor, size=size)

    return [DocPackageDTO.from_dao(dao) for dao in daos]


def delete_doc_package_by_user_id_and_package_id(user_id: int, package_id: int):
    dao = DocPackageDAO.get_by_id(package_id)
    if not dao:
        raise DocPackageNotFoundException

    if dao.user_id != user_id:
        raise AccessDeniedError

    dao.delete()


def delete_doc_ident_by_id(ident_id: int):
    dao: DocPackageIdentDAO = DocPackageIdentDAO.get_by_id(ident_id=ident_id)
    if not dao:
        raise DocPackageIdentNotFoundException

    dao.delete()


@db.atomic()
def update_doc_package_by_user_id_and_package_id(user_id: int, package_id: int, data: Dict):
    if not package_id or not user_id:
        return

    dao = DocPackageDAO.get_by_id(package_id)
    if not dao:
        raise DocPackageNotFoundException

    if dao.user_id != user_id:
        raise AccessDeniedError

    desc: str = data.get('desc', '')
    if desc:
        dao.desc = desc
    dao.save()

    # 处理 ident
    new_idents: List[str] = data.get('idents', [])
    if new_idents:
        # 原来的 ident
        raw_ident: List[str] = [ident.ident for ident in dao.idents]
        raw_ident_map: Dict[str, int] = {ident.ident: ident.id for ident in dao.idents}

        # 要删除的 ident
        for ident in set(raw_ident) - set(new_idents):
            ident_id: Optional[int] = raw_ident_map.get(ident)
            if not ident_id:
                return

            delete_doc_ident_by_id(ident_id=ident_id)

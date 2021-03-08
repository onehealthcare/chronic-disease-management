from typing import List

from models.chronic_condition_sys.dao.doc_package import (
    DocPackageDAO,
    DocPackageIdentDAO,
)
from models.chronic_condition_sys.dto.doc_package import DocPackageDTO
from models.chronic_condition_sys.exceptions import DocPackageNotFoundException
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


def delete_doc_package_by_user_id_and_package_id(user_id: int, package_id: int):
    dao = DocPackageDAO.get_by_id(package_id)
    if not dao:
        raise DocPackageNotFoundException

    if dao.user_id != user_id:
        raise AccessDeniedError

    dao.delete()

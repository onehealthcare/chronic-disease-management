from typing import List

from models.chronic_condition_sys.dao.doc_package import (
    DocPackageDAO,
    DocPackageIdentDAO,
)
from models.chronic_condition_sys.dto.doc_package import DocPackageDTO
from models.chronic_condition_sys.exceptions import DocPackageNotFoundException
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

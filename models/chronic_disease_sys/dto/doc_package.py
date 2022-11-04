import datetime
from typing import List

from pydantic import BaseModel
from utils.datetime_utils import _datetime


class DocPackageIdentDTO(BaseModel):
    id: int
    package_id: int
    ident: str
    status: int
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao) -> 'DocPackageIdentDTO':
        return DocPackageIdentDTO(
            id=dao.id,
            package_id=dao.package_id,
            ident=dao.ident,
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )


class DocPackageDTO(BaseModel):
    id: int
    user_id: int
    desc: str
    status: int
    idents: List[DocPackageIdentDTO]
    ident_urls: List[str]
    ident_pattern_urls: List[str]
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao) -> 'DocPackageDTO':
        return DocPackageDTO(
            id=dao.id,
            user_id=dao.user_id,
            idents=[DocPackageIdentDTO.from_dao(o) for o in dao.idents],
            ident_urls=dao.ident_urls,
            ident_pattern_urls=dao.ident_pattern_urls,
            desc=dao.desc,
            status=dao.status,
            created_at=_datetime(dao.created_at)
        )

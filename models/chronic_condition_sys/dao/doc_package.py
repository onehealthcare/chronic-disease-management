import datetime
from typing import List

from models.base import Base
from models.const import CommonStatus
from peewee import CharField, DateTimeField, IntegerField, TextField


class DocPackageDAO(Base):
    """
    用户的一次上传
    """
    desc = TextField()
    user_id = IntegerField(index=True)
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'chronic_condition_doc_package'

    @classmethod
    def get_by_id(cls, package_id: int) -> 'DocPackageDAO':
        return cls.get(cls.id == package_id)

    @property
    def idents(self) -> List['DocPackageIdentDAO']:
        return DocPackageIdentDAO.get_by_package_id(self.id)

    @property
    def ident_urls(self) -> List[str]:
        return [ident.ident for ident in self.idents]


class DocPackageIdentDAO(Base):
    """
    用户的一次上传中包含的图片
    """
    package_id = IntegerField(index=True)
    ident = CharField()
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'chronic_condition_doc_package_ident'

    @classmethod
    def get_by_id(cls, package_id: int) -> 'DocPackageIdentDAO':
        return cls.get(cls.id == package_id)

    @classmethod
    def get_by_package_id(cls, package_id: int) -> List['DocPackageIdentDAO']:
        return list(DocPackageIdentDAO.select().where(DocPackageIdentDAO.package_id == package_id, DocPackageIdentDAO.status == CommonStatus.NORMAL))

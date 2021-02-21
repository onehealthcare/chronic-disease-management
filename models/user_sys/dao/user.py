import datetime

from models.base import Base
from models.const import CommonStatus
from peewee import CharField, DateTimeField, IntegerField


class UserDAO(Base):
    name = CharField(index=True)
    bits = IntegerField(default=0)
    ident = CharField(default='')
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'user'

    @classmethod
    def get_by_id(cls, user_id: int) -> 'UserDAO':
        return UserDAO.get(UserDAO.id == user_id)

    @classmethod
    def get_by_name(cls, name: str) -> 'UserDAO':
        return UserDAO.get(UserDAO.name == name)

    def update_status(self, status: int):
        self.status = status
        self.save()

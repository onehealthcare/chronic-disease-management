import datetime

from models.base import Base
from models.const import CommonStatus, Role
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

    def set_bit(self, bit):
        self.bits = self.bits | bit  # type: ignore
        self.save()

    def clear_bit(self, bit):
        self.bits = self.bits & (~bit)
        self.save()

    def check_bit(self, bit):
        return self.bits & bit

    def set_role_admin(self):
        self.set_bit(Role.BITS_ROLE_ADMIN)

    def set_role_clear(self):
        self.bits = 0
        self.save()

    def is_admin(self):
        return bool(self.check_bit(Role.BITS_ROLE_ADMIN))

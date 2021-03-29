import datetime

from models.base import Base
from models.const import CommonStatus
from peewee import CharField, DateTimeField, IntegerField


class UserPhoneDAO(Base):
    user_id = IntegerField(index=True)
    phone = CharField(index=True)
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'user_phone'

    @classmethod
    def get_by_user_id(cls, user_id: int) -> 'UserPhoneDAO':
        return cls.get(cls.user_id == user_id)

    @classmethod
    def get_by_phone(cls, phone: str) -> 'UserPhoneDAO':
        return cls.get(cls.phone == phone)

    def update_status(self, status: int):
        self.status = status
        self.save()

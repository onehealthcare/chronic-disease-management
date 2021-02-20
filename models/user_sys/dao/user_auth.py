import datetime

from models.base import Base
from models.const import CommonStatus
from peewee import BlobField, CharField, DateTimeField, IntegerField


class UserAuthDAO(Base):
    user_id = IntegerField(index=True)
    third_party_id = CharField(index=True)
    provider = IntegerField(index=True)
    detail_json = BlobField(default='{}')
    status = IntegerField(index=True, default=CommonStatus.NORMAL)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'user_auth'

    @classmethod
    def get_by_user_id_and_provider(cls, user_id: int, provider: int) -> 'UserAuthDAO':
        return UserAuthDAO.get(UserAuthDAO.user_id == user_id,
                               UserAuthDAO.provider == provider)

    @classmethod
    def get_by_third_party_id_and_provider(cls, third_party_id: str, provider: int) -> 'UserAuthDAO':
        return UserAuthDAO.get(UserAuthDAO.third_party_id == third_party_id,
                               UserAuthDAO.provider == provider)

    def update_status(self, status: int):
        self.status = status
        self.save()

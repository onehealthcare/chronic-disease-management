import datetime

from models.const import Role
from pydantic import BaseModel
from utils.datetime_utils import _datetime


class UserDTO(BaseModel):
    id: int
    name: str
    status: int
    bits: int
    ident: str
    created_at: datetime.datetime

    @classmethod
    def from_dao(cls, dao):
        return UserDTO(
            id=dao.id,
            name=dao.name,
            bits=dao.bits,
            status=dao.status,
            ident=dao.ident,
            created_at=_datetime(dao.created_at)
        )

    def check_bit(self, bit):
        return self.bits & bit

    def is_admin(self):
        return bool(self.check_bit(Role.BITS_ROLE_ADMIN))

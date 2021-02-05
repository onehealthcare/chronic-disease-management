import datetime
from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    name: str
    status: int
    bits: int
    ident: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    @classmethod
    def from_dao(cls, dao):
        return UserDTO(
            id=dao.id,
            name=dao.name,
            bits=dao.bits,
            status=dao.status,
            ident=dao.ident,
            created_at=dao.created_at
        )

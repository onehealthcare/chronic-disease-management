from typing import Optional
import datetime
from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    name: str
    bits: int
    status: int
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

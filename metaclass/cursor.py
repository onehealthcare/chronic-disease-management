from pydantic import BaseModel


class Pager(BaseModel):
    cursor: int
    size: int

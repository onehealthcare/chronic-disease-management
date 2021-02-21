from pydantic import BaseModel


class Code2SessionData(BaseModel):
    open_id: str
    session_key: str

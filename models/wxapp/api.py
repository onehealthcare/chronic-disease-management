from metaclass.wxapp.session import Code2SessionData
from models.init_db import wxapp_client


def code_to_session(code: str) -> Code2SessionData:
    return wxapp_client.code_to_session(code)

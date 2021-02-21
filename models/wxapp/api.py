import wechatpy
from metaclass.wxapp.session import Code2SessionData
from models.init_db import wxapp_client
from models.wxapp.exceptions import InvalidAuthCodeError


def code_to_session(code: str) -> Code2SessionData:
    try:
        return wxapp_client.code_to_session(code)
    except wechatpy.exceptions.WeChatClientException:
        raise InvalidAuthCodeError

from config import (
    MYSQL_DB,
    MYSQL_HOST,
    MYSQL_PASSWD,
    MYSQL_PORT,
    MYSQL_USER,
    WXAPP_ID,
    WXAPP_SECRET,
)
from playhouse.pool import PooledMySQLDatabase
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatWxa


db = PooledMySQLDatabase(MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWD,
                         host=MYSQL_HOST, port=MYSQL_PORT)

wxapp = WeChatWxa(WeChatClient(WXAPP_ID, WXAPP_SECRET))

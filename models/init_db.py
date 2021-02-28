from config import (
    MYSQL_DB,
    MYSQL_HOST,
    MYSQL_PASSWD,
    MYSQL_PORT,
    MYSQL_USER,
    QCLOUD_CC_COS_BUCKET,
    QCLOUD_CC_COS_REGION,
    QCLOUD_SECRET_ID,
    QCLOUD_SECRET_KEY,
    WXAPP_ID,
    WXAPP_SECRET,
)
from libs.qcloud import QCloudCOSClient
from playhouse.pool import PooledMySQLDatabase
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatWxa


db = PooledMySQLDatabase(MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWD,
                         host=MYSQL_HOST, port=MYSQL_PORT)

wxapp_client = WeChatWxa(WeChatClient(WXAPP_ID, WXAPP_SECRET))

# 存储用户单据
qcloud_cos_client = QCloudCOSClient(secret_id=QCLOUD_SECRET_ID,
                                    secret_key=QCLOUD_SECRET_KEY,
                                    bucket=QCLOUD_CC_COS_BUCKET,
                                    region=QCLOUD_CC_COS_REGION,
                                    allow_prefix='*')

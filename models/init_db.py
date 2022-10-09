import redis
from config import (
    MYSQL_DB,
    MYSQL_HOST,
    MYSQL_PASSWD,
    MYSQL_PORT,
    MYSQL_USER,
    QCLOUD_CDM_COS_BUCKET,
    QCLOUD_CDM_COS_REGION,
    QCLOUD_SECRET_ID,
    QCLOUD_SECRET_KEY,
    REDIS_URL,
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
                                    bucket=QCLOUD_CDM_COS_BUCKET,
                                    region=QCLOUD_CDM_COS_REGION,
                                    allow_prefix='*')

# redis
redis_conn = redis.Redis.from_url(REDIS_URL, decode_responses=True)  # 存binary 数据，不需要 decode response

import os


DEBUG = bool(os.environ.get('DEBUG', False))

HOST = "https://web.nps.motn.top"

# MySQL
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER', 'tonghs')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'tonghs')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'web-template')

# sentry
SENTRY_DSN = "https://ad8effa8e62040b6826c8a44b025ad6c@o327962.ingest.sentry.io/5624232"

LOG_PATH = os.environ.get('LOG_PATH', "/var/log/cdm")


# 微信小程序
WXAPP_ID = os.environ.get('WXAPP_ID', '')
WXAPP_SECRET = os.environ.get('WXAPP_SECRET', '')


# jwt
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret')

# API sign secret
API_SECRET = os.environ.get('API_SECRET', 'your-secret')

# qcloud
QCLOUD_SECRET_ID = os.environ.get('QCLOUD_SECRET_ID', '<QCLOUD_SECRET_ID>')
QCLOUD_SECRET_KEY = os.environ.get('QCLOUD_SECRET_KEY', '<QCLOUD_SECRET_KEY>')

# 慢病管理 bucket
QCLOUD_CDM_COS_BUCKET = os.environ.get('QCLOUD_CDM_COS_BUCKET', '')
QCLOUD_CDM_COS_REGION = os.environ.get('QCLOUD_CDM_COS_REGION', '')
QCLOUD_CDM_COS_DOMAIN = os.environ.get('QCLOUD_CDM_COS_DOMAIN', '')
QCLOUD_CDM_COS_URL = 'https://{}/{}{}'.format(QCLOUD_CDM_COS_DOMAIN, '{}', '?imageView2/2/w/1024/q/85')
QCLOUD_CDM_COS_URL_PATTERN = 'https://{}/{}{}'.format(
    QCLOUD_CDM_COS_DOMAIN, '{}', '?imageMogr2/crop/#width#x#height#/gravity/center/rquality/85'
)

# redis
REDIS_DB = os.environ.get('REDIS_DB', 'test-redis')
REDIS_URL = f'redis://{REDIS_DB}/0'

# qcloud SMS
SMS_SDK_APP_ID = "<SMS_SDK_APP_ID>"
SMS_SIGN_NAME = "<SMS_SIGN_NAME>"
SMS_WXAPP_LOGIN_TEMPLATE_ID = "<SMS_SIGN_NAME>"

STRAVA_CLIENT_ID = 0
STRAVA_CLIENT_SECRET = "<STRAVA_CLIENT_SECRET>"

AZURE_VISION_KEY = "<AZURE_VISION_KEY>"
AZURE_VISION_ENDPOINT = "<AZURE_VISION_ENDPOINT>"

AZURE_OPEN_AI_KEY = "<AZURE_OPEN_AI_KEY>"
AZURE_OPEN_AI_ENDPOINT = "<AZURE_OPEN_AI_ENDPOINT>"

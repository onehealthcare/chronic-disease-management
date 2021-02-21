import os


DEBUG = bool(os.environ.get('DEBUG', False))

# MySQL
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER', 'tonghs')
MYSQL_PASSWD = os.environ.get('MYSQL_PASSWD', 'tonghs')
MYSQL_DB = os.environ.get('MYSQL_DB', 'web-template')

# sentry
SENTRY_DSN = "https://ad8effa8e62040b6826c8a44b025ad6c@o327962.ingest.sentry.io/5624232"

LOG_PATH = os.environ.get('LOG_PATH', "/var/log/web-template")


# 微信小程序
WXAPP_ID = os.environ.get('WXAPP_ID', '')
WXAPP_SECRET = os.environ.get('WXAPP_SECRET', '')


# jwt
JWT_SECRET = os.environ.get('JWT_SECRET', 'you-secret')

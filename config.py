import os

DEBUG = bool(os.environ.get('DEBUG', False))

# MySQL
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER', 'tonghs')
MYSQL_PASSWD = os.environ.get('MYSQL_PASSWD', 'tonghs')
MYSQL_DB = os.environ.get('MYSQL_DB', 'web-template')

# sentry
SENTRY_DSN = "https://2c959e2e5cc945fb88b543644e281ddf@sentry.io/1840050"

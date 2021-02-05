from config import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWD, MYSQL_PORT, MYSQL_USER
from playhouse.pool import PooledMySQLDatabase


db = PooledMySQLDatabase(MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWD,
                         host=MYSQL_HOST, port=MYSQL_PORT)

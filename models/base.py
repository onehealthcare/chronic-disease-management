import datetime
from peewee import Model, DateTimeField, DoesNotExist
from playhouse.pool import PooledMySQLDatabase

from config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWD,
    MYSQL_DB,
)

db = PooledMySQLDatabase(MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWD,
                         host=MYSQL_HOST, port=MYSQL_PORT)


class Base(Model):
    _created_at = DateTimeField(default=datetime.datetime.now)
    _updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    @classmethod
    def get(cls, *query, **kwargs):
        try:
            return super(Base, cls).get(*query, **kwargs)
        except DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if hasattr(self, 'updated_at'):
            self.updated_at = datetime.datetime.now()
        return super(Base, self).save(*args, **kwargs)

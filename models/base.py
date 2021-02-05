import datetime

from models.init_db import db
from peewee import DateTimeField, DoesNotExist, Model


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
            self._updated_at = datetime.datetime.now()
        return super(Base, self).save(*args, **kwargs)

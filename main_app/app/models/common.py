from datetime import datetime
from email.policy import default
from enum import unique
import peewee
from ..database.database import db

class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)
    role = peewee.IntegerField()
    class Meta:
        database = db

class Token(peewee.Model):
    owner = peewee.ForeignKeyField(User, backref="token")
    token = peewee.CharField(index=True)
    created_at = peewee.DateTimeField(default=datetime.now())

    class Meta:
        database = db
from datetime import datetime
from email.policy import default
from enum import unique
import peewee
from ..database.database import db

class User(peewee.Model):
    firstName = peewee.CharField(max_length=80)
    lastName = peewee.CharField(max_length=80)
    email = peewee.CharField(unique=True, index=True)
    password = peewee.CharField()
    changedPassword = peewee.CharField()
    changedEmail = peewee.CharField()
    upline = peewee.CharField()
    downline = peewee.CharField()
    tree = peewee.CharField()
    kyc = peewee.BooleanField()
    product = peewee.CharField()
    marketingCampaign = peewee.CharField()
    isActive = peewee.BooleanField(default=True)
    role = peewee.IntegerField()
    class Meta:
        database = db

class Token(peewee.Model):
    owner = peewee.ForeignKeyField(User, backref="token")
    token = peewee.CharField(index=True)
    created_at = peewee.DateTimeField(default=datetime.now())

    class Meta:
        database = db
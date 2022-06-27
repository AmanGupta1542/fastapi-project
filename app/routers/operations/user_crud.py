import os
from fastapi import Depends
from typing import Union
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from ...settings import config
from ...dependencies import common as CDepends
from ...models import common as CModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

   
def get_user(email: str):
    users = CModel.User.select()
    print([user.email for user in users])
    print([user for user in users])

    print(CModel.User)
    print(CModel.User.email)
    print(CModel.User.email == 'aman@mistpl.com')
    existing_user = CModel.User.get(CModel.User.email == email)
    print(existing_user)
    return existing_user
    os._exit(0)
    return True


def authenticate_user(email: str, password: str, dependencies=[Depends(CDepends.get_db)]):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta , None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.settings.secret_key, algorithm=config.settings.algorithm)
    return encoded_jwt
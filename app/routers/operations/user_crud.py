import os
from fastapi import Depends, HTTPException, status
from typing import Union
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer  

from ...settings import config
from ...dependencies import common as CDepends
from ...models import common as CModel
from ...schemas import common as CSchemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

   
def get_user(email: str):
    existing_user = CModel.User.get(CModel.User.email == email)
    return existing_user


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

def save_access_token(user, expires_in):
    access_token = create_access_token(data={"sub": user.email}, expires_delta=expires_in)
    token = CModel.Token(owner_id = user, token= access_token)
    token.save()
    return access_token


def get_user_data(user_id: int):
    return CModel.User.filter(CModel.User.id == user_id).first()

async def get_current_user(token: str = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.settings.secret_key, algorithms=[config.settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = CSchemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: CSchemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Union
from datetime import datetime, timedelta, timezone
import pytz

from ..dependencies import common as CDepends
from ..schemas import common as CSchemas
from ..settings import config
from .operations import user_crud as UserO
from ..models import common as CModels

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(CDepends.get_db)],
    responses={404: {"description": "Not found"}},
)

@router.post("/login", response_model=CSchemas.Token)
def login(login_data: CSchemas.LoginData = Body()):
    user = UserO.authenticate_user(login_data.email, login_data.password)
    user_tokens_list = user.token.select().dicts()
    is_token_exist = True if len(user_tokens_list) > 0 else False
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)
    if not is_token_exist:
        access_token = UserO.save_access_token(user, timedelta(minutes=15))
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        last_created_token = user_tokens_list[-1]['token']
        token_time = datetime.now(timezone.utc) - user_tokens_list[-1]['created_at'].astimezone(pytz.UTC)

        if token_time.total_seconds()/60 > 15:
            token_for_del = CModels.Token.delete().where(CModels.Token.owner_id == user.id)
            token_for_del.execute()
            access_token = UserO.save_access_token
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            return {"access_token": last_created_token, "token_type": "bearer"}

@router.post("/logout")
def logout(user_id: int = Body()):
    token_for_del = CModels.Token.delete().where(CModels.Token.owner_id == user_id)
    token_for_del.execute()
    return {"message": "logout successful"}
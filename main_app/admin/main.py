from fastapi import FastAPI, Depends, status, HTTPException
from .routers import users, settings
from fastapi.security import HTTPBearer 
from typing import Any

from ..app.routers.operations.user_crud import get_current_active_user

auth_admin = HTTPBearer()

def user(current_user : Any = Depends(get_current_active_user)):
    if current_user.role == 1:
        return current_user
    else :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can access this api",
            headers={"WWW-Authenticate": "Bearer"},
        )

app = FastAPI(dependencies=[Depends(user)])

app.include_router(users.router)
app.include_router(settings.router)
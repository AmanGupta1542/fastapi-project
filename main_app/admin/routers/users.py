from fastapi import Depends, Request, APIRouter
from ..dependencies import common as CDepends
from ..schemas import common as CSchemas
from typing import Any , List

from ...app.models.common import User

router = APIRouter(
    # dependencies=[Depends(CDepends.get_db)],
    responses={404: {"description": "Not found"}},
)

@router.get("/user-details", response_model=List[CSchemas.User])
def get_users(skip: int = 0, limit: int = 100, all_users=False):
    if all_users :
        return list(User.select())
    else :
        return list(User.select().offset(skip).limit(limit))
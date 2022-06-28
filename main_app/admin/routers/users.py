from fastapi import Depends, Request, APIRouter

router = APIRouter(
    # dependencies=[Depends(CDepends.get_db)],
    responses={404: {"description": "Not found"}},
)

@router.get("/user-details")
def user_details(request: Request):
    return {"status": "success"}
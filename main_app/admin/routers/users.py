from fastapi import APIRouter

router = APIRouter(
    # dependencies=[Depends(CDepends.get_db)],
    responses={404: {"description": "Not found"}},
)

@router.get("/user-details")
def user_details():
    return {"status": "success"}
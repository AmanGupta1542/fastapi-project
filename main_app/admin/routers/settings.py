from fastapi import APIRouter

router = APIRouter()

@router.get("/settings")
def user_details():
    return {"status": "success"}
from fastapi import APIRouter

router = APIRouter()

@router.get("/settings")
def settings():
    return {"status": "success"}
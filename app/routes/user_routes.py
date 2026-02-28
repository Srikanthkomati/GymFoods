from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
def read_current_user(current_user: str = Depends(get_current_user)):
    return {
        "message": "Protected route accessed",
        "user_id": current_user
    }

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User 
from app.schemas.user_schema import UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# --------------------------------
# Get Current User Profile
# --------------------------------
@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

# --------------------------------
# Update User Profile
# --------------------------------
@router.put("/update-profile", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    update_data = user_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user
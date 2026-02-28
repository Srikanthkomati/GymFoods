from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import SessionLocal
from app import models, schemas
from app.auth_utils import create_access_token, create_refresh_token, verify_token
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        age=user.age,
        height=user.height,
        weight=user.weight,
        goal=user.goal,
        city=user.city,
        diet_type=user.diet_type,
        budget=user.budget
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
    }
@router.post("/refresh")
def refresh_token(refresh_token: str):
    user_id = verify_token(refresh_token, expected_type="refresh")

    new_access_token = create_access_token(
        data={"sub": user_id}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
